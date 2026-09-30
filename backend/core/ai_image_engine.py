import requests
import os
import uuid
import urllib.parse

def generate_featured_image(prompt: str) -> str:
    """
    Generate an image using Pollinations.ai free API based on the prompt.
    Downloads the image to web/static/images/ and returns the local filepath.
    """
    image_dir = os.path.join("web", "static", "images")
    os.makedirs(image_dir, exist_ok=True)
    
    # URL encode the prompt and add Flux model parameters for photorealism
    safe_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1280&height=720&nologo=true&model=flux&enhance=true"
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        filename = f"featured_{uuid.uuid4().hex[:8]}.jpg"
        filepath = os.path.join(image_dir, filename)
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        # Return the relative path for web access and internal usage
        return f"static/images/{filename}"
    except Exception as e:
        print(f"Error generating image: {e}")
        return ""
