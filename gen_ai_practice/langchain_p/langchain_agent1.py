from langchain.agents import create_agent
from langchain_openai import AzureChatOpenAI
from langgraph.checkpoint.memory import MemorySaver


from dotenv import load_dotenv
load_dotenv()

import os

model = AzureChatOpenAI(
    model="gpt-4o",  # or your deployment model name
    azure_deployment=os.getenv("AZURE_OPENAI_MODEL"),
)
from pydantic import BaseModel
class AnswerFormateClass(BaseModel):
    response: str
    source:str

memmory=MemorySaver()

my_agent=create_agent(
    model=model,
    tools=[],
    system_prompt="you are a informative agent which give short and crisp reponse to any query.",
    response_format=AnswerFormateClass,
    checkpointer=memmory
    )

import uuid
my_uuid = uuid.uuid4()
print(my_uuid)
config = {"configurable": {"thread_id": str(my_uuid)}}

result=my_agent.invoke(
    {
        "messages":[{"role":"user","content":"who is mr. Modi"}]
    },
    config=config
)
print(result)
print("---------------------------------")
print(result["structured_response"])

import uuid
my_uuid = uuid.uuid4()
print(my_uuid)
config = {"configurable": {"thread_id": str(my_uuid)}}

result=my_agent.invoke(
    {
        "messages":[{"role":"user","content":"what is the age of him?"}]
    },
    config=config
)
print(result)
print("---------------------------------")
print(result["structured_response"])
