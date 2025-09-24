import streamlit as st
from stt_pipeline import render_mic_recorder

def consent_banner():
    st.markdown("## 🛡️ Consent & Disclosure")
    st.info(
        "This AI chatbot is **not a substitute for professional therapy**.\n\n"
        "Your voice may be processed for analysis. "
        "Data will only be stored if you consent."
    )

    consent = st.checkbox(
        "I consent to continue and agree that this is not a substitute for professional therapy.",
        value=False
    )
    return consent

def emergency_resources():
    st.error("❌ Consent not given. Redirected to emergency support:")
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
    """Render mic recorder and display chat history."""
    st.success("✅ Consent given. Ready to start.")
    st.markdown("Click on **START** to begin speaking.")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    audio = render_mic_recorder()
    
    if audio:
        st.audio(audio['bytes'], format="audio/webm")
    
    st.info("Click on **STOP** to end the recording.")
    
    st.subheader("Chat History")
    for msg in st.session_state.chat_history:
        if msg.startswith("User:"):
            st.write(f"**You:** {msg[6:]}")
        else:
            st.write(f"**Bot:** {msg[5:]}")
    
    return st.session_state.chat_history

def display_latest_audio():
    """Display the latest recorded audio."""
    if "last_audio" in st.session_state and st.session_state.last_audio:
        st.subheader("Latest Recording")
        st.audio(st.session_state.last_audio, format="audio/webm")