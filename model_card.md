# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

The recommender compares every song in the catalog to a "taste profile" and gives each one a score out of 10. A profile says what the listener wants: a favorite genre, a favorite mood, and target levels for energy, valence (how happy or dark a song sounds), and acousticness (how acoustic versus electronic it is).

For the three number-based traits, the model rewards songs that are close to the target, not songs that are simply higher or lower. If a listener wants medium-low energy, a very calm song and a very intense song both lose points, and the song nearest the target gets the most. Energy is worth up to 3.5 points, valence up to 2.5, and acousticness up to 1. Mood and genre are all-or-nothing: a matching mood adds 2 points and a matching genre adds 1. I weighted mood above genre because mood describes what the listener wants right now, and genre labels are sparse in my small catalog.

Once every song has a score, the model sorts them from highest to lowest (ties go to the song closer on energy) and shows the top five. Each result also lists the reasons behind its score, such as "mood match (+2.0)", so the listener can see why it was picked.

Changes from the starter: the starter only suggested genre, mood and energy. I added valence and acousticness, dropped tempo and danceability because they mostly repeat what energy already says, and made mood count for more than genre. The whole thing runs from the command line (`python -m src.main`).

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
