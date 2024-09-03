import streamlit as st
from llm import GeminiInterface
import json

# Page configuration
st.set_page_config(
    page_title="LangGu",
    page_icon="👋",
    layout="wide",
    initial_sidebar_state="expanded")

# Session state configuration
if "lang_config" not in st.session_state:
    with open("lang_config.json") as f:
        st.session_state.lang_config = json.load(f)['KOR-JAP']
if "llm" not in st.session_state:
    st.session_state.llm = GeminiInterface(system_prompt=st.session_state.lang_config['system_prompt'])
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "ai", "parts": st.session_state.lang_config['starting_message']}]

# Page content
st.title("LangGu: Your All-In-One Language Buddy")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["parts"])

prompt = st.chat_input("Ask away!")
if prompt:
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("ai"):
        response = st.write_stream(st.session_state.llm.generate(prompt, stream=True))
    st.session_state.messages.append({"role": "user", "parts": prompt})
    st.session_state.messages.append({"role": "ai", "parts": response})
