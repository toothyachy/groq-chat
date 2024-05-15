import streamlit as st
import os
from chain import *

os.environ["LANGCHAIN_TRACING_V2"] = st.secrets["langchain_tracing_v2"]
os.environ["LANGCHAIN_PROJECT"] = st.secrets["langchain_project"]
os.environ["LANGCHAIN_ENDPOINT"] = st.secrets["langchain_endpoint"]
os.environ["LANGCHAIN_API_KEY"] = st.secrets["langchain_api_key"]


st.title("Meet Me, Mark Manson")
st.caption("Sure, I'm just sitting around all day waiting for your questions anyway.")

get_message_history(session_id="abcd1234")
history = store["abcd1234"].messages
for i in range(len(history)):
    if i % 2 == 0:
        with st.chat_message("user"):
            st.write(f"{history[i].content}")
    else:
        with st.chat_message("assistant"):
            st.write(f"{history[i].content}")


qn = st.chat_input("Whatever")
if qn:
    with st.chat_message("user"):
        st.markdown(qn)

    with st.chat_message("assistant"):
        st.write_stream(
            chain_with_memory.stream(
                {"question": qn},
                config={"configurable": {"session_id": "abcd1234"}},
            )
        )
