"""
Fills in TODO IDs in playlists by searching YouTube.
Run this script once per day (quota = 10,000 units; each search = 100 units).
It skips entries that already have a real ID.
"""
import json
import time
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path

ROOT = Path(__file__).parent

PLAYLISTS = [
    "playlist-france80s.json",
    "playlist-france00s.json",
]


def load_api_key():
    for line in (ROOT / ".env").read_text().splitlines():
        if line.startswith("YOUTUBE_API_KEY="):
            return line.split("=", 1)[1].strip()
    raise ValueError("YOUTUBE_API_KEY not found")


def search_video(api_key, artist, title):
    query = f"{artist} {title}"
    params = urllib.parse.urlencode({
        "q": query,
        "part": "snippet",
        "type": "video",
        "videoCategoryId": "10",
        "maxResults": "1",
        "key": api_key,
    })
    url = f"https://www.googleapis.com/youtube/v3/search?{params}"
    with urllib.request.urlopen(url) as resp:
        data = json.loads(resp.read())
    items = data.get("items", [])
    if not items:
        return None, None
    item = items[0]
    return item["id"]["videoId"], item["snippet"]["title"]


def main():
    api_key = load_api_key()
    total_searched = total_fixed = 0

    for filename in PLAYLISTS:
        path = ROOT / filename
        videos = json.loads(path.read_text())
        changed = False

        print(f"\n── {filename} ──")
        for video in videos:
            if not video["id"].startswith("TODO"):
                continue

            artist, title = video["artist"], video["title"]
            print(f"  Searching: {artist} — {title} … ", end="", flush=True)
            try:
                vid_id, yt_title = search_video(api_key, artist, title)
                total_searched += 1
                if vid_id:
                    video["id"] = vid_id
                    changed = True
                    total_fixed += 1
                    print(f"→ {vid_id} | {yt_title}")
                else:
                    print("NOT FOUND")
                time.sleep(0.2)
            except urllib.error.HTTPError as e:
                body = e.read().decode()
                if "quotaExceeded" in body:
                    print(f"\n⚠ Quota exhausted after {total_searched} searches. Saving progress.")
                    if changed:
                        path.write_text(json.dumps(videos, ensure_ascii=False, indent=2))
                    return
                raise

        if changed:
            path.write_text(json.dumps(videos, ensure_ascii=False, indent=2))
            print(f"  Saved {filename}")

    print(f"\nDone. {total_fixed}/{total_searched} IDs filled.")


if __name__ == "__main__":
    main()
