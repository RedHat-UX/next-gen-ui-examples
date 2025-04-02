import streamlit
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def display_chat_history(st: streamlit, messages):
    for message in messages:
        with st.chat_message(message["role"]):
            if message["role"] == "user":
                st.markdown(message["content"])
            else:
                col1, col2 = st.columns(2, gap="medium", border=False)
                with col1:
                    st.html(message["ngui"])
                with col2:
                    st.markdown(message["content"])
