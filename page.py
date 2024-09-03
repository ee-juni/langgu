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
if "lang_config_json" not in st.session_state:
    with open("lang_config.json") as f:
        st.session_state.lang_config_json = json.load(f)
    st.session_state.sel_lang = list(st.session_state.lang_config_json.keys())[0]
def set_lang_config():
    st.session_state.lang_config = st.session_state.lang_config_json[st.session_state.sel_lang]
    st.session_state.llm = GeminiInterface(system_prompt=st.session_state.lang_config['system_prompt'])
    st.session_state.messages = [{"role": "ai", "parts": st.session_state.lang_config['starting_message']}]
if "lang_config" not in st.session_state:
    set_lang_config()

# Page content
with st.sidebar:
    sel_lang = st.selectbox(
        label="Language Configuration", 
        options=st.session_state.lang_config_json.keys(), 
        index=0, 
        on_change=set_lang_config,
        key="sel_lang"
    )

st.title("👋 LangGu: Your All-In-One Language Buddy")

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
