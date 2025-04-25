from typing import TypedDict, TypeVar, Dict, Generic, Optional, Any
from langchain.agents import AgentExecutor
from langchain_core.runnables import RunnableConfig


StrDictAny = TypeVar(name="StrDictAny", bound=Dict[str, Any])
TInput = TypeVar("TInput")


class ReactAgentInput(TypedDict):
    input: str
    instructions: Optional[str]
    chat_history: Optional[str]


class TypedAgentExecutor(Generic[TInput]):
    def __init__(self, executor: AgentExecutor):
        self.executor = executor

    def invoke(self, input: TInput, config: RunnableConfig | None = None, **kwargs):
        return self.executor.invoke(input=input, config=config, **kwargs)
