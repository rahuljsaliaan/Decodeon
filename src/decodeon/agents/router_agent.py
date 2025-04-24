from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import BasePromptTemplate
from langchain_core.tools import Tool

from decodeon.core import settings
from decodeon.agents import create_python_agent, create_csv_agent
from decodeon.types import TypedAgentExecutor, ReactAgentInput, StrDictAny
from decodeon.types.enums import OpenAIModel


llm = ChatOpenAI(
    api_key=settings.openai_api_key,
    model=OpenAIModel.gpt_4o_mini.value,
    temperature=0,
)
base_prompt: BasePromptTemplate = hub.pull("langchain-ai/react-agent-template")


python_agent_func = (create_python_agent().invoke,)


def python_agent_executor_wrapper(original_prompt: str) -> StrDictAny:
    return create_python_agent().invoke(input={"input": original_prompt})


def csv_agent_executor_wrapper(original_prompt: str, path: str = None) -> StrDictAny:
    return create_csv_agent(path=path).invoke(input={"input": original_prompt})


def create_router_agent(path: str = None):
    tools = [
        Tool(
            name="Python Agent",
            func=python_agent_executor_wrapper,
            description="""
            Useful when you need to transform natural language into python code and execute it, returning the result of the code execution. DOES NOT ACCEPT CODE AS INPUT
            """,
        ),
        Tool(
            name="CSV Agent",
            func=csv_agent_executor_wrapper,
            description="""
            Useful when you need answer question over the csv file.
            Takes an optional parameter path and if not provided then uses the default episode_info.csv file
            """,
        ),
    ]

    agent = create_react_agent(
        llm=llm,
        prompt=base_prompt.partial(instructions=f"File path: {str(path)}"),
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
        input={"input": "Which writer wrote the most episodes>"}
    )
