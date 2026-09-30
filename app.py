import streamlit as st
import requests

st.title("Team Chatbot")

API_URL = "https://gen.pollinations.ai/v1/chat/completions"
API_KEY = st.secrets["POLLINATIONS_API_KEY"]

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Ask your question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.spinner("Thinking..."):
        try:
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "openai",
                "messages": st.session_state.messages
            }
            response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            data = response.json()
            answer = data['choices'][0]['message']['content']
        except Exception as e:
            answer = f"Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.chat_message("assistant").write(answer)
