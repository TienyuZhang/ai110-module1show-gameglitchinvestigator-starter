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

4) Secret number may be generated outside the selected range.
The secret number is sometimes generated outside the selected difficulty range.
For example, when selecting a difficulty with Range 1–20 or Range 1–50, the secret number is still sometimes generated from 1–100.
Expected behavior: The secret number should be generated within the selected range for the chosen difficulty level.

5) The result of the comparasion between the guess number and the secrect number are wrong sometimes.
The bug was in app.py: On even-numbered attempts, secret is cast to a str. Then in check_guess, comparing int > str raises a TypeError, which falls into the except block that does string comparison — so "12" > "5" is False lexicographically (because "1" < "5"), returning "Too Low" even though 12 > 5. 
Expected behavior: Always pass secret as int so check_guess uses numeric comparison.

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---
I used Claude Code.

Claude successfully refactored logic into logic_utils.py. It correctly identified the logic functions in app.py, moved them into logic_utils.py, removed the original definitions from app.py, and added the necessary import statements. I verified the result by checking both logic_utils.py and app.py to confirm that all logic functions were moved correctly. I also ran the application to ensure the logic functions still worked as expected.

When I asked the AI to add tests for the fixed bug related to the Attempt counter, it used score differences to check whether the Attempt counter was working correctly. This approach was incorrect because it could not directly verify the initial value of the Attempt counter or monitor whether the Attempt counter was updated correctly during gameplay. After I clarified the type of tests I needed, the AI eventually generated tests that directly validated the Attempt counter’s initialization and updates during the game.


## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---
To determine whether a bug was fixed, I checked whether the program behaved correctly in situations where the bug previously occurred. I reviewed the relevant code changes and then ran the application to verify that the feature now worked as expected without introducing new issues.

One test I ran about the hit message:
When the guess number is above secret number — player should be told to go LOWER, so I assert "Go LOWER" in message,and  "Go HIGHER" not in message;
When Guess number is below secret number — player should be told to go HIGHER, so I assert "Go  HIGHER" in message,and  "Go LOWER" not in message.

AI helped me generate test cases using pytest. It suggested test structures and helped write the basic test functions. Although sometimes the first version of the test was incorrect, it still helped me understand how to structure tests. 


## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---
Streamlit reruns the entire script from top to bottom on every user interaction — every button click, every selectbox change, every keystroke in a text input. This means random.randint() would be called again on every single interaction.
There are two scenarios in the original app will change the secret number:
1) Page refresh — refreshing the browser clears st.session_state entirely, so a brand new secret is generated. This is expected behavior.
2) The "New Game" button bug — the new_game handler explicitly called random.randint(1, 100) (the hardcoded range bug we fixed). But it also didn't reset st.session_state.status back to "playing", so after winning/losing, clicking "New Game" generated a new secret but then st.stop() immediately halted the script due to the old "won"/"lost" status — effectively trapping the player and silently changing the secret with no way to play.

Imagine a whiteboard that gets erased and redrawn every time someone in the room raises their hand.
That's Streamlit. Every time a user interacts with anything — clicks a button, types in a box, changes a dropdown — Streamlit erases everything and reruns the entire Python script from line 1. The screen you see is always the result of the most recent full run.
This means any regular variable like secret = random.randint(1, 20) gets thrown away and recalculated every single rerun. The number would change constantly. st.session_state is a sticky notepad on the side of the whiteboard — it survives the erase. Values stored there persist across reruns for as long as the browser tab is open.

Two changes together fixed it:
1) The if "secret" not in st.session_state guard — ensures the secret is only generated once per session.
2) Fixing the "New Game" button — the original hardcoded random.randint(1, 100) was replaced with random.randint(low, high), so when a new game intentionally starts, the secret is at least generated within the correct difficulty range.
Without 1), the secret would change on every interaction. Without 2), the secret would be stable but potentially outside the selected difficulty's range.


## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One habit I want to keep is committing changes to Git frequently. Whenever I complete a small feature or make several important changes, I create a commit to save my progress. This helps me keep track of what I changed and makes it easier to revert to a previous version if something breaks. It also makes the development process more organized and safer.

Next time, I would review my code more carefully before asking AI for help. Sometimes I asked AI too quickly without fully understanding the problem myself. If I first analyze the code and identify the exact issue, I can give AI a clearer prompt and get more useful suggestions.

This project showed me that AI is a powerful tool that can help solve many coding problems when given clear instructions. However, AI can still make mistakes, even when the request is clear. Because of this, developers must carefully review AI-generated code and make the final decisions themselves. AI should be treated as a helpful assistant, not as the person responsible for the project.
