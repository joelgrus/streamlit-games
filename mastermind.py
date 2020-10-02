from typing import Tuple, NamedTuple, Union, List
import random
import dataclasses

import streamlit as st

from gamestate import persistent_game_state

DIGITS = ['0', '1', '2', '3', '4', '5']
K = 4


class Guess(NamedTuple):
    guess: str
    red: int
    white: int

    def show(self):
        st.write(f"{self.guess}, White {self.white}, Red {self.red}")


@dataclasses.dataclass
class GameState:
    secret_code: str
    game_number: int = 0
    previous_guesses: Tuple[Guess, ...] = ()
    game_over: bool = False

state = persistent_game_state(initial_state=GameState(''.join(random.choices(DIGITS, k=4))))

st.write("""MASTER MIND""")
st.write(f"I, the computer, will choose a secret {K}-digit number "
         "with all digits between 0 and 5. It is your job to "
         "guess the number. Each time you guess I will tell you a "
         "'white' score and a 'red' score. The 'white' score is the "
         "number of digits that are both in the number and in the correct position. "
         "The 'red' score is the number of digits that are in the number but are in "
         "the wrong position.")
st.write("For example, if my secret number were 1234, and you guessed 1442, "
         "you would get one 'white' (for the '1', which is in the correct place) "
         "and two 'red' (for the '2' and one of the '4's, which are correct but "
         "in the wrong place.")


if st.button("NEW GAME"):
    state.secret_code = ''.join(random.choices(DIGITS, k=4))
    state.game_number += 1
    state.previous_guesses = ()
    state.game_over = False


# Don't use Union types!
def parse_guess(guess: str) -> Union[str, List[str]]:
    if not all('0' <= c <= '5' for c in guess):
        return "I said **digits between 0 and 5**"
    if len(guess) != K:
        return f"I said **{K}** digits!"
    return list(guess)


if not state.game_over:
    raw_guess = st.text_input(f"please guess a {K} digit number, digits 0 to 5: ", key=state.game_number)
    guess = parse_guess(raw_guess) if raw_guess else ''

    if not guess and not state.previous_guesses:
        pass
    elif isinstance(guess, str):
        st.markdown(guess)
    else:        
        white = 0  # correct color + correct location
        red = 0    # correct color + wrong location
    
        for i in range(K):
            if guess[i] == state.secret_code[i]:
                white += 1
                guess[i] = -1  # sentinel for "already counted as white"
                        
        for i in range(K):
            if guess[i] == -1:
                continue
            try:
                idx = guess.index(state.secret_code[i])
                red += 1
                guess[idx] = -2 # sentinel for "already counted as red"
            except ValueError:
                continue

        state.previous_guesses += (Guess(raw_guess, red, white),)

        if white == K:
            state.game_over = True
            st.markdown("YOU GOT IT!")
            st.markdown(f"it only took you {len(state.previous_guesses)} guesses")

        for previous_guess in reversed(state.previous_guesses):
            previous_guess.show()


