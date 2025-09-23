import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode

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
    st.error("❌ Consent not given. You are redirected to emergency support:")
    st.markdown("## 📞 Emergency Resources in Oman")
    st.markdown("### 🏥 Ministry of Health (MOH)")
    st.markdown("- **General Adult Psychiatry:** +968 2487 3127")
    st.markdown("- **Child & Adolescence Psychiatry:** +968 2487 3127")
    st.markdown("- **Psychology Services:** +968 2487 3983")
    st.markdown("### 🏥 National Hospitals")
    st.markdown("- **Al Masarra Hospital (Psychiatry & Addiction):** +968 2487 3268")
    st.markdown("- **Royal Hospital – Mental Health Support (Mon–Fri, 8 AM–8 PM):** +968 24 607 555")
    st.markdown("### 🏥 Private Hospitals & Clinics")
    st.markdown("- **KIMSHEALTH Oman Hospital (Darsait):** +968 2476 0100 / 200 / 300")
    st.markdown("- **Oman International Hospital (Al Ghubrah):** +968 2490 3500 | WhatsApp: +968 9938 9376 | Email: marketing@omanihospital.com")
    st.markdown("- **Muscat Private Hospital (Al Khuwair):** +968 2458 3600 (operator) / +968 2458 3791 (emergency)")
    st.markdown("- **Aster Al Raffah Hospital (Al Raffah):** +968 2249 6000 | Email: info.oman@asterhospital.com")
    st.markdown("- **Badr Al Samaa Hospital (Al Khoud):** +968 2459 1000 (main switchboard)")
    st.markdown("- **Burjeel Medical Center (Al Azaiba):** +968 24 399 777 | Email: info@bmcoman.com")
    st.markdown("- **Hatat House Polyclinic (Wadi Adai / Al Azaiba):** Tel: +968 2456 3641 / 2456 4367 | Emergency: +968 9943 1173")
    st.markdown("### 🌐 Global Resource")
    st.markdown("- **WHO — Mental Health**: [https://www.who.int/health-topics/mental-health](https://www.who.int/health-topics/mental-health)")
    st.markdown("---")
    st.info("If this is an immediate life-threatening emergency, please call the Royal Oman Police / Ambulance: **9999**.")

def audio_input():
    st.success("✅ Consent given. Starting session...")
    st.markdown("Click on **START** to begin speaking.")
    webrtc_streamer(
        key="speech",
        mode=WebRtcMode.SENDONLY,
        audio_receiver_size=256,
        media_stream_constraints={"audio": True, "video": False},
        
    )

    st.info("Click on **STOP** to end the recording.")