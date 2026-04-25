import json
import re
import urllib.request
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).parent


def load_api_key():
    env = ROOT / ".env"
    for line in env.read_text().splitlines():
        line = line.strip()
        if line.startswith("YOUTUBE_API_KEY="):
            return line.split("=", 1)[1].strip()
    raise ValueError(".env : clé YOUTUBE_API_KEY introuvable")


def parse_iso8601(duration):
    """PT1H2M3S → secondes"""
    m = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", duration)
    if not m:
        raise ValueError(f"Format durée inconnu : {duration}")
    h, mi, s = (int(x or 0) for x in m.groups())
    return h * 3600 + mi * 60 + s


def fetch_durations(api_key, video_ids):
    params = urllib.parse.urlencode({
        "id": ",".join(video_ids),
        "part": "contentDetails",
        "key": api_key,
    })
    url = f"https://www.googleapis.com/youtube/v3/videos?{params}"
    with urllib.request.urlopen(url) as resp:
        data = json.loads(resp.read())

    return {
        item["id"]: parse_iso8601(item["contentDetails"]["duration"])
        for item in data["items"]
    }


def main():
    api_key = load_api_key()

    playlist_path = ROOT / "playlist.json"
    playlist = json.loads(playlist_path.read_text())

    ids = [v["id"] for v in playlist]
    print(f"Récupération des durées pour {len(ids)} vidéos…")

    durations = fetch_durations(api_key, ids)

    updated = 0
    for video in playlist:
        vid_id = video["id"]
        if vid_id in durations:
            old = video["duration"]
            new = durations[vid_id]
            video["duration"] = new
            diff = f"{old}s → {new}s" if old != new else f"{new}s (inchangé)"
            print(f"  {video['artist']} — {video['title']}: {diff}")
            updated += 1
        else:
            print(f"  ⚠ ID introuvable sur YouTube : {vid_id} ({video['title']})")

    playlist_path.write_text(json.dumps(playlist, ensure_ascii=False, indent=2))
    print(f"\nplaylist.json mis à jour ({updated}/{len(ids)} vidéos).")


if __name__ == "__main__":
    main()
