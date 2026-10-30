from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware



# agent = create_agent(
#     model="gpt-5.5",
#     tools=[write_file, execute_sql, read_data],
#     middleware=[
#         HumanInTheLoopMiddleware(
#             interrupt_on={
#                 "write_file": True,  # All decisions (approve, edit, reject, respond) allowed
#                 "execute_sql": {"allowed_decisions": ["approve", "reject"]},  # No editing allowed
#                 "read_data": False, # Safe operation, no approval needed
#             },
#             # Prefix for interrupt messages - combined with tool name and args to form the full message
#             # e.g., "Tool execution pending approval: execute_sql with query='DELETE FROM...'"
#             # Individual tools can override this by specifying a "description" in their interrupt config
#             description_prefix="Tool execution pending approval",
#         ),
#     ],