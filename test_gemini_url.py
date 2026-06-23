import webbrowser

# Test different Gemini URL formats
urls = [
    "https://gemini.google.com/?q=ml",
    "https://gemini.google.com/app?q=ml", 
    "https://gemini.google.com/chat?q=ml",
    "https://bard.google.com/?q=ml",
    "https://gemini.google.com/",
    "https://gemini.google.com/app"
]

print("Testing Gemini URLs:")
for i, url in enumerate(urls, 1):
    print(f"{i}. {url}")

# Test the first URL
print(f"\nOpening: {urls[0]}")
webbrowser.open(urls[0])