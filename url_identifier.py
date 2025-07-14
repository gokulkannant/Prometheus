from urllib.parse import urlparse

YTDL_DOMAINS = ["youtube.com", "youtu.be", "vimeo.com", "dailymotion.com", "soundcloud.com"]
TORRENT_KEYWORDS = ["magnet:?", ".torrent"]
DIRECT_EXTENSIONS = [".zip", ".rar", ".7z", ".pdf", ".exe", ".mp4", ".mkv", ".apk", ".tar.gz", ".deb"]

def identify_url_type(url: str) -> str:
    url = url.strip()

    if url.startswith("magnet:?"):
        return f"/qbmirror {url}"

    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    path = parsed.path.lower()

    if any(d in domain for d in YTDL_DOMAINS):
        return f"/ytdl {url}"

    if any(t in url for t in TORRENT_KEYWORDS):
        return f"/qbmirror {url}"

    if any(path.endswith(ext) for ext in DIRECT_EXTENSIONS):
        return f"/mirror {url}"

    return f"/unknown {url}"
