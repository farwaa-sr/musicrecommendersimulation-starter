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

The biggest weakness I found is that the exact-match mood and genre bonuses can outweigh how a song actually sounds. With my original weights, the "high energy but sad" test profile (energy 0.9, valence 0.2) ranked Rainy Window Blues first even though its energy is 0.38, because matching "sad" and "blues" added 3 of the 10 points; Iron Cathedral, which is far closer on energy and valence, came second only because its labels did not match. The same thing happened for a "loud and fully acoustic" profile, where a song with an energy gap of 0.62 won on labels alone. This is made worse by the small catalog: 14 of its 18 genres and 14 of its 18 moods appear on only one song, so a listener's favorite label usually matches at most one track, and a near-synonym such as "aggressive" versus "intense" earns nothing. Doubling the energy weight and halving the genre weight fixed both cases, but it made energy over half of every score, so the real fix is probably softer label matching rather than just shifting weights. The energy gap itself is not biased against any group of listeners, since the catalog is fairly balanced (8 low, 7 mid and 8 high energy songs).

---

## 7. Evaluation  

### Profiles I tested
I ran seven listener profiles against the 23-song catalog and looked at the top five songs for each (full outputs are in the README). All results below use my original weights; I describe what happened when I changed them at the end.

- **High-Energy Pop (Pop):** loves pop, happy, lively, bright-sounding songs.
- **Chill Lofi (Lofi):** loves lofi, chill, calm and acoustic songs.
- **Deep Intense Rock (Rock):** loves rock, intense, very loud songs with a darker feel.
- **Conflicting: high energy but sad (Sad):** wants blues and sad moods but also very high energy, which rarely go together.
- **Genre not in catalog (K-pop):** wants K-pop, which has no songs at all, with a happy, high-energy feel.
- **Impossible: loud and fully acoustic (Impossible):** wants very high energy and almost entirely acoustic sound, a combination no song has.
- **Neutral (Neutral):** every number set to the middle, jazz and relaxed.

I was checking two things: do ordinary listeners get the songs I would pick for them, and what happens when a listener asks for something the catalog cannot give.

### What surprised me
1. **"Gym Hero" kept turning up.** It showed up for Pop, Rock, K-pop and Impossible. In plain terms: Gym Hero is a pop song that is very energetic and fairly cheerful. A "happy pop" listener wants exactly that mix of lively and upbeat, and the system checks the song's numbers and its genre label, not whether it is actually a "happy" song. Its mood is "intense", so it loses the points for mood, but it is so close on energy, cheerfulness and genre that it still lands third. It is not a bug, but it is not what a happy-pop listener would call a perfect match either. The same song shows up for rock fans because it is just as loud and "intense" as a rock song.
2. **Labels can beat the sound.** For the Sad profile, a quiet blues song (Rainy Window Blues) beat louder songs that matched the energy the listener asked for, just because its mood and genre words matched.
3. **A missing genre barely hurt.** The K-pop profile got nearly the same results as Pop, because the system fell back on mood and the numbers, which is a good sign.
4. **The Impossible profile hid its problem.** The top song scored 7.61 out of 10 even though nothing in the catalog fits, so a weak match looks like a decent one.
5. **The Neutral profile gave a one-song answer.** Coffee Shop Stories (jazz, relaxed) scored far above everything else, and the other four places were separated by less than 0.3 points, so their order is close to arbitrary.

### Comparing every pair of profiles
- **Pop vs Lofi:** no songs in common. Pop gets lively, bright songs; Lofi gets slow, acoustic, calm ones. Makes sense, since they are almost opposites on energy and acousticness.
- **Pop vs Rock:** they share Gym Hero and Concrete Crown. Both want loud songs, but Pop gets cheerful ones and Rock gets darker, "intense" ones; Gym Hero is the bridge because it is loud and bright.
- **Pop vs Sad:** only Concrete Crown in common. Both want high energy, but Sad asks for a gloomy feel, so Pop gets happy songs and Sad gets blues and metal. This shows the cheerfulness setting does real work.
- **Pop vs K-pop:** almost identical lists (same top two and the same five songs apart from order). The only difference is that K-pop has no genre bonus to give, so Gym Hero drops from third to fourth. Makes sense.
- **Pop vs Impossible:** only Gym Hero in common. Impossible's acoustic request pulls a folk song to first place, while Pop's lively request does not.
- **Pop vs Neutral:** nothing in common. Neutral wants mid-level everything, so it gets jazz, country and R&B, while Pop gets loud pop and dance songs.
- **Lofi vs Rock:** completely different lists, the cleanest test. One wants quiet and acoustic, the other loud and electric, and the songs flip accordingly.
- **Lofi vs Sad:** no overlap. Lofi gets calm, mellow songs; Sad gets high-energy dark ones. The system respects the energy request.
- **Lofi vs K-pop:** no overlap. Calm and acoustic against loud and bright, as expected.
- **Lofi vs Impossible:** they share Wildflower Road (a folk song). It is Lofi's fifth pick on its numbers, but Impossible's first pick on its labels (folk, dreamy), so the same song ranks high for two different reasons.
- **Lofi vs Neutral:** only Midnight Coding in common. It sits at medium-low energy, so it satisfies a calm listener and a middle-of-the-road one.
- **Rock vs Sad:** four of five songs shared (Storm Runner, Iron Cathedral, Night Drive Loop, Concrete Crown). Both want loud songs, so that overlap is right. The difference is the first place: Rock's is a rock song, Sad's is a quiet blues song, which came from labels.
- **Rock vs K-pop:** Gym Hero and Concrete Crown in common. Rock gets darker, harder songs and K-pop gets brighter ones.
- **Rock vs Impossible:** four songs shared, because both want very loud songs. The difference is that Impossible's acoustic request pushes a gentle folk song to the top.
- **Rock vs Neutral:** nothing in common. Very loud against middle-of-everything.
- **Sad vs K-pop:** only Concrete Crown in common. Same loudness, opposite mood, so one list is gloomy and the other cheerful.
- **Sad vs Impossible:** three songs shared (Storm Runner, Iron Cathedral, Night Drive Loop). Both ask for something the catalog cannot fully offer, and in both a song winning on labels beat songs that fit the loudness better.
- **Sad vs Neutral:** nothing in common. Loud and gloomy against middle of the road.
- **K-pop vs Impossible:** only Gym Hero in common. K-pop is bright and loud; Impossible wants loud and acoustic.
- **K-pop vs Neutral:** nothing in common. Bright and loud against a middle-ground jazz listener.
- **Impossible vs Neutral:** nothing in common. One asks for the extremes, the other for the exact middle.

### Does the output make sense?
For the three realistic profiles, yes: the top pick is what I would choose by hand (Sunrise City, Library Rain, Storm Runner). The profiles that disagree the most (Lofi against Rock) share no songs, which is what I hoped to see. Where it breaks is the strange requests, where the system always gives a confident-looking answer.

### Weight experiment
I doubled the energy weight and halved the genre weight. Ordinary profiles barely changed, but the Sad profile moved Rainy Window Blues from first to fourth and the Impossible profile moved Wildflower Road from first to fifth, which looked more accurate. The cost is that energy then makes up over half of every score.

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
