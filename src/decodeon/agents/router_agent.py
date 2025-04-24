from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import BasePromptTemplate
from langchain_core.tools import Tool
from langchain_core.output_parsers import PydanticOutputParser

from decodeon.core import settings
from decodeon.models import CSVAgentInput
from decodeon.agents import create_python_agent, create_csv_agent
from decodeon.types import TypedAgentExecutor, ReactAgentInput, StrDictAny
from decodeon.types.enums import OpenAIModelEnum


llm = ChatOpenAI(
    api_key=settings.openai_api_key,
    model=OpenAIModelEnum.gpt_4o_mini.value,
    temperature=0,
)
base_prompt: BasePromptTemplate = hub.pull("langchain-ai/react-agent-template")
parser = PydanticOutputParser(pydantic_object=CSVAgentInput)


def python_agent_executor_wrapper(original_prompt: str) -> StrDictAny:
    return create_python_agent().invoke(input={"input": original_prompt})


def csv_agent_executor_wrapper(input_str: str) -> StrDictAny:
    input_data = parser.parse(input_str)

    print(input_data.model_dump())

    return create_csv_agent(path=input_data.path).invoke(
        input={"input": input_data.input}
    )


def create_router_agent():
    tools = [
        Tool(
            name="Python Agent",
            func=python_agent_executor_wrapper,
            description="""\
            Use this tool when you need to **perform tasks by writing and executing Python code** based on natural language instructions.

            ⚠️ IMPORTANT: This tool does **not accept raw code**. Only provide natural language descriptions of the task.

            Example tasks this tool can handle:
            - Generating and saving QR codes into directories
            - Downloading content from the web and storing it
            - Creating or modifying files
            - Performing calculations or data transformations
            - Any logic that requires using Python programmatically

            **Choose this tool for any automation or data processing task where Python is needed.**
            """,
        ),
        Tool(
            name="CSV Agent",
            func=csv_agent_executor_wrapper,
            description=f"""
            Use this tool to analyze or extract insights from a CSV file.

            🧾 Input must be a dictionary with the following keys:
            - "path": Full file path to the CSV file 
            - "input": Natural language instruction describing the task

            🚫 Do NOT include labels like "CSV file path:" in the path.
            ⚠️ Only use this tool if a valid 'path' is available and NOT marked as 'Not given'.
            """,
        ),
    ]

    agent = create_react_agent(
        llm=llm,
        prompt=base_prompt,
        tools=tools,
    )

    agent_executor = TypedAgentExecutor[ReactAgentInput](
        AgentExecutor(
            agent=agent, tools=tools, verbose=True, handle_parsing_errors=True
        )
    )

    return agent_executor


if __name__ == "__main__":
    router_agent_executor = create_router_agent()
    router_agent_executor.invoke(
        input={
            "input": "Which writer wrote the most episodes>",
            "instructions": "CSV file path: Not given",
        }
    )
