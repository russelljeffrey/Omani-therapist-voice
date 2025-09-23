import streamlit as st
from ui import consent_banner, emergency_resources, audio_input

def main():
    st.title("🧠 Omani Therapist Voice Bot (Prototype)")

    if consent_banner():
        audio_input()
        
    else:
        emergency_resources()

if __name__ == "__main__":
    main()