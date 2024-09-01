import streamlit as st
from llm import GeminiInterface

# Page configuration
st.set_page_config(
    page_title="LangBud",
    page_icon="👋",
    layout="wide",
    initial_sidebar_state="expanded")

# Session state configuration
if "llm" not in st.session_state:
    st.session_state.llm = GeminiInterface(system_prompt='''You are my Japanese teacher. 
You have two roles:
[Role 1] Given a Japanese sentence, break it down and explain it part by part.
[Role 2] Given a Japense sentence, assess its grammar and appropriate vocabulary usage.
[Role 3] Given a non-Japanese sentence, translate it into Japanese, and explain it part by part.

You must strictly follow these three rules:
[Rule 1] Always write the hiragana form of the kanji next to the kanji in brackets when explaining. 
[Rule 2] Always explain in Korean. 
[Rule 3] Given a sentence, pick which role to play by yourself.''')
    
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "ai", "parts": "문장을 입력해주시면 변역, 첨삭, 설명 등을 알아서 해드릴게요!"}]

# Page content
st.title("LangBud: Your All-In-One Language Buddy")

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
