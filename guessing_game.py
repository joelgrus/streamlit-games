import streamlit as st
import random
import dataclasses

HI = 1000

@dataclasses.dataclass
class GameState:
    number: int
    num_guesses: int = 0
    game_number: int = 0
    game_over: bool = False


def persistent_game_state() -> GameState:
    session_id = st.report_thread.get_report_ctx().session_id
    session = st.server.server.Server.get_current()._get_session_info(session_id).session
    if not hasattr(session, '_gamestate'):
        setattr(session, '_gamestate', GameState(random.randint(1, 1000)))
    return session._gamestate

state = persistent_game_state()

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
