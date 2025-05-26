from collections.abc import AsyncGenerator

import logging
from typing import Any

import beeai_framework
from acp_sdk import Artifact, Message
from acp_sdk.models import MessagePart
from acp_sdk.server import Server, RunYield, RunYieldResume, Context

from beeai_framework.backend.chat import ChatModel, ChatModelParameters
from beeai_framework.agents.react import ReActAgent, ReActAgentUpdateEvent
from beeai_framework.backend import AssistantMessage, Role, UserMessage
from beeai_framework.memory import UnconstrainedMemory
from beeai_framework.tools.tool import AnyTool

from movies_beeai_tools import MovieSearchByTitleTool

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

server = Server()

# https://github.com/i-am-bee/acp/blob/main/examples/python/beeai-chat/agent.py


def to_framework_message(role: str, content: str) -> beeai_framework.backend.Message:
    match role:
        case Role.USER:
            return UserMessage(content)
        case Role.ASSISTANT:
            return AssistantMessage(content)
        case _:
            raise ValueError(f"Unsupported role {role}")


@server.agent(name="movies")
async def movies_agent(
    input: list[Message],
    context: Context,
) -> AsyncGenerator[RunYield, RunYieldResume]:
    """
    The agent is an AI-powered conversational system with memory, supporting search in movies DB.
    """

    # ensure the model is pulled before running
    llm = ChatModel.from_name("ollama:llama3.2", ChatModelParameters(temperature=0.5))

    # Configure tools
    tools: list[AnyTool] = [MovieSearchByTitleTool()]

    # Tempaltes
    # https://github.com/i-am-bee/beeai-framework/blob/main/python/examples/agents/react_advanced.py
    instructions = """
        You are useful assistant to answer the user's question about movies. 
        Always use any of registered tool functions to get information about movie and then provide the answer based on what you found.
        If you'are asked to show picture or play trailer the answer is 'Here it is.'
    """

    templates: dict[str, Any] = {
        "system": lambda template: template.update(
            defaults={"instructions": instructions}
        ),
    }

    # Create agent with memory and tools
    agent = ReActAgent(
        llm=llm, templates=templates, tools=tools, memory=UnconstrainedMemory()
    )

    logger.debug(input)

    framework_messages = [
        to_framework_message(message.parts[0].role, str(message))
        for message in input
        if not isinstance(message.parts[0], Artifact)
    ]
    await agent.memory.add_many(framework_messages)

    async for data, event in agent.run():
        match (data, event.name):
            case (ReActAgentUpdateEvent(), "update"):
                update = data.update.value
                logger.debug("update: %s", update)
                if not isinstance(update, str):
                    update = update.get_text_content()
                match data.update.key:
                    # case "tool_input":
                    #     yield Message(parts=[MessagePart(content=update, role="tool")])
                    case "tool_output":
                        part = Artifact(
                            content=update,
                            name="tool_output",
                            role=Role.TOOL,
                            id=event.id,
                        )
                        logger.debug("sending tool output: %s", part)
                        yield Message(parts=[part])

            case (ReActAgentUpdateEvent(), "partial_update"):
                update = data.update.value
                if not isinstance(update, str):
                    update = update.get_text_content()
                match data.update.key:
                    case "thought":
                        yield {data.update.key: update}
                    # case "tool_output":
                    # yield {data.update.key: update}
                    # yield Message(parts=[MessagePart(content=update, role="tool")])
                    case "final_answer":
                        yield MessagePart(content=update, role=Role.ASSISTANT)


if __name__ == "__main__":
    server.run()
