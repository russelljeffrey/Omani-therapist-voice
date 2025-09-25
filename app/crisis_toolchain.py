from transformers import pipeline
import logging
import streamlit as st
import uuid

logging.basicConfig(
    filename="crisis_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - Session: %(session_id)s - %(message)s"
)

CRISIS_LABEL_MAPPING = {
    "LABEL_0": "Low / No Risk",
    "LABEL_1": "High Risk",
    "low_risk": "Low / No Risk",
    "medium_risk": "Medium Risk",
    "high_risk": "High Risk",
    "suicide": "High Risk",
    "not_suicide": "Low / No Risk"
}

def load_crisis_detector():
    """Load the crisis detection model."""
    try:
        detector = pipeline("text-classification", model="sentinet/suicidality", framework="pt")
        return detector
    except Exception as e:
        logging.error(f"Error loading crisis detector: {str(e)}", extra={"session_id": get_session_id()})
        return None

crisis_detector = load_crisis_detector()

def get_session_id():
    """Get or create anonymized session ID."""
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    return st.session_state.session_id

def detect_crisis(transcript, emotions):
    """Detect crisis signals, consider cumulative risk, and log high/medium risk."""
    if not crisis_detector:
        logging.error("Crisis detector not loaded", extra={"session_id": get_session_id()})
        return {"label": "error", "score": 0.0}
    
    session_id = get_session_id()
    
    raw_result = crisis_detector(transcript)[0]
    raw_label = raw_result['label']
    score = raw_result['score']
    
    label = CRISIS_LABEL_MAPPING.get(raw_label, raw_label)
    
    crisis_risk = {"label": label, "score": score}
    
    crisis_keywords = ["انتحار", "ما أبغى أعيش", "قتل نفسي", "suicide", "kill myself", "life is not worth living"]
    if any(kw in transcript.lower() for kw in crisis_keywords):
        crisis_risk = {"label": "High Risk", "score": 0.95}
    
    # Cumulative risk
    negative_emotions = ["sadness", "grief", "fear", "remorse", "anger", "disappointment"]
    if "emotion_history" not in st.session_state:
        st.session_state.emotion_history = []
    
    # Append top emotion
    if emotions:
        top_emotion = emotions[0]["label"]
        st.session_state.emotion_history.append(top_emotion)
    
    # Check if negative emotions dominate recent inputs
    recent_emotions = st.session_state.emotion_history[-3:]  # Last 3 inputs
    negative_count = sum(1 for emo in recent_emotions if emo in negative_emotions)
    if negative_count >= 2 and crisis_risk["label"] != "High Risk":
        crisis_risk = {"label": "Medium Risk", "score": max(crisis_risk["score"], 0.85)}
    
    # Log high/medium risk with detailed context
    if crisis_risk["label"] in ["High Risk", "Medium Risk"] and crisis_risk["score"] > 0.8:
        logging.info(
            f"Crisis detected: Transcript='{transcript}' | Risk={crisis_risk['label']} | Score={crisis_risk['score']:.2f} | Emotions={emotions} | Emotion History={st.session_state.emotion_history}",
            extra={"session_id": session_id}
        )
    
    return crisis_risk