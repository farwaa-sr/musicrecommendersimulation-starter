"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Taste profiles: target values for the features used in scoring
    chill_lofi = {
        "genre": "lofi", "mood": "chill",
        "energy": 0.40, "valence": 0.60, "acousticness": 0.80,
    }
    intense_rock = {
        "genre": "rock", "mood": "intense",
        "energy": 0.90, "valence": 0.45, "acousticness": 0.10,
    }
    user_prefs = chill_lofi

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
