import os
import logging
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from app.models.emotion_detector.detector import load_emotion_classifier, detect_emotions

logging.basicConfig(
    filename="crisis_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - Session: %(session_id)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

emotion_classifier = load_emotion_classifier()

INTENT_MAPPING = {
    "seeking_resources": "Looking for support or resources",
    "venting_emotions": "Expressing feelings or stress",
    "unknown": "Talking about daily life / feelings"
}

def analyze_intent(transcript, session_id="unknown"):
    """Analyze emotions and intent in transcript using LLM."""
    emotions = detect_emotions(transcript, emotion_classifier)
    logging.info(f"Emotions detected: {emotions}", extra={"session_id": session_id})
    
    # LLM-based Intent Classification
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("No OpenAI API key found in environment")
        
        llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.3,
            api_key=api_key
        )
        
        prompt_template = PromptTemplate(
            input_variables=["transcript"],
            template="""
            You are an intent classification system for a mental health voice bot. Analyze the following transcript to determine the user's intent. Choose one of the following intents:
            - seeking_resources: User is looking for support, resources, or help (e.g., "I need a therapist in Muscat", "أحتاج معالج في مسقط").
            - venting_emotions: User is expressing emotions like sadness, stress, or anxiety (e.g., "I'm so sad", "أنا حزين جدًا").
            - unknown: User is talking about daily life or neutral topics (e.g., "Today was a good day", "اليوم كان جيدًا").
            
            Consider linguistic nuances and cultural context (Omani Arabic or English). Return only the intent name (seeking_resources, venting_emotions, or unknown).
            
            Transcript: {transcript}
            """
        )
        
        prompt = prompt_template.format(transcript=transcript)
        logging.info(f"Intent classification prompt: {prompt}", extra={"session_id": session_id})
        
        response = llm.invoke(prompt)
        intent = response.content.strip()
        logging.info(f"LLM intent response: {intent}", extra={"session_id": session_id})
        
        # Validate intent
        if intent not in INTENT_MAPPING:
            logging.warning(f"Invalid intent '{intent}' detected, defaulting to 'unknown'", extra={"session_id": session_id})
            intent = "unknown"
        
    except Exception as e:
        logging.error(f"Intent classification failed: {str(e)}", extra={"session_id": session_id})
        intent = "unknown"
    
    # Map to human-readable description
    intent_description = INTENT_MAPPING.get(intent, INTENT_MAPPING["unknown"])
    logging.info(f"Intent classified: {intent_description}", extra={"session_id": session_id})
    
    return emotions, intent_description