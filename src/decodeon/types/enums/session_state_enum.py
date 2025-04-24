from enum import Enum


class SessionStateEnum(Enum):
    """Enumeration for session state keys."""

    csv_path = "csv_path"
    chat_history = "chat_history"
    action_in_progress = "action_in_progress"
