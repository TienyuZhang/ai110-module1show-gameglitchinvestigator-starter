import random
import streamlit as st
from logic_utils import check_guess, parse_guess, get_range_for_difficulty, update_score



st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    # FIXME: Logic breaks here — attempts should start at 0, not 1
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []  # each entry: {"attempt", "guess", "outcome", "temp"}

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    # FIX: Reset all session state so the player can actually start a new game.
    # Previously only attempts and secret were reset; status/score/history were left
    # over from the previous game, causing st.stop() to fire immediately after a win/loss.
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append({"attempt": st.session_state.attempts, "guess": raw_guess, "outcome": "Invalid", "temp": ""})
        st.error(err)
    else:
        # FIX: Always pass secret as int so check_guess uses numeric comparison.
        # Bug was here: secret was cast to str on even attempts, causing
        # check_guess to fall back to lexicographic string comparison
        # (e.g. "12" < "5"), which produced wrong Too High / Too Low results.
        secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        # Hot/Cold proximity indicator
        distance = abs(guess_int - st.session_state.secret)
        range_size = high - low
        proximity = distance / range_size if range_size > 0 else 1.0
        if proximity < 0.05:
            temp_label = "🔥🔥 Scorching!"
        elif proximity < 0.15:
            temp_label = "🔥 Hot!"
        elif proximity < 0.30:
            temp_label = "😐 Warm"
        elif proximity < 0.55:
            temp_label = "❄️ Cold"
        else:
            temp_label = "❄️❄️ Freezing!"

        st.session_state.history.append({"attempt": st.session_state.attempts, "guess": guess_int, "outcome": outcome, "temp": temp_label})

        if show_hint:
            hint_text = f"{message} &nbsp; {temp_label}"
            if outcome == "Too High":
                st.error(hint_text)
            elif outcome == "Too Low":
                st.info(hint_text)
            elif outcome == "Win":
                st.success(hint_text)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

st.divider()

# Session summary table
valid_history = [h for h in st.session_state.history if h.get("outcome") != "Invalid"]
if valid_history:
    st.subheader("Session Summary")
    st.caption("Hot/Cold shows how close your guess was to the secret: 🔥🔥 Scorching (≤5%) → 🔥 Hot (≤15%) → 😐 Warm (≤30%) → ❄️ Cold (≤55%) → ❄️❄️ Freezing (>55%) of the number range.")
    import pandas as pd
    st.table(pd.DataFrame([
        {"#": h["attempt"], "Guess": h["guess"], "Result": h["outcome"], "Hot/Cold": h["temp"]}
        for h in valid_history
    ]))
    st.caption(f"Current score: **{st.session_state.score}**")

st.caption("Built by an AI that claims this code is production-ready.")
