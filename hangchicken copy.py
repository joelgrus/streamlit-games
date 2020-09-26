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
    serial_number: int
    word: str
    guessed: Tuple[str, ...] = ()
    step: int = 0

@st.cache(allow_output_mutation=True)
def persistent_game_state():
    return GameState(0, random.choice(get_words()))

state = persistent_game_state()

if st.button("new game"):
    state.guessed = ()
    state.step = 0
    state.serial_number += 1
    state.word = random.choice(get_words())


chicken = st.empty()
letters = st.empty()
guessed = st.empty()
message = st.empty()
text_input = st.empty()

st.write(state)

guess = text_input.text_input("guess a letter", max_chars=1, key=(state.serial_number, len(state.guessed)))

if state.step == 0 and not state.guessed and not guess:
    message.write("welcome to hangchicken")
elif len(guess) != 1:
    message.write("just one letter!")
elif guess < 'a' or guess > 'z':
    message.write("a lowercase letter!")
elif guess in state.guessed:
    message.write(f"you already guessed **{guess}**")
elif guess not in state.word:
    message.write(f"the word has no **{guess}**")
    state.step += 1
    state.guessed += (guess,)
else: 
    message.write("good guess")
    state.guessed += (guess,)

if state.step == len(STEPS) - 1:
    message.markdown(f"you lose, the word was **{state.word}**")
elif all(c in state.guessed for c in state.word):
    message.markdown(f"**YOU WIN**")

chicken.text(STEPS[state.step])
# Show the word
chars = [c if c in state.guessed else "_" for c in state.word]
letters.text(" ".join(chars))

# Show the guessed letters
guessed.text(f'guessed: {" ".join(state.guessed)}')
