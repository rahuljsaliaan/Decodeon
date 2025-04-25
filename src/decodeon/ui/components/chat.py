import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import trim_messages, HumanMessage, AIMessage

from decodeon.core import settings
from decodeon.types.enums import SessionStateEnum, OpenAIModelEnum
from decodeon.models import ChatHistory, ChatHistoryList

# Initialize the llm
llm = ChatOpenAI(
    api_key=settings.openai_api_key,
    temperature=0,
    model=OpenAIModelEnum.gpt_4o_mini.value,
)
# Initialize the output parser
parser = StrOutputParser()


def convert_chat_history_to_langchain_messages(chat_history_list: list[ChatHistory]):
    """Convert chat history to LangChain messages."""

    messages = []
    for entry in chat_history_list:
        messages.append(HumanMessage(content=entry.user_query))
        messages.append(AIMessage(content=entry.ai_output))
    return messages


def convert_langchain_messages_to_chat_history(messages: list) -> list[ChatHistory]:
    """Convert LangChain messages to chat history."""

    chat_history_items = []

    for user_msg, ai_msg in zip(messages[::2], messages[1::2]):
        if isinstance(user_msg, HumanMessage) and isinstance(ai_msg, AIMessage):
            chat_history_items.append(
                ChatHistory(user_query=user_msg.content, ai_output=ai_msg.content)
            )

    return chat_history_items


def new_chat(
    user_query: str,
    ai_output: str,
):
    """Display a new chat message in the Streamlit app."""

    st.chat_message("user").write(user_query)
    formatted_output = parser.parse(ai_output).strip()
    st.chat_message("ai").write(formatted_output)

    # Create a new chat history entry and add it to the session state
    chat_history = ChatHistory(user_query=user_query, ai_output=ai_output)

    # Get the current chat history from the session state
    chat_history_list: ChatHistoryList = st.session_state[SessionStateEnum.chat_history]

    # If the chat history is empty, initialize it with the new entry
    if not chat_history_list.root:
        st.session_state[SessionStateEnum.chat_history] = ChatHistoryList(
            root=[chat_history]
        )

    # Trim the chat history to the maximum number of tokens
    trimmed_messages = trim_messages(
        messages=convert_chat_history_to_langchain_messages(
            chat_history_list.root + [chat_history]
        ),
        max_tokens=settings.chat_max_tokens,
        token_counter=llm,
        strategy="last",
        include_system=True,
    )

    # Convert the trimmed messages back to chat history format and update the session state
    st.session_state[SessionStateEnum.chat_history] = ChatHistoryList(
        root=convert_langchain_messages_to_chat_history(trimmed_messages)
    )


def init_chat_history():
    """Initialize the chat history in the session state."""

    if SessionStateEnum.chat_history not in st.session_state:
        st.session_state[SessionStateEnum.chat_history] = ChatHistoryList(root=[])

    chat_history: ChatHistoryList = st.session_state[SessionStateEnum.chat_history]

    for chat in chat_history.root:
        st.chat_message("user").write(chat.user_query)
        st.chat_message("ai").write(chat.ai_output)
