import streamlit as st
import openai
from io import BytesIO
from app import config
import logging

logging.getLogger("openai").setLevel(logging.ERROR)

client = openai.OpenAI(api_key=config.OPENAI_API_KEY)

def text_to_speech(text):
    """Convert text to speech using OpenAI TTS."""
    try:
        st.session_state.is_processing = True
        
        response = client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=text
        )
        audio_bytes = BytesIO(response.content)
        st.audio(audio_bytes, format="audio/mp3")
        if "chat_history" in st.session_state:
            st.session_state.chat_history.append(f"Bot: {text}")
        if "audio_history" in st.session_state:
            st.session_state.audio_history.append(("bot", response.content, text))
        logging.info(f"Session: {st.session_state.get('session_id', 'unknown')} - TTS completed for response: {text[:50]}...")
        
        st.session_state.is_processing = False
    except Exception as e:
        st.session_state.is_processing = False
        logging.error(f"Session: {st.session_state.get('session_id', 'unknown')} - TTS error: {str(e)}")
        st.error(f"TTS error: {str(e)}")