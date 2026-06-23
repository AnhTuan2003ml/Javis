import requests
import io

def test_image_generation():
    try:
        url = "https://image.pollinations.ai/prompt/cat"
        print(f"Testing URL: {url}")
        
        response = requests.get(url, timeout=30)
        print(f"Status code: {response.status_code}")
        print(f"Content type: {response.headers.get('content-type')}")
        print(f"Content length: {len(response.content)}")
        
        if response.status_code == 200:
            with open("test_cat.jpg", "wb") as f:
                f.write(response.content)
            print("Image saved as test_cat.jpg")
        else:
            print("Failed to generate image")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_image_generation()