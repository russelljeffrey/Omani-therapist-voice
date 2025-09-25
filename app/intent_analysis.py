from models.emotion_detector.detector import load_emotion_classifier, detect_emotions

emotion_classifier = load_emotion_classifier()

INTENT_MAPPING = {
    "seeking_resources": "Looking for support or resources",
    "venting_emotions": "Expressing feelings or stress",
    "unknown": "Talking about daily life / feelings"
}

def analyze_intent(transcript):
    """Analyze emotions and intent in transcript."""
    # Emotion Detection
    emotions = detect_emotions(transcript, emotion_classifier)
    
    # Rule-based Intent Classification
    intent = "unknown"
    keywords = {
        "seeking_resources": ["therapist", "muscat", "help", "support", "معالج", "مسقط", "مساعدة", "دعم", "استشارة"],
        "venting_emotions": ["sad", "depressed", "anxiety", "حزين", "اكتئاب", "قلق", "توتر", "stress", "ضيق"]
    }
    transcript_lower = transcript.lower()
    for intent_type, kw_list in keywords.items():
        if any(kw in transcript_lower for kw in kw_list):
            intent = intent_type
            break
    
    # Map to human-readable description
    intent_description = INTENT_MAPPING.get(intent, INTENT_MAPPING["unknown"])
    
    return emotions, intent_description