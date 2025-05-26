from typing import AsyncGenerator, Optional
import logging
import json

from langgraph.prebuilt import create_react_agent
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    AIMessageChunk,
    ToolMessage,
    BaseMessage,
)
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from acp_sdk.models import MessagePart, Artifact, Message
from acp_sdk.server import Server, RunYield, RunYieldResume, Context

from next_gen_ui_testing import data_set_movies


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


### Movies Agent
@tool(
    "movie_search_by_title",
    response_format="content",
    parse_docstring=True,
    return_direct=False,
)
def movie_search_by_title(title: Optional[str]):
    """Search movies based on title.
    You get all details about a movie including plot, release date, budget, IMDB rating and also poster as URL and what movies the actor played

    Args:
        title: Movie title e.g. 'Toy Story'
    """
    logger.debug("movie_search_by_title, title=%s", title)
    movies_data = data_set_movies.find_movie(title)
    m_str = json.dumps(movies_data, default=str)
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("movie: %s", json.dumps(movies_data, default=str, indent=2))
    return m_str


model = ChatOpenAI(
    model="llama3.2:latest", api_key="ollama", base_url="http://localhost:11434/v1"
)
system_prompt = (
    "You are useful assistant to answer the user's question about movies."
    "If you'are asked to show picture or play trailer just say 'Here it is.'"
)
# Create LangGraph ReAct movies agent
movies_agent = create_react_agent(
    model=model,
    tools=[movie_search_by_title],
    prompt=system_prompt,
)

server = Server()


def to_framework_message(message: Message) -> BaseMessage:
    """Convert ACP Message to Framework Message"""
    part = message.parts[0]
    content = str(message)
    match part.role:
        case "user":
            return HumanMessage(content=str(message))
        case "assistant":
            return AIMessage(content=str(message))
        case "tool":
            if isinstance(part, Artifact):
                return ToolMessage(content=content, tool_call_id=part.id)
        case _:
            raise ValueError(f"Unsupported role {part.role}")


@server.agent(name="movies")
async def movies_agent_acp_server(
    input: list[Message],
    context: Context,
) -> AsyncGenerator[RunYield, RunYieldResume]:
    try:
        framework_messages = [to_framework_message(message) for message in input]

        async for msg, metadata in movies_agent.astream(
            {"messages": framework_messages},
            # {"configurable": configurable},
            stream_mode="messages",
        ):
            if msg.content == "":
                continue

            if isinstance(msg, ToolMessage):
                part = Artifact(
                    content=msg.content,
                    name="tool_output",
                    role=msg.type,
                    id=msg.tool_call_id,
                )
                logger.debug("sending tool output to client")
                yield Message(parts=[part])
            elif isinstance(msg, AIMessage) or isinstance(msg, AIMessageChunk):
                yield MessagePart(content=msg.content, role="assistant")
    except Exception as e:
        logger.exception("Error in execution")
        raise e


if __name__ == "__main__":
    server.run()
