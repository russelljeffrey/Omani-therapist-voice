import streamlit as st
from app.ui import consent_banner, emergency_resources, audio_input, display_latest_audio
from app.intent_analysis import analyze_intent
from app.crisis_toolchain import detect_crisis, get_session_id
from app.response_gen import generate_response
from app.tts_pipeline import text_to_speech
from app.rag_layer import setup_vectorstore
from app import config
import logging



# Configure logging with session_id
logging.basicConfig(
    filename="crisis_log.txt",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - Session: %(session_id)s - %(message)s",
    force=True
)
logging.getLogger().handlers[0].setFormatter(
    logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - Session: %(session_id)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
)
logging.getLogger().handlers[0].setLevel(logging.ERROR)

def main():
    st.set_page_config(page_title="Omani Therapist Voice Bot", layout="centered")
    st.title("🧠 Omani Therapist Voice Bot (Prototype)")
    
    if not config.OPENAI_API_KEY:
        st.error("OpenAI API key not found in .env file. Please set OPENAI_API_KEY.")
        emergency_resources()
        return
    
    # Initialize vectorstore
    try:
        vectorstore = setup_vectorstore()
        st.session_state.vectorstore = vectorstore
    except Exception as e:
        st.error(f"Failed to initialize vectorstore: {str(e)}. App may have limited functionality.")
        logging.error(f"Vectorstore initialization failed: {str(e)}")
    
    if not consent_banner():
        st.error("❌ Consent not given. Redirected to emergency support:")
        emergency_resources()
        return
    
    # Audio input and chat history
    with st.spinner("Processing your input..."):
        chat_history = audio_input()
    
    # Process new transcript
    if st.session_state.get("transcript"):
        transcript = st.session_state.transcript
        with st.spinner("Analyzing and generating response..."):
            # Analyze intent (emotion + rule-based intent)
            emotions, intent = analyze_intent(transcript)
            st.session_state.emotions = emotions
            st.session_state.intent = intent
            st.write("**Detected Emotions:**", ", ".join([f"{e['label']} ({e['score']:.2f})" for e in emotions]))
            st.write(f"**Intent:** {intent}")
            
            # Crisis Toolchain
            crisis_risk, score = detect_crisis(transcript, emotions)
            st.session_state.crisis_risk = crisis_risk
            st.write(f"**Crisis Risk:** {crisis_risk} ({score:.2f})")
            
            if crisis_risk.lower() in ['high risk', 'medium risk'] and score > 0.8:
                st.error("⚠️ أشوفك محتاج دعم فوري، ياخي. تواصل مع مستشفى المسارة على 2487 3268 أو اتصل 9999 للطوارئ.")
                emergency_resources()
                if crisis_risk.lower() == 'high risk':
                    return  # Halt conversation for high risk
            
            # Response Generation and TTS
            response = generate_response(
                transcript,
                ", ".join([e['label'] for e in emotions]),
                intent,
                crisis_risk
            )
            st.write(f"**Bot Response:** {response}")
            text_to_speech(response)
    
    # Display latest audio (if needed)
    display_latest_audio()

if __name__ == "__main__":
    main()