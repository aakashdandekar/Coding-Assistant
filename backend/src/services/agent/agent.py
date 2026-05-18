from langchain.agents import create_agent
from fastapi import HTTPException
from langchain_core.messages import HumanMessage, AIMessage
from src.services.config import groq_model

SYSTEM_PROMPT = """
    system prompt
"""

TOOLS = []

HISTORY = []

agent = create_agent(
    model=groq_model,
    tools=TOOLS,
    system_prompt=SYSTEM_PROMPT
)

async def run_agent(
    query: str,
    history: list[HumanMessage|AIMessage] = HISTORY
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
        print(f"Error {e} occurred while running agent.")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")