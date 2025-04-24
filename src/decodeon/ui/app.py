import streamlit as st
import time
from langchain_core.output_parsers import StrOutputParser

from decodeon.types.enums import SessionStateEnum
from decodeon.ui.components import (
    init_query_input,
    upload_files,
    init_chat_history,
    new_chat,
)
from decodeon.agents.router_agent import create_router_agent
from decodeon.models import ChatHistoryList
from decodeon.core.utils import get_file_name_without_ext

parser = StrOutputParser()

agent_executor = create_router_agent()


def app():
    st.title("Decodeon: LangChain-Powered Code Interpreter")
    current_working_file = st.session_state.get(SessionStateEnum.csv_path)
    if current_working_file:
        st.markdown(
            f"📄 **Current working file:** `{get_file_name_without_ext(current_working_file)}`"
        )

    user_query = init_query_input()

    init_chat_history()

    if user_query:
        with st.spinner("Generating response..."):
            try:
                st.session_state[SessionStateEnum.action_in_progress] = True
                chat_history: ChatHistoryList = st.session_state[
                    SessionStateEnum.chat_history
                ]

                files = user_query.files

                if len(files) > 0:
                    csv_file = files[0]
                    upload_files(csv_file)

                result = agent_executor.invoke(
                    {
                        "input": user_query.text,
                        "instructions": f"""
                            File path: {current_working_file or "no file path provided"}                          
                        """,
                        "chat_history": chat_history.formatted_output,
                    }
                )
                new_chat(user_query=user_query.text, ai_output=result["output"])
            except Exception as e:
                error_message = st.error(f"Some Error occurred {e}")
                time.sleep(3)
                error_message.empty()
            finally:
                st.session_state[SessionStateEnum.action_in_progress] = False
                st.rerun()


if __name__ == "__main__":
    app()
