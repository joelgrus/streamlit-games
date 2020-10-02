from typing import TypeVar
import dataclasses

import streamlit as st

StateT = TypeVar('StateT')

def persistent_game_state(initial_state: StateT) -> StateT:
    session_id = st.report_thread.get_report_ctx().session_id
    session = st.server.server.Server.get_current()._get_session_info(session_id).session
    if not hasattr(session, '_gamestate'):
        setattr(session, '_gamestate', initial_state)
    return session._gamestate
