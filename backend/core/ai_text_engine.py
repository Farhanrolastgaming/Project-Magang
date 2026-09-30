import os
import json
import re
import time
from config.settings import settings

# Daftar model Gemini yang akan dicoba berurutan
GEMINI_MODELS = [
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-2.5-flash",
    "gemini-2.0-flash",
]

# Daftar model Groq yang bisa digunakan (List 2026 yang aktif di Server Groq)
GROQ_MODELS = [
    "openai/gpt-oss-120b",
    "qwen/qwen3.8-27b",
    "openai/gpt-oss-20b"
]

def generate_article_content(topic_or_keyword: str) -> dict:
    """
    Generates a full SEO-optimized article based on the topic.
    Uses multi-model fallback across Gemini and Groq with exponential backoff for 503 errors.
    """
    import os
    from dotenv import dotenv_values
    
    # Ambil Env Variables secara realtime (langsung dari file) agar tidak perlu restart Uvicorn
    # saat user mengedit kunci di .env.
    env_dict = dotenv_values(".env")
    api_key_gemini = env_dict.get("GEMINI_API_KEY", "")
    api_key_groq = env_dict.get("GROQ_API_KEY", "")
    
    if not api_key_gemini and not api_key_groq:
        return {"error": "Semua API Key (Gemini & Groq) kosong. Silakan isi salah satu di file .env"}
        
    prompt = f"""
    Buatkan saya artikel berbahasa Indonesia untuk di post di web dengan focus keywordnya '{topic_or_keyword}', dan kembangkan judulnya agar support dan keindeks di pencarian AI/support GEO dan support SEO dengan maksimal 60 karakter (jangan lebih!). 
    Buat minimal 400 kata. 
    Dan buatkan 12 keywordnya dalam bentuk koma (buat keyword yang sesuai dengan isi materi dan topik artikel (jangan yang out of topic, dan jangan yang melebar. jadi spesifik sesuai focus keyphrase)). 
    Buatkan meta descriptionnya (kurang dari 153 huruf/karakter). 
    Buat format artikelnya agar support GEO dan SEO. keyword phrase 5 kata.
    
    Output WAJIB berupa raw JSON valid tanpa markdown (tidak boleh ada ```json tag). 
    Gunakan keys berikut dengan tipe data yang ditentukan:
    {{
        "title": "String (Judul artikel panjang asli)",
        "seo_title": "String (Judul SEO maksimal 60 karakter)",
        "slug": "String (url-friendly format)",
        "meta_description": "String (Maksimal 153 karakter)",
        "keyphrase": "String (Keyword phrase persis 5 kata)",
        "keywords_list": ["Keyword1", "Keyword2", "Keyword3", "Keyword4", "Keyword5", "Keyword6", "Keyword7", "Keyword8", "Keyword9", "Keyword10", "Keyword11", "Keyword12"],
        "content_body": "String HTML"
    }}
    
    Aturan struktur konten content_body:
    - HANYA gunakan elemen HTML berikut: <h4>, dan <p>. 
    - Anda DILARANG KERAS menggunakan tag <h1>, <h2>, atau <h3>. 
    - Gunakan HANYA tag <h4> untuk semua poin-poin atau subjudul/section di dalam artikel.
    - Gunakan <p> untuk semua kalimat isi. JANGAN gunakan tag HTML lain (tanpa <html>, <body>, <li>, dll).
    - JANGAN memasukkan Judul Utama ataupun Meta Deskripsi ke dalam `content_body`! (Sistem kami yang akan merangkainya).
    - Sebutkan secara natural nama lokasi/daerah Indonesia (GEO Support) di dalam paragraf isi secara natural.
    
    Pastikan JSON valid dan escape karakternya. Dilarang menambahkan teks narasi apapun selain JSON murni!
    """
    
    last_error = "Tidak ada percobaan yang dilakukan."
    
    # 1. Coba menggunakan Gemini API terlebih dahulu
    if api_key_gemini:
        from google import genai
        client = genai.Client(api_key=api_key_gemini)
        
        for model_name in GEMINI_MODELS:
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    print(f"[AI Engine] Mencoba model Gemini: {model_name} (percobaan {attempt + 1}/{max_retries})")
                    response = client.models.generate_content(
                        model=model_name,
                        contents=prompt,
                    )
                    text = response.text.strip()
                    
                    data = _parse_and_inject_json(text)
                    print(f"[AI Engine] Berhasil dengan Gemini model: {model_name}")
                    return data
                    
                except Exception as e:
                    error_str = str(e)
                    last_error = f"[Gemini {model_name}]: {error_str}"
                    
                    if "429" in error_str:
                        print(f"[AI Engine] Kuota model Gemini {model_name} habis (429). Pindah ke model lain...")
                        break
                    elif "503" in error_str:
                        wait_time = 5 * (attempt + 1)
                        print(f"[AI Engine] Model Gemini {model_name} overload (503). Tunggu {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                    elif "404" in error_str:
                        print(f"[AI Engine] Model Gemini {model_name} tidak tersedia (404). Coba model lain...")
                        break
                    else:
                        print(f"[AI Engine] Error Gemini {model_name}: {error_str}")
                        break
    
    # 2. Jika Gemini gagal semua dan Groq API Key ada, fallback ke GROQ
    if api_key_groq:
        import groq
        client = groq.Groq(api_key=api_key_groq)
        
        for model_name in GROQ_MODELS:
            max_retries = 2
            for attempt in range(max_retries):
                try:
                    print(f"[AI Engine] Fallback ke model Groq: {model_name} (percobaan {attempt + 1}/{max_retries})")
                    
                    response = client.chat.completions.create(
                        messages=[
                            {"role": "user", "content": prompt}
                        ],
                        model=model_name,
                        temperature=0.7,
                        max_tokens=2500,
                    )
                    
                    text = response.choices[0].message.content.strip()
                    data = _parse_and_inject_json(text)
                    print(f"[AI Engine] Berhasil dengan Groq model: {model_name}")
                    return data
                    
                except Exception as e:
                    error_str = str(e)
                    last_error = f"[Groq {model_name}]: {error_str}"
                    
                    if "rate_limit_exceeded" in error_str or "429" in error_str:
                        print(f"[AI Engine] Kuota model Groq {model_name} limit/habis. Pindah ke model lain...")
                        break
                    elif "503" in error_str or "timeout" in error_str.lower():
                        wait_time = 3 * (attempt + 1)
                        print(f"[AI Engine] Model Groq {model_name} sibuk/timeout. Tunggu {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                    else:
                        print(f"[AI Engine] Error Groq {model_name}: {error_str}")
                        break
        
    return {"error": f"Semua model API (Gemini/Groq) gagal me-response/habis kuota. Detail terakhir: {last_error}"}


def _parse_and_inject_json(text: str) -> dict:
    """Helper for cleaning markdown prefix and injecting wikipedia."""
    # Clean potential markdown JSON wrapping
    if "```json" in text:
        text = text.split("```json")[1]
    if "```" in text:
        text = text.split("```")[0]
        
    # Sometime AI leaves trailing texts
    start_idx = text.find("{")
    end_idx = text.rfind("}")
    if start_idx != -1 and end_idx != -1:
        text = text[start_idx:end_idx+1]
        
    data = json.loads(text.strip())
    
    # Post-process content to inject Wikipedia outlinks for regions
    data['content_body'], data['wikipedia_outlinks'] = _inject_wikipedia_outlinks(data['content_body'])
    return data


def _inject_wikipedia_outlinks(content: str) -> tuple[str, list]:
    locations = {
        "Jakarta": "https://id.wikipedia.org/wiki/Daerah_Khusus_Ibukota_Jakarta",
        "Surabaya": "https://id.wikipedia.org/wiki/Kota_Surabaya",
        "Medan": "https://id.wikipedia.org/wiki/Kota_Medan",
        "Bandung": "https://id.wikipedia.org/wiki/Kota_Bandung",
        "Yogyakarta": "https://id.wikipedia.org/wiki/Daerah_Istimewa_Yogyakarta",
        "Semarang": "https://id.wikipedia.org/wiki/Kota_Semarang",
        "Sukoharjo": "https://id.wikipedia.org/wiki/Kabupaten_Sukoharjo",
        "Surakarta": "https://id.wikipedia.org/wiki/Kota_Surakarta",
        "Solo": "https://id.wikipedia.org/wiki/Kota_Surakarta",
        "Bali": "https://id.wikipedia.org/wiki/Bali",
        "Lombok": "https://id.wikipedia.org/wiki/Pulau_Lombok",
        "Sragen": "https://id.wikipedia.org/wiki/Kabupaten_Sragen",
        "Malang": "https://id.wikipedia.org/wiki/Kota_Malang",
        "Makassar": "https://id.wikipedia.org/wiki/Kota_Makassar",
        "Denpasar": "https://id.wikipedia.org/wiki/Kota_Denpasar",
        "Bogor": "https://id.wikipedia.org/wiki/Kota_Bogor",
        "Depok": "https://id.wikipedia.org/wiki/Kota_Depok",
        "Tangerang": "https://id.wikipedia.org/wiki/Kota_Tangerang",
        "Bekasi": "https://id.wikipedia.org/wiki/Kota_Bekasi",
        "Boyolali": "https://id.wikipedia.org/wiki/Kabupaten_Boyolali",
        "Klaten": "https://id.wikipedia.org/wiki/Kabupaten_Klaten",
    }
    
    injected_links = []
    
    for loc, url in locations.items():
        pattern = r'\b' + re.escape(loc) + r'\b'
        if re.search(pattern, content, flags=re.IGNORECASE):
            content = re.sub(pattern, f'<a href="{url}" target="_blank" rel="noopener noreferrer">{loc}</a>', content, count=1, flags=re.IGNORECASE)
            injected_links.append(url)
            
    return content, injected_links
