import streamlit as st

from decodeon.types.enums import SessionStateEnum


def init_query_input():
    placeholder = (
        "Ask about the CSV file's contents, processing, or any code-related questions (Python)."
        if st.session_state.get(SessionStateEnum.csv_path)
        else "Ask any code-related questions (Python)."
    )

    # Get current action state
    action_in_progress = st.session_state.get(
        SessionStateEnum.action_in_progress, False
    )

    st.file_uploader

    # Disable input if action is in progress
    return st.chat_input(
        max_chars=1000,
        accept_file=True,
        file_type="csv",
        placeholder=placeholder,
        disabled=action_in_progress,
    )
