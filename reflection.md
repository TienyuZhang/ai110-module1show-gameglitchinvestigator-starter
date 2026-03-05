# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

---
1) Difficulty settings for “Hard” and “Normal” are reversed. 
The difficulty configuration for Hard and Normal appears to be incorrect. Currently, Normal is more difficult than Hard:
Normal: Range 1–100, Attempts allowed: 8
Hard: Range 1–50, Attempts allowed: 5
Because the range for Normal is larger, it is actually harder than Hard.
Suggestion: Swap the range settings so that Hard uses 1–100 and Normal uses 1–50 (or otherwise adjust them so Hard is more difficult than Normal).

2) The hints were backwards. 
The hint messages appear to be displayed incorrectly.
When the guessed number is lower than the secret number, the game should display “Go higher”, but it currently shows “Go LOWER.”
When the guessed number is higher than the secret number, the game should display “Go lower”, but it currently shows “Go HIGHER.”
The hint logic appears to be reversed.

3) Attempt counter starts with the wrong value.
The Attempts counter is initialized at 1 instead of 0 at the start of the game.
As a result, the Attempts left value is always one less than expected, and the game ends and displays the result one attempt earlier than it should.
Expected behavior: The Attempts counter should start at 0 when the game begins.

4) 4. Secret number may be generated outside the selected range.
The secret number is sometimes generated outside the selected difficulty range.
For example, when selecting a difficulty with Range 1–20 or Range 1–50, the secret number is still sometimes generated from 1–100.
Expected behavior: The secret number should be generated within the selected range for the chosen difficulty level.

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
