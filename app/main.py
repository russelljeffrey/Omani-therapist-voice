import streamlit as st
from ui import consent_banner, emergency_resources, audio_input, display_latest_audio
import config

def main():
    st.set_page_config(page_title="Omani Therapist Voice Bot", layout="wide")
    st.title("🧠 Omani Therapist Voice Bot (Prototype)")
    
    if not config.OPENAI_API_KEY:
        st.error("OpenAI API key not found in .env file. Please set OPENAI_API_KEY.")
        emergency_resources()
        return
    
    if consent_banner():
        chat_history = audio_input()
        display_latest_audio()
        
        # Placeholder for chatbot response
        if chat_history and chat_history[-1].startswith("User:"):
            # Example: Uncomment to enable LLM response
            # from stt_pipeline import client
            # response = client.chat.completions.create(
            #     model="gpt-3.5-turbo",
            #     messages=[
            #         {"role": "system", "content": "You are a supportive therapist bot."},
            #         {"role": "user", "content": chat_history[-1].split("User: ")[1]}
            #     ]
            # )
            # chat_history.append(f"Bot: {response.choices[0].message.content}")
            # st.rerun()
            st.info("🤖 Bot response would go here (uncomment in code to enable).")
    
    else:
        emergency_resources()

if __name__ == "__main__":
    main()