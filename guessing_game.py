import streamlit as st
import random
import dataclasses

from gamestate import persistent_game_state

HI = 1000

@dataclasses.dataclass
class GameState:
    number: int
    num_guesses: int = 0
    game_number: int = 0
    game_over: bool = False

state = persistent_game_state(initial_state=GameState(random.randint(1, 1000)))

if st.button("NEW GAME"):
    state.number = random.randint(1, HI)
    state.num_guesses = 0
    state.game_number += 1
    state.game_over = False

if not state.game_over:
    guess = st.text_input(f"guess a number between 1 and {HI}", key=state.game_number)

    if guess:

        try:
            guess = int(guess)
            state.num_guesses += 1

            if guess < state.number:
                st.write(f"{guess} is too low")
            elif guess > state.number:
                st.write(f"{guess} is too high")
            else:
                st.write(f"you win, it only took you {state.num_guesses} tries")
                state.game_over = True

        except ValueError:
            st.write("please guess a *number*")
