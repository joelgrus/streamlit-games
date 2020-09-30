from typing import List, Tuple
from string import ascii_lowercase
import types
import random
import dataclasses

import streamlit as st


PROTOTYPE = """
 ┏━━┑
 ┃  O>
 ┃>╦╧╦<
 ┃ ╠═╣
 ┃ ╨ ╨
 ┻━━━━
"""


STEPS = [
"""
 ┏━━┑
 ┃
 ┃
 ┃
 ┃
 ┻━━━━
""",
"""
 ┏━━┑
 ┃  O
 ┃
 ┃
 ┃
 ┻━━━━
""",
"""
 ┏━━┑
 ┃  O>
 ┃
 ┃
 ┃
 ┻━━━━
""",
"""
 ┏━━┑
 ┃  O>
 ┃ ╔╧╗
 ┃ ╚═╝
 ┃
 ┻━━━━
""",
"""
 ┏━━┑
 ┃  O>
 ┃>╦╧╗
 ┃ ╚═╝
 ┃
 ┻━━━━
""",
"""
 ┏━━┑
 ┃  O>
 ┃>╦╧╦<
 ┃ ╚═╝
 ┃
 ┻━━━━
""",
"""
 ┏━━┑
 ┃  O>
 ┃>╦╧╦<
 ┃ ╠═╝
 ┃ ╨
 ┻━━━━
""",
"""
 ┏━━┑
 ┃  O>
 ┃>╦╧╦<
 ┃ ╠═╣
 ┃ ╨ ╨
 ┻━━━━
"""
]

MIN_LENGTH = 3
MAX_LENGTH = 8

@st.cache
def get_words() -> List[str]:
    with open('words1000.txt') as f:
        words = [line.strip() for line in f]

    words = [w for w in words if MIN_LENGTH <= len(w) <= MAX_LENGTH]
    words = [w for w in words if all('a' <= c <= 'z' for c in w)]

    return words

@dataclasses.dataclass
class GameState:
    game_number: int
    word: str
    guessed: Tuple[str, ...] = ()
    step: int = 0
    game_over: bool = False


def persistent_game_state():
    session_id = st.report_thread.get_report_ctx().session_id
    session = st.server.server.Server.get_current()._get_session_info(session_id).session
    if not hasattr(session, '_gamestate'):
        setattr(session, '_gamestate', GameState(0, random.choice(get_words())))


state = persistent_game_state()

if st.button("new game"):
    state.guessed = ()
    state.step = 0
    state.game_number += 1
    state.word = random.choice(get_words())
    state.game_over = False

if not state.game_over:
    guess = st.text_input("guess a letter", max_chars=1, key=state.game_number)

    if not guess:
        st.write("please guess")
    elif guess < 'a' or guess > 'z':
        st.write("please guess a lowercase letter!")
    elif guess in state.guessed:
        st.write(f"you already guessed **{guess}**")
    elif guess not in state.word:
        st.write(f"the word has no **{guess}**")
        state.step += 1
        state.guessed += (guess,)
    else: 
        st.write("good guess")
        state.guessed += (guess,)

if state.step == len(STEPS) - 1:
    st.markdown(f"you lose, the word was **{state.word}**")
    state.game_over = True
elif all(c in state.guessed for c in state.word):
    st.markdown(f"**YOU WIN**")
    state.game_over = True

# Show the chicken
st.text(STEPS[state.step])

# Show the word
chars = [c if c in state.guessed else "_" for c in state.word]
st.text(" ".join(chars))

# Show the guessed letters
st.text(f'guessed: {" ".join(state.guessed)}')
