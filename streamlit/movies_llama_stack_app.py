import os
import streamlit as st
from streamlit_common import display_chat_history

import asyncio
import logging
import json

from llama_stack_client import AsyncLlamaStackClient
from llama_stack_client.types import UserMessage
from llama_stack_client.lib.agents.agent import AsyncAgent

from next_gen_ui_llama_stack import NextGenUILlamaStackAgent
from next_gen_ui_testing import data_set_movies

from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

st.set_page_config(layout="wide")


@st.cache_resource
def get_llama_stack_client():
    LLAMA_STACK_SERVER = os.getenv("LLAMA_STACK_SERVER")
    return AsyncLlamaStackClient(base_url=LLAMA_STACK_SERVER)


@st.cache_resource
def get_movies_agent():
    client = get_llama_stack_client()

    # Movies Agent
    def find_movie(title: str):
        """Get details of movie.

        :param title: movie title e.g. Toy Story
        :returns: detail about movie
        """
        logger.debug("Get movie, title: %s", title)
        # imported from next_gen_ui_testing
        movies_data = data_set_movies.find_movie(title)
        response_str = json.dumps(movies_data, default=str)
        logger.debug("returning: %s", response_str)
        return response_str

    INFERENCE_MODEL = os.getenv("INFERENCE_MODEL")
    movies_agent = AsyncAgent(  # ReActAgent
        client=client,
        model=INFERENCE_MODEL,
        instructions="You are a helpful assistant. Use the tools you have access to for providing relevant answers.",
        sampling_params={
            "strategy": {"type": "top_p", "temperature": 1.0, "top_p": 0.9},
        },
        tools=[find_movie],
    )
    return movies_agent


@st.cache_resource
def get_ngui_agent():
    client = get_llama_stack_client()
    INFERENCE_MODEL_NGUI = os.getenv("INFERENCE_MODEL_NGUI")
    ngui_agent = NextGenUILlamaStackAgent(client, INFERENCE_MODEL_NGUI)
    logger.info("NGUI Agent created with INFERENCE_MODEL_NGUI=%s", INFERENCE_MODEL_NGUI)
    return ngui_agent


client = get_llama_stack_client()


# Streamlit UI
# Display chat history
st.title("Next Gen UI Movies Assistant powered by Llama Stack")

if "messages" not in st.session_state:
    st.session_state.messages = []

display_chat_history(st, st.session_state.messages)

agent = get_movies_agent()
ngui_agent = get_ngui_agent()


async def get_ngui_rendering(user_input, steps, ngui_placeholder):
    async for ng_agent_event in ngui_agent.create_turn(
        user_input, steps=steps, component_system="rhds"
    ):
        logger.info(f"\n\n-------NGUI Agent event_type={ng_agent_event['event_type']}")
        if ng_agent_event["event_type"] == "rendering":
            ngui_data = ng_agent_event["payload"]
            ngui_response = ngui_data[0]["rendition"]
            logger.debug(ngui_response)
            ngui_placeholder.html(ngui_response)
            return ngui_response


async def process_response(
    prompt, response, message_component, ngui_placeholder, previous_tool_step
):
    full_response: str = ""
    ngui_response = ""
    tool_step = ""
    async for chunk in response:
        # logger.debug("chunk: %s", chunk)
        payload = chunk.event.payload
        if payload.event_type == "step_progress" and payload.delta.type == "text":
            full_response += payload.delta.text
            message_component.markdown(full_response)

        if (
            payload.event_type == "step_complete"
            and payload.step_details.step_type == "tool_execution"
        ):
            tool_step = payload.step_details
            logger.info("tool response: %s", tool_step)
            # TODO: Fire some event and render it once get response to make it really reactive
            ngui_response = await get_ngui_rendering(
                prompt, [tool_step], ngui_placeholder
            )

    if not ngui_response and previous_tool_step:
        tool_step = previous_tool_step
        logger.info("generating component from historical step. %s", tool_step)
        ngui_response = await get_ngui_rendering(prompt, [tool_step], ngui_placeholder)

    return full_response, ngui_response, tool_step


async def start_chat():
    prompt = st.chat_input("Ask something about movies...")
    if prompt:
        logger.info(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        # Get response from LlamaStack API
        with st.chat_message("assistant"):
            col1, col2 = st.columns(2, gap="medium", border=False)
            with col2:
                message_placeholder = st.empty()
            with col1:
                ngui_placeholder = st.empty()

            # Initialization
            if "session_id" not in st.session_state:
                session_id = await agent.create_session("test-session")
                st.session_state["session_id"] = session_id
                st.session_state["tool_step"] = None

            response = await agent.create_turn(
                messages=[UserMessage(content=prompt, role="user")],
                session_id=st.session_state["session_id"],
            )

            full_response, ngui_response, tool_step = await process_response(
                prompt,
                response,
                message_placeholder,
                ngui_placeholder,
                st.session_state["tool_step"],
            )

            st.session_state["tool_step"] = tool_step
            # message_placeholder.markdown(full_response)

        st.session_state.messages.append(
            {"role": "assistant", "content": full_response, "ngui": ngui_response}
        )


asyncio.run(start_chat())
