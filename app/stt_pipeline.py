import streamlit as st
import openai
from io import BytesIO
from streamlit_mic_recorder import mic_recorder
from app import config
import logging

logging.getLogger("openai").setLevel(logging.ERROR)

if config.OPENAI_API_KEY:
    client = openai.OpenAI(api_key=config.OPENAI_API_KEY)
else:
    client = None
    st.error("OpenAI API key not found in .env file. Please set OPENAI_API_KEY.")

# session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "audio_history" not in st.session_state:
    st.session_state.audio_history = []
if "transcript" not in st.session_state:
    st.session_state.transcript = None

def transcribe_callback():
    """Callback to auto-transcribe and display on recording stop."""
    if 'recorder_output' in st.session_state and st.session_state.recorder_output:
        audio_data = st.session_state.recorder_output
        if client:
            try:
                audio_file = BytesIO(audio_data['bytes'])
                audio_file.name = "audio.webm"
                
                st.session_state.is_processing = True
                
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
                
                st.session_state.transcript = transcript
                st.session_state.chat_history.append(f"User: {transcript}")
                st.session_state.audio_history.append(("user", audio_data['bytes'], transcript))
                st.success(f"Transcription: {transcript}")
                logging.info(f"Session: {st.session_state.get('session_id', 'unknown')} - Transcription completed: {transcript}")
                
                st.session_state.is_processing = False
                st.rerun()
                
            except Exception as e:
                st.session_state.is_processing = False
                logging.error(f"Session: {st.session_state.get('session_id', 'unknown')} - Transcription error: {str(e)}")
                st.error(f"Transcription error: {str(e)}")
        else:
            st.session_state.is_processing = False
            st.error("No OpenAI API key provided.")

def render_mic_recorder():
    """Render the mic recorder component."""
    if st.session_state.get("is_processing", False):
        with st.spinner("Processing audio..."):
            pass
    else:
        audio = mic_recorder(
            key="recorder",
            start_prompt="🎤 Start Recording",
            stop_prompt="⏹️ Stop & Transcribe",
            just_once=False,
            use_container_width=True,
            format="webm",
            callback=transcribe_callback
        )
        return audio