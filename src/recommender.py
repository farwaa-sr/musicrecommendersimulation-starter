import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv into a list of dicts, converting id to int and numeric features to float."""
    int_fields = ("id",)
    float_fields = ("energy", "tempo_bpm", "valence", "danceability", "acousticness")

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for field in int_fields:
                row[field] = int(row[field])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song out of 10 against the user's preferences and return (score, reasons)."""
    score = 0.0
    reasons: List[str] = []

    # Numeric features: reward closeness to the target, not higher or lower values.
    numeric_rules = (
        ("energy", "energy", 3.5),
        ("valence", "valence", 2.5),
        ("acousticness", "acousticness", 1.0),
    )
    for pref_key, song_key, max_points in numeric_rules:
        if pref_key not in user_prefs:
            continue
        gap = abs(song[song_key] - user_prefs[pref_key])
        points = max_points * (1 - gap)
        score += points
        reasons.append(f"{song_key} gap {gap:.2f} (+{points:.2f})")

    # Categorical features: exact match bonus.
    for pref_key, song_key, bonus in (("mood", "mood", 2.0), ("genre", "genre", 1.0)):
        if song[song_key] == user_prefs.get(pref_key):
            score += bonus
            reasons.append(f"{song_key} match (+{bonus:.1f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort best-first (ties: closer energy, then lower id), and return the top k."""
    scored = [
        (song, score, ", ".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]

    # Highest score first; ties go to the smaller energy gap, then the lower id.
    target_energy = user_prefs.get("energy", 0.0)
    ranked = sorted(
        scored,
        key=lambda item: (-item[1], abs(item[0]["energy"] - target_energy), item[0]["id"]),
    )
    return ranked[:k]
