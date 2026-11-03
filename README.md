# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world recommenders like Spotify or YouTube work in two stages. First, they score each item by predicting how relevant it is to a specific user, using signals such as what the user has played, skipped, or saved, along with the item's own features (genre, mood, energy, tempo). Then they rank all of those scored items, apply extra rules like removing songs already heard or keeping the list varied, and show only the top few. My version is a much smaller, content-based take on that idea: instead of learning from listening history, it compares each song's attributes directly against a user's stated taste. I score every song on how close it is to the user's target rather than rewarding higher or lower values, so a user who wants energy 0.4 is not handed a 0.9 song. I prioritize energy first, then valence, then mood, with acousticness and genre as smaller nudges, because energy and valence capture how a song feels and mood captures what the listener wants right now. I chose to weight mood above genre because genre labels are too sparse in my small dataset to carry much weight. After scoring, I rank songs from highest to lowest and return the top results.

### Features used

**`Song`** (one row of `data/songs.csv`)

| Feature | Type | Used in scoring? |
|---|---|---|
| `id`, `title`, `artist` | int / str | No, identification and display only |
| `genre` | str | Yes, exact match bonus (weight 0.10) |
| `mood` | str | Yes, exact match bonus (weight 0.20) |
| `energy` | float 0-1 | Yes, closeness to target (weight 0.35) |
| `valence` | float 0-1 | Yes, closeness to target (weight 0.25) |
| `acousticness` | float 0-1 | Yes, closeness to target (weight 0.10) |
| `tempo_bpm` | float | No, mostly redundant with energy |
| `danceability` | float 0-1 | No, mostly redundant with energy |

**`UserProfile`** (the listener's taste)

| Feature | Type | Compared against |
|---|---|---|
| `favorite_genre` | str | `Song.genre` |
| `favorite_mood` | str | `Song.mood` |
| `target_energy` | float 0-1 | `Song.energy` |
| `target_valence` | float 0-1 | `Song.valence` (to be added to the starter profile) |
| `likes_acoustic` | bool | `Song.acousticness`, mapped to a target of about 0.8 if true and 0.2 if false |

Scoring rule for each song:

```
score = 0.35*(1 - |energy - target_energy|)
      + 0.25*(1 - |valence - target_valence|)
      + 0.20*(mood == favorite_mood)
      + 0.10*(1 - |acousticness - acoustic_target|)
      + 0.10*(genre == favorite_genre)
```

Ranking rule: sort all songs by score (highest first), break ties by smaller energy distance and then lower `id`, and return the top K.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



