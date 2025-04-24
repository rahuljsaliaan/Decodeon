import os
import streamlit as st

from decodeon.types.enums import SessionStateEnum


def delete_file(file_path):
    """Delete a file from the filesystem."""

    # Use the relative path from the root of the project
    full_path = os.path.join(
        os.getcwd(), file_path
    )  # Ensure it’s relative to the root directory
    try:
        if os.path.exists(full_path):
            os.remove(full_path)
            st.session_state[SessionStateEnum.csv_path] = None
    except Exception as e:
        print(f"Error deleting file {e}")


def get_file_name_without_ext(path: str) -> str:
    """Get the file name without its extension."""

    return os.path.splitext(os.path.basename(path))[0]
