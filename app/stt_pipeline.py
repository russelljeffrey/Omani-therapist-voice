import streamlit as st
import openai
from io import BytesIO
from streamlit_mic_recorder import mic_recorder
import config

if config.OPENAI_API_KEY:
    client = openai.OpenAI(api_key=config.OPENAI_API_KEY)
else:
    client = None
    st.error("OpenAI API key not found in .env file. Please set OPENAI_API_KEY.")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_audio" not in st.session_state:
    st.session_state.last_audio = None
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
                
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
                
                # Store for chatbot and display
                st.session_state.transcript = transcript
                st.session_state.chat_history.append(f"User: {transcript}")
                st.session_state.last_audio = audio_data['bytes']  # Store latest audio
                st.success(f"Transcription: {transcript}")
                st.rerun()
                
            except Exception as e:
                st.error(f"Transcription error: {str(e)}")
        else:
            st.error("No OpenAI API key provided.")

def render_mic_recorder():
    """Render the mic recorder component."""
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