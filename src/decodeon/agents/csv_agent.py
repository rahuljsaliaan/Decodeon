from langchain_openai import ChatOpenAI
from langchain_experimental.agents import create_csv_agent as create_inbuilt_csv_agent

from decodeon.core import settings
from decodeon.types.enums import OpenAIModelEnum
from decodeon.types import TypedAgentExecutor, ReactAgentInput

llm = ChatOpenAI(
    api_key=settings.openai_api_key,
    model=OpenAIModelEnum.gpt_4.value,
    temperature=0,
)


def create_csv_agent(path: str = None):
    """
    Create a CSV agent using the LangChain library.
    Args:
        path (str): Path to the CSV file.
    """

    if path is None:
        raise FileNotFoundError("File path not provided!")

    return TypedAgentExecutor[ReactAgentInput](
        create_inbuilt_csv_agent(
            llm=llm,
            path=path,
            verbose=True,
            handle_parsing_errors=True,
            allow_dangerous_code=True,
        )
    )


if __name__ == "__main__":
    csv_agent_executor = create_csv_agent()
    csv_agent_executor.invoke(
        input={
            "input": """
            How many columns are there?.
            Which write wrote the most episode? How many episode did he write?.
            """
        }
    )
