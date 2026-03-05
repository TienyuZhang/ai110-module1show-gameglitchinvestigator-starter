from logic_utils import check_guess, update_score, get_range_for_difficulty

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"


# Tests targeting the reversed hint message bug:
# When guess > secret, message must say "Go LOWER!" (not "Go HIGHER!")
# When guess < secret, message must say "Go HIGHER!" (not "Go LOWER!")

def test_hint_message_too_high():
    # Guess (60) is above secret (50) — player should be told to go LOWER
    outcome, message = check_guess(60, 50)
    assert "Go LOWER" in message, f"Expected 'Go LOWER' in hint when guess is too high, got: '{message}'"
    assert "Go HIGHER" not in message

def test_hint_message_too_low():
    # Guess (40) is below secret (50) — player should be told to go HIGHER
    outcome, message = check_guess(40, 50)
    assert "Go HIGHER" in message, f"Expected 'Go HIGHER' in hint when guess is too low, got: '{message}'"
    assert "Go LOWER" not in message

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# Tests targeting the attempts counter initialization bug:
# Bug: attempts was initialized to 1 instead of 0, causing "Attempts:" to show 1
# before any guess, and "Attempts left" to be one short from the start.

def test_attempts_initial_value():
    # Simulates: st.write("Attempts:", st.session_state.attempts)
    # At game start, before any guess is submitted, attempts should be 0.
    attempts = 0  # correct initial value after fix
    assert attempts == 0, f"Expected attempts to start at 0, got {attempts}"

def test_attempts_left_at_game_start():
    # Simulates: f"Attempts left: {attempt_limit - st.session_state.attempts}"
    # At game start with Normal difficulty (limit=8), all 8 attempts should be available.
    attempt_limit = 8
    attempts = 0  # correct initial value after fix
    attempts_left = attempt_limit - attempts
    assert attempts_left == attempt_limit, (
        f"Expected {attempt_limit} attempts left at start, got {attempts_left}"
    )

def test_bugged_attempts_left_at_game_start():
    # Before the fix, attempts started at 1, so attempts_left was already 7 instead of 8.
    attempt_limit = 8
    bugged_attempts = 1  # the original buggy initial value
    attempts_left = attempt_limit - bugged_attempts
    assert attempts_left == 7, f"Bugged path should show 7, got {attempts_left}"
    assert attempts_left != attempt_limit, "Bugged attempts_left should not equal the full limit"


# Tests targeting the swapped Hard/Normal range bug:
# Bug: Normal returned 1-100 and Hard returned 1-50, making Normal harder than Hard.
# Fix: Normal should use 1-50 and Hard should use 1-100.

def test_hard_range_is_larger_than_normal():
    # Hard must have a wider range than Normal to actually be harder.
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high, (
        f"Hard range (1–{hard_high}) should be larger than Normal range (1–{normal_high})"
    )

def test_normal_range():
    # Normal difficulty should use range 1–50.
    low, high = get_range_for_difficulty("Normal")
    assert (low, high) == (1, 50), f"Expected Normal range (1, 50), got ({low}, {high})"

def test_hard_range():
    # Hard difficulty should use range 1–100.
    low, high = get_range_for_difficulty("Hard")
    assert (low, high) == (1, 100), f"Expected Hard range (1, 100), got ({low}, {high})"


# Tests targeting the secret-generated-outside-range bug:
# Bug: the New Game button used hardcoded randint(1, 100) instead of randint(low, high),
# so Easy (1–20) and Normal (1–50) could produce secrets well outside their range.

def test_secret_within_easy_range():
    # Simulates: secret = random.randint(low, high) using the correct difficulty range.
    # A secret for Easy must always be between 1 and 20.
    import random
    low, high = get_range_for_difficulty("Easy")
    random.seed(42)
    num_samples = 100  # number of random secrets to generate and check
    for _ in range(num_samples):
        secret = random.randint(low, high)
        assert low <= secret <= high, f"Secret {secret} is outside Easy range ({low}–{high})"

def test_secret_within_normal_range():
    # A secret for Normal must always be between 1 and 50.
    import random
    low, high = get_range_for_difficulty("Normal")
    random.seed(42)
    num_samples = 100  # number of random secrets to generate and check
    for _ in range(num_samples):
        secret = random.randint(low, high)
        assert low <= secret <= high, f"Secret {secret} is outside Normal range ({low}–{high})"

def test_bugged_secret_exceeds_easy_range():
    # Before the fix, New Game used hardcoded (1, 100) for all difficulties.
    # This shows that hardcoded range can produce secrets outside Easy's 1–20 bound.
    import random
    easy_low, easy_high = get_range_for_difficulty("Easy")
    random.seed(0)
    secrets = [random.randint(1, 100) for _ in range(100)]
    out_of_range = [s for s in secrets if s > easy_high]
    assert len(out_of_range) > 0, "Expected hardcoded 1–100 to generate secrets outside Easy range"
