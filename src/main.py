"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

Run from the project root with either:
    python -m src.main
    python src/main.py
"""

try:
    from .recommender import load_songs, recommend_songs  # python -m src.main
except ImportError:
    from recommender import load_songs, recommend_songs  # python src/main.py


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Taste profiles: target values for the features used in scoring
    pop_happy = {
        "genre": "pop", "mood": "happy",
        "energy": 0.80, "valence": 0.80, "acousticness": 0.20,
    }
    chill_lofi = {
        "genre": "lofi", "mood": "chill",
        "energy": 0.40, "valence": 0.60, "acousticness": 0.80,
    }
    intense_rock = {
        "genre": "rock", "mood": "intense",
        "energy": 0.90, "valence": 0.45, "acousticness": 0.10,
    }
    user_prefs = pop_happy

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(f"\nProfile: {user_prefs['genre']} / {user_prefs['mood']}, "
          f"energy {user_prefs['energy']:.2f}, valence {user_prefs['valence']:.2f}, "
          f"acousticness {user_prefs['acousticness']:.2f}")
    print("\nTop recommendations")
    print("=" * 60)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} by {song['artist']}  [{song['genre']}, {song['mood']}]")
        print(f"   Score: {score:.2f} / 10")
        for reason in explanation.split(", "):
            print(f"     - {reason}")
        print()


if __name__ == "__main__":
    main()
