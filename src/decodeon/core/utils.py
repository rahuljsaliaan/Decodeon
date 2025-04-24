import os
import json
import streamlit as st

from decodeon.types.enums import SessionStateEnum


def delete_file(file_path):
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


def string_to_json(input_str: str) -> dict:
    try:
        # Parse the string into a JSON object (dictionary in Python)
        print(input_str)
        json_data = json.loads(input_str)
        return json_data
    except json.JSONDecodeError:
        raise ValueError("Invalid json format")


def get_file_name_without_ext(path: str) -> str:
    return os.path.splitext(os.path.basename(path))[0]
