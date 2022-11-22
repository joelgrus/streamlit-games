from typing import TypeVar

import streamlit as st

StateT = TypeVar('StateT')

def persistent_game_state(initial_state: StateT) -> StateT:
    if '_gamestate' not in st.session_state:
        st.session_state['_gamestate'] = initial_state
    return st.session_state['_gamestate']
