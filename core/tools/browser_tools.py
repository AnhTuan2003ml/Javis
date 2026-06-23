"""Safe browser tools for Javis.

These tools only open/read public web pages. They must not send, post,
submit, delete, or modify user data.
"""

import json
import re
import subprocess
import urllib.parse
import urllib.request
import webbrowser
from pathlib import Path

_CONTEXT_FILE = Path(__file__).resolve().parents[2] / "data" / "state" / "tool_context.json"


def _load_context() -> dict:
    try:
        if _CONTEXT_FILE.exists():
            return json.loads(_CONTEXT_FILE.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {}


def _save_context(**updates) -> None:
    try:
        _CONTEXT_FILE.parent.mkdir(parents=True, exist_ok=True)
        data = _load_context()
        data.update(updates)
        _CONTEXT_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass


def get_last_youtube_query() -> str:
    return str(_load_context().get("last_youtube_query", "")).strip()


_KNOWN_SITES = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "facebook": "https://www.facebook.com",
    "github": "https://github.com",
    "gmail": "https://mail.google.com",
    "wikipedia": "https://www.wikipedia.org",
    "stackoverflow": "https://stackoverflow.com",
    "linkedin": "https://www.linkedin.com",
    "instagram": "https://www.instagram.com",
    "twitter": "https://twitter.com",
    "x": "https://x.com",
}


def _open_url(url: str) -> None:
    """Open URL using Chrome when available, fallback to default browser.

    Do not use `cmd /c start` with shell=True for dynamic URLs because Windows
    cmd can mis-parse words such as "the" or characters such as `&`.
    """
    chrome_candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for chrome in chrome_candidates:
        try:
            if Path(chrome).exists():
                subprocess.Popen([chrome, '--profile-directory=Default', '--new-window', url])
                return
        except Exception:
            pass
    webbrowser.open(url)


def _clean_query(text: str) -> str:
    text = (text or "").strip()
    text = re.sub(r"\s+", " ", text)
    return text.strip(" .,'\"")


def google_search(query: str) -> str:
    query = _clean_query(query)
    if not query:
        _open_url("https://www.google.com")
        return "Google opened."

    url = "https://www.google.com/search?q=" + urllib.parse.quote_plus(query)
    _open_url(url)
    return f"Searching Google for: {query}"


def youtube_search(query: str) -> str:
    query = _clean_query(query)
    if not query:
        _open_url("https://www.youtube.com")
        return "YouTube opened."

    _save_context(last_youtube_query=query)
    url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(query)
    _open_url(url)
    return f"Searching YouTube for: {query}"


def _find_youtube_video_id(query: str, index: int = 1) -> str | None:
    """Find the first YouTube video id for a query without sending/modifying data.

    Preferred path: yt-dlp if installed, because it is more stable than scraping.
    Fallback: read the public YouTube search HTML and extract the first watch id.
    """
    query = _clean_query(query)
    if not query:
        return None

    index = max(1, min(int(index or 1), 10))

    # 1) Optional dependency: yt-dlp. Works well on Windows if installed.
    try:
        completed = subprocess.run(
            ["yt-dlp", "--default-search", f"ytsearch{index}", "--get-id", query],
            capture_output=True,
            text=True,
            timeout=18,
        )
        if completed.returncode == 0:
            ids = [line.strip() for line in completed.stdout.splitlines() if re.fullmatch(r"[A-Za-z0-9_-]{11}", line.strip())]
            if len(ids) >= index:
                return ids[index - 1]
            if ids:
                return ids[0]
    except Exception:
        pass

    # 2) Fallback: public search result page. This is read-only.
    try:
        url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(query)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=12) as resp:
            html = resp.read().decode("utf-8", errors="ignore")

        seen = set()
        ids = []
        for video_id in re.findall(r'"videoId":"([A-Za-z0-9_-]{11})"', html):
            if video_id not in seen:
                ids.append(video_id)
                seen.add(video_id)
        for video_id in re.findall(r"watch\?v=([A-Za-z0-9_-]{11})", html):
            if video_id not in seen:
                ids.append(video_id)
                seen.add(video_id)
        if len(ids) >= index:
            return ids[index - 1]
        if ids:
            return ids[0]
    except Exception:
        return None

    return None


def youtube_play(query: str = "", index: int = 1) -> str:
    """Open the Nth YouTube video result for a query.

    This is a safe read/open action. It does not send, post, delete, or modify data.
    """
    query = _clean_query(query) or get_last_youtube_query()
    try:
        index = max(1, min(int(index or 1), 10))
    except Exception:
        index = 1

    if not query:
        _open_url("https://www.youtube.com")
        return "YouTube opened."

    _save_context(last_youtube_query=query)
    video_id = _find_youtube_video_id(query, index=index)
    if video_id:
        url = f"https://www.youtube.com/watch?v={video_id}&autoplay=1"
        _open_url(url)
        ordinal = {1: "first", 2: "second", 3: "third"}.get(index, f"#{index}")
        return f"Playing {ordinal} YouTube result for: {query}"

    # If YouTube blocks scraping or yt-dlp is missing, still do something useful.
    youtube_search(query)
    return f"Could not resolve video #{index} automatically, searching YouTube for: {query}"


def open_website(site: str) -> str:
    site = _clean_query(site).lower()
    if not site:
        return "No website specified."

    site = re.sub(r"^(open|go to|visit)\s+", "", site).strip()
    if site in {"the", "a", "an", "to", "for", "in", "on", "video", "result", "second", "first", "third"}:
        return "I need a real website name, not a filler word."

    url = _KNOWN_SITES.get(site)

    if not url:
        if site.startswith(("http://", "https://")):
            url = site
        elif "." in site:
            url = "https://" + site
        else:
            # Unknown one-word site: search instead of guessing a risky URL.
            return google_search(site)

    _open_url(url)
    return f"Opened website: {site}"
