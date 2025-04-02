import streamlit as st
from streamlit_common import display_chat_history

import asyncio
import logging

from movies_langgraph_graph import create_assistant_graph
from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Streamlit UI
st.set_page_config(initial_sidebar_state="collapsed", layout="wide")

st.write(
    """
<style>
    h2, h4 {
        margin: 0; 
    }        
</style>""",
    unsafe_allow_html=True,
)

# Side bar: LLM Configuration
with st.sidebar:
    st.header("LLM Configuration", divider=True)
    st.session_state.base_url = st.text_input(
        "API Url", "http://localhost:11434/v1", on_change=st.cache_resource.clear
    )
    st.session_state.api_key = st.text_input(
        "API Key", "ollama", on_change=st.cache_resource.clear
    )
    st.session_state.model = st.text_input(
        "Assistent model", "llama3.2:latest", on_change=st.cache_resource.clear
    )
    st.session_state.ngui_model = st.text_input(
        "Next Gen UI model", "llama3.2:latest", on_change=st.cache_resource.clear
    )
    st.header("Conversation", divider=True)
    if st.button("New thread"):
        st.session_state.messages = []
        st.rerun()


st.title("Next Gen UI Movies Assistant powered by LangGraph")

# Init session
if "messages" not in st.session_state:
    st.session_state.messages = []

display_chat_history(st, st.session_state.messages)


@st.cache_resource
def get_assistent_graph():
    ss = st.session_state
    model = ChatOpenAI(model=ss.model, api_key=ss.api_key, base_url=ss.base_url)
    ngui_model = ChatOpenAI(
        model=ss.ngui_model,
        api_key=ss.api_key,
        base_url=ss.base_url,
        disable_streaming=True,
    )
    return create_assistant_graph(model, ngui_model)


async def start_chat():
    prompt = st.chat_input("Ask something about movies...")
    if prompt:
        logger.info(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        logger.debug(
            "Sending mesages to the assistant messages.count=%s",
            len(st.session_state.messages),
        )
        full_response = ""
        ngui_response = ""
        with st.chat_message("assistant"):
            col1, col2 = st.columns(2, gap="medium", border=False)
            with col2:
                message_placeholder = st.empty()
            with col1:
                ngui_placeholder = st.empty()

            try:
                async for msg, metadata in get_assistent_graph().astream(
                    {"messages": st.session_state.messages},
                    # {"configurable": configurable},
                    stream_mode="messages",
                ):
                    langgraph_node = metadata["langgraph_node"]
                    if langgraph_node == "summary":
                        full_response += msg.content
                        message_placeholder.markdown(full_response)
                    if langgraph_node == "design_system_handler":
                        ngui_response += msg.content
                        ngui_placeholder.html(ngui_response)
            except Exception as e:
                logger.exception("Error in execution")
                ngui_response = e
                full_response = ""
                ngui_placeholder.text(ngui_response)
        # save to the history
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response, "ngui": ngui_response}
        )


asyncio.run(start_chat())
