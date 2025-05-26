from acp_sdk.models import (
    Artifact,
    ArtifactEvent,
    Message,
    MessagePart,
    MessagePartEvent,
)
import streamlit as st
from rhds_component import ngui_rhds_component
from streamlit_common import display_chat_history

import asyncio
import logging

from acp_sdk.client import Client

# from beeai_framework.adapters.beeai_platform.agents import BeeAIPlatformAgent
# from beeai_framework.memory.unconstrained_memory import UnconstrainedMemory

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Streamlit UI
st.set_page_config(initial_sidebar_state="collapsed", layout="wide")
# Side bar
with st.sidebar:
    st.header("Conversation", divider=True)
    if st.button("New thread"):
        st.session_state.messages = []
        st.rerun()


st.title("Next Gen UI Movies Assistant powered by ACP")


# Init session
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = None

display_chat_history(st, st.session_state.messages)

# https://github.com/i-am-bee/beeai-framework/blob/main/python/examples/agents/providers/beeai_platform.py
# movies_platform_agent = BeeAIPlatformAgent(agent_name="movies", url="http://127.0.0.1:8333/api/v1/acp/", memory=UnconstrainedMemory())
# ngui_platform_agent = BeeAIPlatformAgent(agent_name="next_gen_ui", url="http://127.0.0.1:8333/api/v1/acp/", memory=UnconstrainedMemory())

movies_acp_url = "http://localhost:8000"


async def start_chat():
    prompt = st.chat_input("Ask something about movies...")
    if prompt:
        async with (
            Client(base_url=movies_acp_url) as client,
            client.session(st.session_state.session_id) as agent_session,
        ):
            logger.debug("session_id=%s", agent_session._session_id)
            st.session_state.session_id = agent_session._session_id

            logger.info(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            full_response = ""
            ngui_response = ""
            with st.chat_message("assistant"):
                # with st.expander("Agent thinking"):
                #     agent_thinking = st.empty()
                col1, col2 = st.columns(2, gap="medium", border=False)
                with col2:
                    message_placeholder = st.empty()

                try:
                    # https://github.com/i-am-bee/acp/blob/main/examples/python/basic/clients/session.py
                    # https://github.com/i-am-bee/acp/blob/main/examples/python/beeai-chat/client.py
                    input = [Message(parts=[MessagePart(content=prompt, role="user")])]
                    logger.debug(
                        "Sending mesages to the assistant count=%s", len(input)
                    )

                    async for event in agent_session.run_stream(
                        agent="movies", input=input
                    ):
                        match event:
                            case MessagePartEvent(part=MessagePart(content=content)):
                                full_response += content
                                message_placeholder.markdown(full_response)
                            case ArtifactEvent(part=Artifact(content=tool_output)):
                                (ngui_response, ngui_response_id) = (
                                    await call_ngui_client(
                                        prompt, tool_output, id=event.part.id
                                    )
                                )
                                with col1:
                                    ngui_rhds_component(
                                        ngui_response, key=ngui_response_id
                                    )

                except Exception as e:
                    logger.exception("Error in execution")
                    ngui_response = e
                    full_response = ""
                    with col1:
                        st.text(ngui_response)
            # save to the history
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response, "ngui": ngui_response}
            )


async def call_ngui_client(prompt: str, tool_output: str, id: str) -> tuple[str, str]:
    ngui_acp_url = "http://localhost:8001"

    result = ""
    ngui_input: list[Message] = [
        Message(parts=[MessagePart(content=prompt, role="user")]),
        # TODO: Artifacts sent to agent are translated to MessagePart !!!
        Message(
            parts=[
                Artifact(content=tool_output, name="tool_output", role="tool", id=id)
            ]
        ),
    ]

    async with Client(base_url=ngui_acp_url) as ngui_client:
        async for ngui_event in ngui_client.run_stream(
            agent="next_gen_ui", input=ngui_input
        ):
            match ngui_event:
                case ArtifactEvent(part=Artifact(content=content)):
                    result = content
                    id = ngui_event.part.id

    return (result, id)


asyncio.run(start_chat())
