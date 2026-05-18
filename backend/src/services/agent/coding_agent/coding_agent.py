from langchain.agents import create_agent
from fastapi import HTTPException
from langchain_core.messages import HumanMessage, AIMessage
from src.services.config import groq_model
from src.services.agent.coding_agent.tools import (
    understand_files_codebase
)

SYSTEM_PROMPT = """
    system prompt
"""

TOOLS = [
    understand_files_codebase
]

HISTORY = []

agent = create_agent(
    model=groq_model,
    tools=TOOLS,
    system_prompt=SYSTEM_PROMPT
)

async def run_agent(
    query: str,
    history: list[HumanMessage | AIMessage] = HISTORY
) -> str:
    try:
        response = await agent.invoke(
            input=query,
            config={
                "recursion_limit": 50
            },
            context=history
        )

        response = response['messages'][-1]

        HISTORY.append(HumanMessage(query))
        HISTORY.append(AIMessage(response))

        return response

    except HTTPException:
        raise
    except Exception as e:
        print(F"Error {e} occurred while running agent.")