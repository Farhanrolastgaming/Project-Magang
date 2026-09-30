import requests
import base64
import os
import mimetypes

class WPIntegrator:
    def __init__(self, wp_url: str, username: str, app_password: str):
        # Ensure wp_url has no trailing slash
        self.wp_url = wp_url.rstrip("/")
        self.username = username
        self.app_password = app_password
        
        credentials = f"{self.username}:{self.app_password}"
        token = base64.b64encode(credentials.encode()).decode('utf-8')
        
        self.headers = {
            "Authorization": f"Basic {token}"
        }

    def upload_media(self, file_path: str) -> int:
        """
        Uploads a local image file to WordPress Media Library.
        Returns the Media ID if successful, else None.
        """
        url = f"{self.wp_url}/wp-json/wp/v2/media"
        
        if not os.path.exists(file_path):
            print(f"Error: media file {file_path} not found.")
            return None
            
        filename = os.path.basename(file_path)
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            mime_type = "image/jpeg"
            
        media_headers = self.headers.copy()
        media_headers["Content-Disposition"] = f"attachment; filename={filename}"
        media_headers["Content-Type"] = mime_type

        try:
            with open(file_path, "rb") as f:
                data = f.read()
                
            response = requests.post(url, headers=media_headers, data=data)
            response.raise_for_status()
            
            res_json = response.json()
            return {
                "id": res_json.get("id"),
                "url": res_json.get("source_url")
            }
        except requests.exceptions.HTTPError as e:
            error_msg = e.response.text if hasattr(e, 'response') and e.response else str(e)
            raise Exception(f"WordPress Media Upload ditolak (Status {e.response.status_code if e.response else ''}): {error_msg}")
        except Exception as e:
            raise Exception(f"Gagal koneksi ke server WordPress saat Upload Media: {str(e)}")

    def get_categories_list(self, limit: int = 25) -> list:
        # Menarik data kategori (maksimal n - default 25 limit untuk performa web)
        url = f"{self.wp_url}/wp-json/wp/v2/categories?per_page={limit}&orderby=count&order=desc"
        try:
            res = requests.get(url, headers=self.headers, timeout=10)
            res.raise_for_status()
            items = res.json()
            cats = [item["name"] for item in items]
            return cats
        except Exception as e:
            print(f"Gagal memuat list kategori: {e}")
            return []

    def get_or_create_category(self, category_name: str, parent_id: int = None) -> int:
        if not category_name:
            return None
            
        url = f"{self.wp_url}/wp-json/wp/v2/categories"
        search_url = f"{url}?search={category_name}"
        if parent_id:
            search_url += f"&parent={parent_id}"
        
        try:
            res = requests.get(search_url, headers=self.headers)
            res.raise_for_status()
            items = res.json()
            # Cari pencocokan persis
            for item in items:
                if item["name"].lower() == category_name.lower():
                    # Jika minta parent spesifik, validasi juga, jika tidak ada req parent return aja.
                    if parent_id and item.get("parent") == parent_id:
                        return item["id"]
                    elif not parent_id:
                        return item["id"]
                    
            # Jika tidak eksis, buat kategori baru
            payload = {"name": category_name}
            if parent_id:
                payload["parent"] = parent_id
            res_create = requests.post(url, headers=self.headers, json=payload)
            res_create.raise_for_status()
            return res_create.json().get("id")
        except Exception as e:
            print(f"Error Kategor: {e}")
            return None

    def get_or_create_tags(self, tags_list: list) -> list:
        url = f"{self.wp_url}/wp-json/wp/v2/tags"
        tag_ids = []
        
        for t in tags_list:
            if not t or not t.strip():
                continue
            t_clean = t.strip()
            try:
                search_url = f"{url}?search={t_clean}"
                res = requests.get(search_url, headers=self.headers)
                if res.status_code == 200:
                    items = res.json()
                    found_id = None
                    for item in items:
                        if item["name"].lower() == t_clean.lower():
                            found_id = item["id"]
                            break
                    
                    if found_id:
                        tag_ids.append(found_id)
                    else:
                        # Buat tag baru
                        res_create = requests.post(url, headers=self.headers, json={"name": t_clean})
                        if res_create.status_code in [200, 201]:
                            tag_ids.append(res_create.json().get("id"))
            except Exception as e:
                print(f"Error sinkronisasi tag {t_clean}: {e}")
                
        return tag_ids

    def create_post(self, title: str, content: str, categories_payload: list, 
                    status: str = "draft", slug: str = None, 
                    featured_media_id: int = None,
                    tags_list: list = None,
                    yoast_data: dict = None) -> dict:
        """
        Creates a post in WordPress with Category hierarchy mapping, Tags, and Yoast.
        Returns a dict: {"id": ID, "link": Permalink}
        """
        url = f"{self.wp_url}/wp-json/wp/v2/posts"
        
        payload = {
            "title": title,
            "content": content,
            "status": status,
        }
        
        if slug:
            payload["slug"] = slug
            
        if featured_media_id:
            payload["featured_media"] = featured_media_id
            
        # Category Mapping (Hierarchical)
        cat_ids = []
        if categories_payload:
            for cat_obj in categories_payload:
                p_id = None
                p_name = cat_obj.get("parent")
                c_name = cat_obj.get("name")
                
                if p_name:
                    p_id = self.get_or_create_category(p_name)
                    
                c_id = self.get_or_create_category(c_name, p_id)
                if c_id:
                    cat_ids.append(c_id)
                    
        if cat_ids:
            payload["categories"] = cat_ids
            
        # Tags Mapping
        if tags_list:
            t_ids = self.get_or_create_tags(tags_list)
            if t_ids:
                payload["tags"] = t_ids
                
        # Yoast SEO Meta Injection
        if yoast_data:
            payload["meta"] = {
                "_yoast_wpseo_title": yoast_data.get("seo_title", ""),
                "_yoast_wpseo_metadesc": yoast_data.get("meta_description", ""),
                "_yoast_wpseo_focuskw": yoast_data.get("focus_keyword", "")
            }
            # Kategori Utama Yoast SEO (Ambil array index 0 sebagai Primary Category)
            if cat_ids:
                payload["meta"]["_yoast_wpseo_primary_category"] = cat_ids[0]
            
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            res_json = response.json()
            return {"id": res_json.get("id"), "link": res_json.get("link")}
        except requests.exceptions.HTTPError as e:
            error_msg = e.response.text if hasattr(e, 'response') and e.response else str(e)
            raise Exception(f"WordPress Publish ditolak (Status {e.response.status_code if e.response else ''}): {error_msg}")
        except Exception as e:
            raise Exception(f"Gagal koneksi ke server WordPress saat Posting: {str(e)}")

    def update_post(self, post_id: int, content: str) -> bool:
        url = f"{self.wp_url}/wp-json/wp/v2/posts/{post_id}"
        payload = {"content": content}
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Update Post Error: {e}")
            return False
