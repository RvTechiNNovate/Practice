import os
from langchain.agents import create_agent, AgentState
from langchain.tools import tool
# from langchain_groq import ChatGroq
from langchain_openai import AzureChatOpenAI
from langchain_core.utils.uuid import uuid7

from langgraph.checkpoint.memory import InMemorySaver


from dotenv import load_dotenv
load_dotenv()


# class MyState(AgentState):
#     user_id:str
#     call_count:int


config = {"configurable": {"thread_id": str(uuid7())}}


from pydantic import BaseModel
class AnswerFormate(BaseModel):
    response:str
    source:str

@tool
def search(query: str) -> str:
    """Search the database for information about Groq, Groq API, and Groq models.  Use this tool whenever you need facts or details regarding Groq."""
    return "Groq is an AI infrastructure company that buildsf high-speed hardware (LPU) and APIs for running large language models."


model = AzureChatOpenAI(
    model="gpt-4o",  # or your deployment model name
    azure_deployment=os.getenv("AZURE_OPENAI_MODEL"),
)

agent = create_agent(
    model = model,
    tools=[search],
    system_prompt="You are a helpful assistant. Be concise and accurate.",
    response_format=AnswerFormate,
    checkpointer=InMemorySaver()

    # state_schema=MyState
)

result1= agent.invoke(
    {
    "messages": [{"role": "user", "content": "what is groq? give me response in short"}]
    },
    config
    )

# result2= agent.invoke({
#     "messages": [{"role": "user", "content": "give me one line"}]},
#     config
#     )

print(result1["structured_response"])
# print(result2["structured_response"])

