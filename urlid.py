import re
from urllib.parse import urlparse

# Define match rules
YTDL_DOMAINS = ["youtube.com", "youtu.be", "vimeo.com", "dailymotion.com", "soundcloud.com"]
TORRENT_KEYWORDS = ["magnet:?", ".torrent"]
DIRECT_EXTENSIONS = [".zip", ".rar", ".7z", ".pdf", ".exe", ".mp4", ".mkv", ".apk", ".tar.gz", ".deb"]

def identify_url_type(url):
    url = url.strip()

    # Handle magnet links
    if url.startswith("magnet:?"):
        return "qbmirror"

    # Parse the URL
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    path = parsed.path.lower()

    # YouTube-dl / streaming links
    if any(d in domain for d in YTDL_DOMAINS):
        return "ytdl"

    # Torrent file links
    if any(t in url for t in TORRENT_KEYWORDS):
        return "qbmirror"

    # Direct download links
    if any(path.endswith(ext) for ext in DIRECT_EXTENSIONS):
        return "mirror"

    return "unknown"

if __name__ == "__main__":
    print("🔗 URL Type Identifier (type 'exit' to quit)\n")
    while True:
        user_input = input("Enter URL: ").strip()
        if user_input.lower() in ['exit', 'quit']:
            break
        result = identify_url_type(user_input)
        print(f"Type ➤ {result}\n")
