import streamlit as st
import pathlib
import textwrap
import google.generativeai as genai

genai.configure(api_key='AIzaSyCBkKSe9dtzeQCVW5Of07_QyngJAGONtlQ')

model = genai.GenerativeModel('models/gemini-1.5-pro-latest')

import docx2txt

file_path = pathlib.Path('WA_chatbot.docx')
content = docx2txt.process(file_path)

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.chat_message("system"):
    st.write("Hi there!👋I'm ready to answer your questions. Ask me anything!")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Enter your query"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    if prompt.lower() in ("hi", "hello", "hey"):  # Handle multiple greetings
        response = "How can I help you today?😊"
    else:
        # context_truncated = textwrap.shorten(content, width=1000)
        response1 = model.generate_content([
            "You are an expert customer assistant and student tutor from Sample Team. I'll give you question and context and you'll return the answer. Answer in 100 words in a paragraph.",
            f"Question: {prompt}",
            f"Context: {content}"
        ])
        response = f"{response1.text}"

    # st.write(response)

    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
