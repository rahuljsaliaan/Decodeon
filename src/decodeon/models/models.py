from typing import List
from pydantic import BaseModel, RootModel, Field


class ChatHistory(BaseModel):
    user_query: str = Field(..., description="User prompt")
    ai_output: str = Field(..., description="AI generated ouput")

    @property
    def formatted_output(self):
        return f"""
            User: {self.user_query}
            AI: {self.ai_output}
        """


class CSVAgentInput(BaseModel):
    path: str = Field(..., description="Full path to the CSV file")
    input: str = Field(..., description="Natural language query about the CSV")


class ChatHistoryList(RootModel[List[ChatHistory]]):
    @property
    def formatted_output(self):
        chat_list = self.root

        return "\n\n".join(chat.formatted_output.strip() for chat in chat_list)
