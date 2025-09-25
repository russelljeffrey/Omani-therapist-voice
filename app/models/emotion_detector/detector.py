from transformers import pipeline
import logging

logging.basicConfig(
    filename="crisis_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# GoEmotions human-readable labels
GO_EMOTION_LABELS = [
    "admiration", "amusement", "anger", "annoyance", "approval", "caring", "confusion",
    "curiosity", "desire", "disappointment", "disapproval", "disgust", "embarrassment",
    "excitement", "fear", "gratitude", "grief", "joy", "love", "nervousness",
    "optimism", "pride", "realization", "relief", "remorse", "sadness", "surprise", "neutral"
]

def load_emotion_classifier():
    """Load the emotion detection model."""
    try:
        classifier = pipeline("text-classification", model="AnasAlokla/multilingual_go_emotions_V1.1", framework="pt")
        return classifier
    except Exception as e:
        logging.error(f"Error loading emotion classifier: {str(e)}")
        return None

def detect_emotions(text, classifier):
    """Detect emotions in text with human-readable labels."""
    if not classifier:
        logging.error("Emotion classifier not loaded")
        return [{"label": "error", "score": 0.0}]
    
    raw_results = classifier(text, top_k=3)
    human_results = []
    for item in raw_results:
        raw_label = item['label']
        # Only split if it's in LABEL_X format
        if raw_label.startswith("LABEL_"):
            try:
                idx = int(raw_label.split('_')[1])
                label = GO_EMOTION_LABELS[idx] if idx < len(GO_EMOTION_LABELS) else raw_label
            except (IndexError, ValueError):
                label = raw_label
        else:
            label = raw_label
        human_results.append({"label": label, "score": item['score']})
    return human_results