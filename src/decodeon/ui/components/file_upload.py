import os
import time
from datetime import datetime
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from decodeon.types.enums import SessionStateEnum, DefaultFoldersEnum


def upload_files(csv_file: UploadedFile):
    """Upload a file to the server and save it in a specific directory."""

    try:
        # Create the file path
        current_date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        file_path_str = f"{csv_file.name or "default"}-{current_date_time}.csv"
        temp_file_path = os.path.join(DefaultFoldersEnum.data.value, file_path_str)

        os.makedirs(
            os.path.join(os.getcwd(), DefaultFoldersEnum.data.value), exist_ok=True
        )
        with open(temp_file_path, "wb") as f:
            f.write(csv_file.getvalue())

        st.session_state[SessionStateEnum.csv_path] = (
            f"{DefaultFoldersEnum.data.value}/{file_path_str}"
        )

        success_message = st.success(f"File uploaded successfully!")
        time.sleep(3)
        success_message.empty()

    except Exception as e:
        error_message = st.error(f"Error in file uploading: {e}")
        time.sleep(3)
        # error_message.empty()
        # st.rerun()
