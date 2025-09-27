
import streamlit as st
from gemini import generate

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
import os

load_dotenv()

elevenlabs = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY"),
)

def tts(text):
    audio = elevenlabs.text_to_speech.convert(
            text=text,
            voice_id="qAZH0aMXY8tw1QufPN0D",
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
    )

    with open("eleven_output.mp3","wb") as f:
        for chunk in audio:
            f.write(chunk)

st.set_page_config(page_title="Gemini Royal Chatbot", page_icon="👑", layout="centered")

# Custom CSS for luxury aesthetics
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #f5e9c2 0%, #e6b800 100%);
        font-family: 'Cinzel', serif;
    }
    .main {
        background: url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1500&q=80') no-repeat center center fixed;
        background-size: cover;
    }
    .royal-header {
        font-size: 3em;
        font-family: 'Cinzel', serif;
        color: #FFD700;
        text-shadow: 0 0 20px #e6b800, 0 0 5px #fff;
        margin-bottom: 0.5em;
        text-align: center;
        animation: glow 2s infinite alternate;
    }
    @keyframes glow {
        from { text-shadow: 0 0 10px #e6b800, 0 0 5px #fff; }
        to { text-shadow: 0 0 30px #FFD700, 0 0 10px #fff; }
    }
    .chat-bubble-user {
        background: #fffbe6;
        color: #bfa100;
        border-radius: 20px 20px 5px 20px;
        padding: 1em;
        margin-bottom: 0.5em;
        box-shadow: 0 2px 8px #e6b80033;
        font-family: 'Cinzel', serif;
        font-size: 1.1em;
    }
    .chat-bubble-bot {
        background: #fff;
        color: #e6b800;
        border-radius: 20px 20px 20px 5px;
        padding: 1em;
        margin-bottom: 1em;
        box-shadow: 0 2px 12px #FFD70055;
        font-family: 'Cinzel', serif;
        font-size: 1.1em;
    }
    .stTextInput>div>div>input {
        background: #fffbe6;
        color: #bfa100;
        font-family: 'Cinzel', serif;
        font-size: 1.1em;
        border: 2px solid #FFD700;
        border-radius: 10px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #FFD700 0%, #e6b800 100%);
        color: #fff;
        font-family: 'Cinzel', serif;
        font-size: 1.1em;
        border-radius: 10px;
        border: none;
        box-shadow: 0 2px 8px #e6b80055;
        transition: background 0.3s;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #e6b800 0%, #FFD700 100%);
        color: #fffbe6;
    }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

st.markdown('<div class="royal-header">👑 Gemini Royal Chatbot 👑</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#bfa100;font-size:1.2em;'>Ask anything and receive a response worthy of royalty.</p>", unsafe_allow_html=True)


# Use st.session_state['messages'] for persistent chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

user_input = st.text_input("Your Royal Question:", "")

if st.button("Send to the Throne") and user_input:
    with st.spinner("The royal mind is pondering..."):
        # Prepare conversation history as context
        history = ""
        for msg in st.session_state["messages"]:
            if msg["role"] == "user":
                history += f"User: {msg['content']}\n"
            else:
                history += f"Gemini: {msg['content']}\n"
        # Add the new user input
        history += f"User: {user_input}\n"
        response = generate(history)
        st.session_state["messages"].append({"role": "user", "content": user_input})
        st.session_state["messages"].append({"role": "bot", "content": response})

        # Convert Gemini response to speech
        tts(response)

        # Play the generated audio in the browser
        st.audio("eleven_output.mp3", format="audio/mp3")

if st.session_state["messages"]:
    st.markdown('<h3 style="color:#FFD700;text-shadow:0 0 10px #e6b800;">Royal Chat History</h3>', unsafe_allow_html=True)
    # Display chat bubbles in order
    for msg in reversed(st.session_state["messages"]):
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-bubble-user"><strong>You:</strong> {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bubble-bot"><strong>Gemini:</strong> {msg["content"]}</div>', unsafe_allow_html=True)
