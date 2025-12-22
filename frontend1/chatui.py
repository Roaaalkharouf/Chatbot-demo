import streamlit as st
import requests
import time

# PAGE CONFIG
st.set_page_config(page_title="Cirrusgo Chatbot", layout="wide")

# CUSTOM CSS (BACKGROUND + CHAT CARD)
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #6a7cff, #7b5cbf);
    }

    .main {
        background: transparent;
    }

    .chat-container {
        max-width: 900px;
        margin: 40px auto;
        background: white;
        border-radius: 16px;
        padding: 0;
        box-shadow: 0px 20px 40px rgba(0,0,0,0.2);
        overflow: hidden;
    }

    .chat-header {
        padding: 20px;
        background: linear-gradient(135deg, #6a7cff, #7b5cbf);
        color: white;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
    }

    .chat-body {
        padding: 20px;
        height: 500px;
        overflow-y: auto;
        background: #f9f9f9;
    }

    .chat-footer {
        padding: 16px;
        border-top: 1px solid #eee;
        background: white;
    }

    .typing {
        font-style: italic;
        color: #888;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# BACKEND API
API_URL = "http://localhost:8000/chat"
# API_URL = "https://YOUR_LAMBDA_FUNCTION_URL"

# SESSION STATE
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = "demo-session"

# CHAT UI
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Header
st.markdown('<div class="chat-header">AI Chatbot</div>', unsafe_allow_html=True)

# Chat body
st.markdown('<div class="chat-body">', unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

st.markdown('</div>', unsafe_allow_html=True)

# Footer (input)
st.markdown('<div class="chat-footer">', unsafe_allow_html=True)

user_input = st.chat_input("Type your message...")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# HANDLE MESSAGE SEND (ENTER OR SEND BUTTON)
if user_input:
    # Show user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Typing indicator
    with st.chat_message("assistant"):
        typing = st.empty()
        typing.markdown("💬 *Typing...*", unsafe_allow_html=True)

    payload = {
        "user_message": user_input,
        "session_id": st.session_state.session_id,
        "model": "titan"
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=30)

        if response.status_code != 200:
            result=f"Backend returned {response.status_code}: {response.text}"
        else:
            data=response.json()
            result=data.get("response", "No response failed in backend output")
    except Exception as e:
            result= f"Backend error: {e}"

    typing.markdown(result)

    st.session_state.messages.append({
        "role": "assistant",
        "content": result
    })
