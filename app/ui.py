import streamlit as st
from app.stt_pipeline import render_mic_recorder
from app.crisis_toolchain import get_session_id

def consent_banner():
    """Render consent banner and manage consent state."""
    st.markdown("## 🛡️ Consent & Disclosure")
    st.info(
        "This AI chatbot is **not a substitute for professional therapy**.\n\n"
        "Your voice may be processed for analysis. "
        "Data will only be stored if you consent."
    )
    
    if "consent" not in st.session_state:
        st.session_state.consent = False
    
    st.checkbox(
        "I consent to continue and agree that this is not a substitute for professional therapy.",
        key="consent"  # Add this key
    )
    
    if st.session_state.consent:
        if "recorder_output" in st.session_state:
            st.session_state.recorder_output = None
    
    return st.session_state.consent

def emergency_resources():
    """Display emergency resources."""
    st.markdown("### Ministry of Health (MOH)")
    st.markdown("- **General Adult Psychiatry:** +968 2487 3127")
    st.markdown("- **Child & Adolescence Psychiatry:** +968 2487 3127")
    st.markdown("- **Psychology Services:** +968 2487 3983")
    st.markdown("### National Hospitals")
    st.markdown("- **Al Masarra Hospital (Psychiatry & Addiction):** +968 2487 3268")
    st.markdown("- **Royal Hospital – Mental Health Support (Mon–Fri, 8 AM–8 PM):** +968 24 607 555")
    st.markdown("### Private Clinics")
    st.markdown("- **KIMSHEALTH Oman Hospital (Darsait):** +968 2476 0100")
    st.markdown("- **Oman International Hospital (Al Ghubrah):** +968 2490 3500 | WhatsApp: +968 9938 9376")
    st.markdown("- **Muscat Private Hospital:** +968 2458 3600")
    st.markdown("- **Aster Al Raffah Hospital:** +968 2249 6000")
    st.markdown("- **Badr Al Samaa Hospital:** +968 2459 1000")
    st.markdown("- **Burjeel Medical Center:** +968 24 399 777")
    st.markdown("- **Hatat House Polyclinic:** +968 2456 3641 / 9943 1173")
    st.markdown("### 🌐 Global Resource")
    st.markdown("- **WHO – Mental Health:** https://www.who.int/health-topics/mental-health")
    st.info("🚨 Immediate emergency? Call Royal Oman Police / Ambulance: 9999.")

def audio_input():
    """Render audio input UI and return chat history."""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "audio_history" not in st.session_state:
        st.session_state.audio_history = []  # Store (type, audio_bytes, transcript) tuples
    if "is_processing" not in st.session_state:
        st.session_state.is_processing = False
    
    # session ID
    if "session_id" not in st.session_state:
        st.session_state.session_id = get_session_id()
    session_id = st.session_state.session_id
    st.markdown(f"**Session ID**: {session_id}")
    
    if st.session_state.consent:
        st.success("✅ Consent given. Ready to start.")
        st.markdown("Click on **START** to begin speaking.")
        
        with st.container():
            render_mic_recorder()
        
        # Display chat history + audio playback
        st.markdown("### Conversation History")
        for i, entry in enumerate(st.session_state.chat_history):
            if entry.startswith("User:"):
                transcript = entry.replace("User: ", "")
                st.markdown(f"**You**: {transcript}")

                for audio_type, audio_bytes, audio_transcript in st.session_state.audio_history:
                    if audio_type == "user" and audio_transcript == transcript:
                        st.audio(audio_bytes, format="audio/webm")
            elif entry.startswith("Bot:"):
                transcript = entry.replace("Bot: ", "")
                st.markdown(f"**Bot**: {transcript}")

                for audio_type, audio_bytes, audio_transcript in st.session_state.audio_history:
                    if audio_type == "bot" and audio_transcript == transcript:
                        st.audio(audio_bytes, format="audio/mp3")
    
    return st.session_state.chat_history

def display_latest_audio():
    """Placeholder function, no longer needed as audio is shown in chat history."""
    pass
