import json
import re
import urllib.request
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).parent

PLAYLISTS = [
    "playlist.json",
    "playlist-90s.json",
    "playlist-80s.json",
]

BATCH_SIZE = 50  # limite YouTube Data API


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


def fetch_batch(api_key, video_ids):
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


def fetch_durations(api_key, video_ids):
    """Récupère les durées en batches de 50."""
    durations = {}
    batches = [video_ids[i:i + BATCH_SIZE] for i in range(0, len(video_ids), BATCH_SIZE)]
    for i, batch in enumerate(batches, 1):
        print(f"  Appel API {i}/{len(batches)} ({len(batch)} IDs)…")
        durations.update(fetch_batch(api_key, batch))
    return durations


def main():
    api_key = load_api_key()

    # Charger toutes les playlists
    playlists = {}
    for filename in PLAYLISTS:
        path = ROOT / filename
        playlists[filename] = json.loads(path.read_text())

    # Collecter les IDs uniques (un même clip peut apparaître dans plusieurs playlists)
    all_ids = list({v["id"] for videos in playlists.values() for v in videos})
    total_videos = sum(len(v) for v in playlists.values())
    print(f"{len(PLAYLISTS)} playlists — {total_videos} vidéos — {len(all_ids)} IDs uniques\n")

    durations = fetch_durations(api_key, all_ids)
    print()

    # Mettre à jour chaque playlist
    grand_total = grand_updated = grand_missing = 0
    for filename, videos in playlists.items():
        updated = missing = 0
        print(f"── {filename} ──")
        for video in videos:
            vid_id = video["id"]
            if vid_id in durations:
                old = video["duration"]
                new = durations[vid_id]
                video["duration"] = new
                diff = f"{old}s → {new}s" if old != new else f"{new}s (inchangé)"
                print(f"  {video['artist']} — {video['title']}: {diff}")
                updated += 1
            else:
                print(f"  ⚠ ID introuvable : {vid_id} ({video['title']})")
                missing += 1

        (ROOT / filename).write_text(json.dumps(videos, ensure_ascii=False, indent=2))
        print(f"  → {updated}/{len(videos)} mis à jour" + (f", {missing} manquant(s)" if missing else "") + "\n")

        grand_total += len(videos)
        grand_updated += updated
        grand_missing += missing

    print(f"Total : {grand_updated}/{grand_total} vidéos mises à jour" +
          (f", {grand_missing} ID(s) introuvable(s)" if grand_missing else "") + ".")


if __name__ == "__main__":
    main()
