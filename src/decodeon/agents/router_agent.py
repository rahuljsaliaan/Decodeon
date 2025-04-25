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


# Create llm, prompt, and parser for the router agent
llm = ChatOpenAI(
    api_key=settings.openai_api_key,
    model=OpenAIModelEnum.gpt_4o_mini.value,
    temperature=0,
)
base_prompt: BasePromptTemplate = hub.pull("langchain-ai/react-agent-template")
parser = PydanticOutputParser(pydantic_object=CSVAgentInput)


def python_agent_executor_wrapper(original_prompt: str) -> StrDictAny:
    """
    Wrapper function to execute the Python agent with the provided prompt.
    This function is used to handle the input and output of the Python agent.

    Args:
        original_prompt (str): The prompt to be executed by the Python agent.
    """

    return create_python_agent().invoke(input={"input": original_prompt})


def csv_agent_executor_wrapper(input_str: str) -> StrDictAny:
    """
    Wrapper function to execute the CSV agent with the provided input string.
    This function is used to handle the input and output of the CSV agent.

    Args:
        input_str (str): The input string containing the CSV file path and instructions.
    """

    # Parse the input string to extract the CSV file path and instructions
    input_data = parser.parse(input_str)

    return create_csv_agent(path=input_data.path).invoke(
        input={"input": input_data.input}
    )


def create_router_agent():
    """
    Create a router agent that can handle both Python and CSV tasks.

    This agent uses the LangChain library to create a React agent with specific tools and prompts.
    """

    # Register the tools for the agent.
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
            If you don't have context but have a CSV file path, use this tool to analyze the file.

            🧾 Input must be a dictionary with the following keys:
            - "path": Full file path to the CSV file 
            - "input": Natural language instruction describing the task

            🚫 Do NOT include labels like "CSV file path:" in the path.
            ⚠️ Only use this tool if a valid 'path' is available and NOT marked as 'Not given'.
            """,
        ),
    ]

    # Create the agent using the prompt, LLM, and tools
    agent = create_react_agent(
        llm=llm,
        prompt=base_prompt,
        tools=tools,
    )

    return TypedAgentExecutor[ReactAgentInput](
        AgentExecutor(
            agent=agent, tools=tools, verbose=True, handle_parsing_errors=True
        )
    )


if __name__ == "__main__":
    router_agent_executor = create_router_agent()
    router_agent_executor.invoke(
        input={
            "input": "Which writer wrote the most episodes>",
            "instructions": "CSV file path: Not given",
        }
    )
