from typing import List
import streamlit as st
from langchain_core.output_parsers import StrOutputParser

from decodeon.types.enums import SessionStateEnum
from decodeon.models import ChatHistory, ChatHistoryList


parser = StrOutputParser()


def new_chat(
    user_query: str,
    ai_output: str,
):
    st.chat_message("user").write(user_query)
    formatted_output = parser.parse(ai_output).strip()
    st.chat_message("ai").write(formatted_output)

    chat_history = ChatHistory(user_query=user_query, ai_output=ai_output)

    chat_history_list: ChatHistoryList = st.session_state[SessionStateEnum.chat_history]
    chat_history_list.root.append(chat_history)


def init_chat_history():
    if SessionStateEnum.chat_history not in st.session_state:
        st.session_state[SessionStateEnum.chat_history] = ChatHistoryList([])

    chat_history: ChatHistoryList = st.session_state[SessionStateEnum.chat_history]

    for chat in chat_history.root:
        st.chat_message("user").write(chat.user_query)
        st.chat_message("ai").write(chat.ai_output)
