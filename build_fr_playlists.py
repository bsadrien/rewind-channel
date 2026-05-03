"""
Search YouTube for each song and build playlist-france80s.json and playlist-france00s.json.
Uses the YouTube Data API v3 /search endpoint.
"""
import json
import time
import urllib.request
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).parent

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
        "videoCategoryId": "10",  # Music
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
    vid_id = item["id"]["videoId"]
    snippet_title = item["snippet"]["title"]
    return vid_id, snippet_title

FRANCE_80S = [
    ("Téléphone", "Un autre monde", 1984),
    ("Téléphone", "Argent trop cher", 1981),
    ("Indochine", "L'aventurier", 1982),
    ("Indochine", "3ème sexe", 1985),
    ("Jean-Jacques Goldman", "Il suffira d'un signe", 1981),
    ("Jean-Jacques Goldman", "Quand la musique est bonne", 1982),
    ("Jean-Jacques Goldman", "Je marche seul", 1983),
    ("Mylène Farmer", "Libertine", 1986),
    ("Mylène Farmer", "Sans contrefaçon", 1987),
    ("Mylène Farmer", "Tristana", 1987),
    ("Alain Bashung", "Gaby oh Gaby", 1980),
    ("Alain Bashung", "Vertige de l'amour", 1981),
    ("Daniel Balavoine", "L'aziza", 1985),
    ("Daniel Balavoine", "Je ne suis pas un héros", 1982),
    ("Vanessa Paradis", "Joe le taxi", 1987),
    ("Renaud", "Mistral gagnant", 1985),
    ("Renaud", "Morgane de toi", 1983),
    ("Renaud", "Dans mon HLM", 1983),
    ("Étienne Daho", "Week-end à Rome", 1986),
    ("Étienne Daho", "Tombé pour la France", 1985),
    ("Les Rita Mitsouko", "Marcia Baila", 1985),
    ("Les Rita Mitsouko", "Andy", 1986),
    ("Niagara", "L'amour à la plage", 1987),
    ("Lio", "Banana Split", 1980),
    ("Laurent Voulzy", "Belle île en mer, Marie-Galante", 1987),
    ("France Gall", "Résiste", 1981),
    ("France Gall", "Il jouait du piano debout", 1982),
    ("Elsa", "T'en va pas", 1986),
    ("Kaoma", "Lambada", 1989),
    ("Jeanne Mas", "Toute première fois", 1985),
    ("Jeanne Mas", "En rouge et noir", 1986),
    ("Alain Souchon", "Ça n'est pas la peine", 1985),
    ("Marc Lavoine", "Elle a les yeux revolver", 1986),
    ("Francis Cabrel", "Sarbacane", 1989),
    ("Cookie Dingler", "Femme Libérée", 1984),
    ("Dalida", "Mourir sur scène", 1983),
    ("Images", "In the Night", 1986),
    ("Début de soirée", "Nuits de lune", 1986),
    ("Stephan Eicher", "Déjeuner en paix", 1988),
    ("Taxi Girl", "Cherchez le garçon", 1980),
    ("Serge Gainsbourg", "Lemon Incest", 1984),
    ("Patrick Bruel", "Marre de cette nana-là", 1984),
    ("Julien Clerc", "Femmes, je vous aime", 1981),
    ("Herbert Léonard", "Pour le plaisir", 1985),
    ("Guesch Patti", "Etienne", 1987),
    ("Jean Luc Lahaye", "Femme que j'aime", 1985),
    ("Patricia Kaas", "Mademoiselle chante le blues", 1988),
    ("Desireless", "Voyage Voyage", 1986),
    ("Alain Chamfort", "Rock'n Rose", 1980),
    ("Michel Sardou", "La java de Broadway", 1985),
    ("Isabelle Adjani", "Pull marine", 1983),
    ("Gold", "Plus près des étoiles", 1985),
    ("Michel Berger", "Quelques mots d'amour", 1981),
    ("Pierre Bachelet", "Les corons", 1982),
    ("Alain Souchon", "Ultra-moderne solitude", 1988),
    ("Véronique Sanson", "Le monde est fou", 1981),
    ("Noir Désir", "Aux teachers du rock'n roll", 1987),
    ("Charlélie Couture", "Comme un avion sans ailes", 1983),
    ("Alain Bashung", "Ma petite entreprise", 1987),
    ("Les Inconnus", "Les problèmes d'amour", 1989),
]

FRANCE_00S = [
    ("Alizée", "Moi Lolita", 2000),
    ("Stromae", "Alors on danse", 2009),
    ("Modjo", "Lady (Hear Me Tonight)", 2000),
    ("Daft Punk", "Harder Better Faster Stronger", 2001),
    ("Justice", "D.A.N.C.E.", 2007),
    ("Bob Sinclar", "Love Generation", 2005),
    ("Kyo", "Je cours", 2003),
    ("Calogero", "En apesanteur", 2004),
    ("Mickey 3D", "Respire", 2003),
    ("Olivia Ruiz", "La femme chocolat", 2005),
    ("Jenifer", "Au soleil", 2002),
    ("Alizée", "J'en ai marre", 2003),
    ("Renan Luce", "La lettre", 2007),
    ("Grégoire", "Toi + Moi", 2008),
    ("BB Brunes", "Nico Teen Love", 2007),
    ("Superbus", "Butterfly", 2004),
    ("Yelle", "A cause des garçons", 2007),
    ("Diam's", "La boulette", 2004),
    ("Christophe Maé", "Il est où le bonheur", 2007),
    ("Corneille", "Parce qu'on vient de loin", 2002),
    ("David Guetta ft. Chris Willis", "The World Is Mine", 2004),
    ("Phoenix", "Too Young", 2001),
    ("Air", "Cherry Blossom Girl", 2004),
    ("Sébastien Tellier", "La Ritournelle", 2004),
    ("Cassius", "The Sound of Violence", 2002),
    ("Bénabar", "Le dîner", 2002),
    ("Raphaël", "Caravane", 2005),
    ("Camille", "Le festin", 2007),
    ("Nolwenn Leroy", "Cassé", 2003),
    ("Christophe Willem", "Septembre", 2007),
    ("Soprano", "La colombe", 2007),
    ("Sinik", "Le temps fait défaut", 2006),
    ("Booba", "Ouest Side", 2006),
    ("Disiz la Peste", "L'histoire de Robbie", 2002),
    ("Abd Al Malik", "Gibraltar", 2006),
    ("Rohff", "La vie du ghetto", 2000),
    ("Diam's", "Jeune demoiselle", 2006),
    ("Zazie", "Tout le monde", 2000),
    ("Thomas Dutronc", "Comme un manouche sans guitare", 2007),
    ("Garou", "Seul", 2000),
    ("Lorie", "Comeback", 2002),
    ("M (Matthieu Chedid)", "Machistador", 2003),
    ("Cali", "L'amour parfait", 2003),
    ("Tryo", "L'hymne de nos campagnes", 2003),
    ("Calogero", "Yallah", 2006),
    ("Florent Pagny", "Peut-être une chanson", 2006),
    ("Patrick Bruel", "Tu ne me verras plus", 2008),
    ("Yannick Noah", "Les lionnes", 2006),
    ("Phoenix", "1901", 2009),
    ("Bob Sinclar", "World Hold On", 2006),
    ("Grand Corps Malade", "Midi 20", 2006),
    ("Carla Bruni", "Quelqu'un m'a dit", 2002),
    ("K-Maro", "Femme Like U", 2004),
    ("MC Solaar", "Solaar pleure", 2003),
    ("IAM", "Nés sous la même étoile", 2003),
    ("Sinsemilia", "Tout le bonheur du monde", 2003),
    ("Lara Fabian", "Je suis malade", 2000),
    ("Amel Bent", "Mon combat", 2004),
    ("BB Brunes", "Coups et blessures", 2008),
    ("Katerine", "Louxor j'adore", 2001),
]

def build_playlist(api_key, songs, label):
    print(f"\n{'='*60}")
    print(f"Building {label} ({len(songs)} songs)")
    print('='*60)
    playlist = []
    for i, (artist, title, year) in enumerate(songs, 1):
        vid_id, yt_title = search_video(api_key, artist, title)
        status = f"→ {vid_id} | {yt_title}" if vid_id else "⚠ NOT FOUND"
        print(f"  [{i:02d}] {artist} — {title} ({year})  {status}")
        playlist.append({
            "id": vid_id or "MISSING",
            "artist": artist,
            "title": title,
            "year": year,
            "duration": 0,
            "director": "N/A",
        })
        time.sleep(0.15)  # avoid hitting rate limits
    return playlist

def main():
    api_key = load_api_key()

    pl_80s = build_playlist(api_key, FRANCE_80S, "France 80s")
    pl_00s = build_playlist(api_key, FRANCE_00S, "France 00s")

    # Save
    (ROOT / "playlist-france80s.json").write_text(
        json.dumps(pl_80s, ensure_ascii=False, indent=2)
    )
    (ROOT / "playlist-france00s.json").write_text(
        json.dumps(pl_00s, ensure_ascii=False, indent=2)
    )

    missing_80s = sum(1 for v in pl_80s if v["id"] == "MISSING")
    missing_00s = sum(1 for v in pl_00s if v["id"] == "MISSING")
    print(f"\nDone. France 80s: {missing_80s} missing. France 00s: {missing_00s} missing.")

if __name__ == "__main__":
    main()
