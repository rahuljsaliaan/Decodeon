import streamlit as st
import time
from langchain_core.output_parsers import StrOutputParser

from decodeon.types.enums import SessionStateEnum
from decodeon.ui.components import (
    init_page_config,
    init_query_input,
    upload_files,
    init_chat_history,
    new_chat,
)
from decodeon.agents.router_agent import create_router_agent
from decodeon.models import ChatHistoryList
from decodeon.core.utils import get_file_name_without_ext

# Initialize the output parser and agent
parser = StrOutputParser()
# Initialize the agent executor
agent_executor = create_router_agent()


def app():
    """The ui entry point for the Decodeon application."""

    # Set Streamlit page configuration
    init_page_config()

    # App title
    st.title("Decodeon: LangChain-Powered Code Interpreter and csv file analyzer")

    # Display current working file if uploaded
    current_working_file = st.session_state.get(SessionStateEnum.csv_path)
    if current_working_file:
        st.markdown(
            f"📄 **Current working file:** `{get_file_name_without_ext(current_working_file)}`"
        )

    # Get user query input
    user_query = init_query_input()

    # Initialize or load previous chat history
    init_chat_history()

    # Handle user query
    if user_query:
        with st.spinner("Generating response..."):
            try:
                st.session_state[SessionStateEnum.action_in_progress] = True
                chat_history: ChatHistoryList = st.session_state[
                    SessionStateEnum.chat_history
                ]

                # Handle file upload if provided
                files = user_query.files
                if len(files) > 0:
                    csv_file = files[0]
                    upload_files(csv_file)

                # Generate response using agent
                result = agent_executor.invoke(
                    {
                        "input": user_query.text,
                        "instructions": f"""
                            File path: {current_working_file or "no file path provided"}                          
                        """,
                        "chat_history": chat_history.formatted_output,
                    }
                )

                # Append new chat to session history
                new_chat(user_query=user_query.text, ai_output=result["output"])
            except Exception as e:
                # Show error message and auto-hide after delay
                error_message = st.error(f"Some Error occurred {e}")
                time.sleep(3)
                # error_message.empty()

            finally:
                # Reset action state and rerun the app
                st.session_state[SessionStateEnum.action_in_progress] = False
                # st.rerun()


if __name__ == "__main__":
    app()
