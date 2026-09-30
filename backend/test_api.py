import requests
import json

url = "http://127.0.0.1:8000/api/generate"
data = {
    "topic": "Kuliner Sragen yang Terkenal",
    "category": "News"
}

print("Mengirim request ke AI Engine...")
try:
    response = requests.post(url, data=data, timeout=120)
    result = response.json()
    
    if response.ok:
        print("=== SUKSES ===")
        print(f"Title: {result.get('title', 'N/A')}")
        print(f"Slug: {result.get('slug', 'N/A')}")
        print(f"Keyphrase: {result.get('keyphrase', 'N/A')}")
        print(f"Keywords: {result.get('keywords_list', [])}")
        print(f"Meta Desc: {result.get('meta_description', 'N/A')}")
        print(f"Image: {result.get('featured_image_url', 'N/A')}")
        print(f"Content length: {len(result.get('content_body', ''))} chars")
    else:
        print(f"=== ERROR {response.status_code} ===")
        print(json.dumps(result, indent=2))
except Exception as e:
    print(f"Request failed: {e}")
