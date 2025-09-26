import uuid
import logging
import os
import json
import re
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from app.models.emotion_detector.detector import detect_emotions

logging.basicConfig(
    filename="crisis_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - Session: %(session_id)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def get_session_id():
    """Generate a unique session ID."""
    return str(uuid.uuid4())

def detect_crisis(transcript, emotions):
    """Detect crisis risk based on transcript and emotions using LLM."""
    session_id = st.session_state.get("session_id", get_session_id())
    try:
        api_key = st.session_state.get("openai_api_key") or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("No OpenAI API key found in st.session_state or environment")
        
        llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.3,
            api_key=api_key
        )
        
        prompt_template = PromptTemplate(
            input_variables=["transcript", "emotions"],
            template="""
            You are a mental health crisis detection system. Analyze the following transcript and emotions to determine the crisis risk level (Low, Medium, High) and assign a score between 0.0 and 1.0.
            
            Transcript: {transcript}
            Emotions: {emotions}
            
            Consider linguistic nuances, cultural context (Omani Arabic or English), and emotional intensity. Examples:
            - High Risk: Explicit suicidal intent (e.g., "أفكر في الانتحار", "I want to end my life").
            - Medium Risk: Expressions of sadness, hopelessness, or distress (e.g., "أنا حزين جدًا", "I feel hopeless").
            - Low Risk: Neutral or positive statements (e.g., "أنا بخير", "I'm okay").
            
            Return a JSON object with "crisis_risk" (Low, Medium, High) and "score" (0.0 to 1.0).
            """
        )
        
        emotions_str = ", ".join([f"{e['label']}: {e['score']:.2f}" for e in emotions])
        
        prompt = prompt_template.format(transcript=transcript, emotions=emotions_str)
        logging.info(f"Crisis detection prompt: {prompt}", extra={"session_id": session_id})
        
        response = llm.invoke(prompt)
        logging.info(f"LLM response: {response.content}", extra={"session_id": session_id})
        
        response_text = re.sub(r'^```json\s*|\s*```$', '', response.content, flags=re.MULTILINE).strip()
        logging.info(f"Cleaned LLM response: {response_text}", extra={"session_id": session_id})
        
        try:
            result = json.loads(response_text)
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse LLM response: {response_text}, error: {str(e)}", extra={"session_id": session_id})
            return "Unknown Risk", 0.0
        
        # Map abbreviated risk levels
        risk_mapping = {
            "Low": "Low Risk",
            "Medium": "Medium Risk",
            "High": "High Risk"
        }
        crisis_risk = risk_mapping.get(result.get("crisis_risk", "Unknown Risk"), "Unknown Risk")
        score = float(result.get("score", 0.0))
        
        logging.info(f"Parsed crisis_risk: {crisis_risk}, score: {score:.2f}", extra={"session_id": session_id})
        
        # Adjust score based on emotions
        for emotion in emotions:
            if emotion['label'] in ['sadness', 'fear'] and emotion['score'] > 0.7:
                score = min(score + 0.15, 1.0)
            elif emotion['label'] == 'anger' and emotion['score'] > 0.7:
                score = min(score + 0.1, 1.0)
        
        # Validate score
        score = max(0.0, min(score, 1.0))
        
        logging.info(f"Crisis detection: {crisis_risk}, Score: {score:.2f}", extra={"session_id": session_id})
        
        return crisis_risk, score
    
    except Exception as e:
        logging.error(f"Crisis detection failed: {str(e)}", extra={"session_id": session_id})
        return "Unknown Risk", 0.0