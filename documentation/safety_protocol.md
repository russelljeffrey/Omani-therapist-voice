# Safety Protocol

This document outlines the **safety-first mechanisms** embedded in the chatbot architecture.  
The goal is to ensure **responsible AI deployment** in sensitive mental health contexts.

---


## 1. Emotion Detection

Implemented in `app/models/emotion_detector/detector.py`, the system detects the emotion of the user based on tone, words and over texture of the language. Afterwards, the classifiers evaluates transcripts and emotions to classify the user's emotion. The model can detect the following emotions:

- 'admiration',
- 'amusement',
- 'anger',
- 'annoyance',
- 'approval',
- 'caring',
- 'confusion',
- 'curiosity',
- 'desire',
- 'disappointment',
- 'disapproval',
- 'disgust',
- 'embarrassment',
- 'excitement',
- 'fear',
- 'gratitude',
- 'grief',
- 'joy',
- 'love',
- 'nervousness',
- 'optimism',
- 'pride',
- 'realization',
- 'relief',
- 'remorse',
- 'sadness',
- 'surprise',
- 'neutral'


## 2. Crisis Detection

Implemented in `crisis_detection.py`, the system takes advantage of the user's emotion and evaluates transcripts to classify user risk levels:

- **High Risk:** Explicit suicidal intent.  
- **Medium Risk:** Emotional distress or hopelessness.  
- **Low Risk:** Neutral or positive statements.