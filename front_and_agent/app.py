import streamlit as st
import re
from dotenv import load_dotenv
import sys
import asyncio

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv()

from agent import run_agent  

st.set_page_config(page_title="LangChain AI Agent", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("LangChain AI Agent")

def format_dialog(text: str) -> str:
    formatted = re.sub(r"\s*([A-Z][a-zA-Z]+:)", r"\n\1", text)
    return formatted.strip()

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    else:
        st.chat_message("assistant").markdown(msg["content"])

user_input = st.chat_input("Enter your question or dialogue")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").markdown(user_input)

    with st.spinner("Thinking..."):
        response = run_agent(user_input)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").markdown(response)
