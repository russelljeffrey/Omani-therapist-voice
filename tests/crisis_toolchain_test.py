import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

import pytest
from app.crisis_toolchain import detect_crisis, get_session_id
from app.intent_analysis import analyze_intent

def test_crisis_detection_low_risk():
    """Test low-risk input."""
    transcript = "أشعر بالبهجة اليوم. كان اجتماعًا مثمرًا وأريد مساعدة الناس. أنا متفائل جدًا."
    emotions, _ = analyze_intent(transcript)
    crisis_risk, score = detect_crisis(transcript, emotions)
    assert crisis_risk == "Low Risk", f"Expected Low Risk, got {crisis_risk}"
    assert score < 0.5, f"Expected score < 0.5, got {score}"
    positive_emotions = ["positive", "joy", "happiness", "optimism", "cheerfulness", "positive_sentiment", "فرح"]
    assert any(e["label"] in positive_emotions for e in emotions), f"Expected one of {positive_emotions}, got {emotions}"

def test_crisis_detection_medium_risk():
    """Test medium-risk input."""
    transcript = "تتزايد نوبات القلق لدي لدرجة أنني بدأت أتجنب المناسبات الاجتماعية، وأجد صعوبة بالغة في التركيز على عملي أو هواياتي المعتادة."
    emotions, _ = analyze_intent(transcript)
    crisis_risk, score = detect_crisis(transcript, emotions)
    assert crisis_risk == "Medium Risk", f"Expected Medium Risk, got {crisis_risk}"
    assert 0.5 <= score <= 0.8, f"Expected score between 0.5 and 0.75, got {score}"
    assert any(e["label"] == "sadness" for e in emotions), "Expected sadness emotion"

def test_crisis_detection_high_risk():
    """Test high-risk input."""
    transcript = "أشعر باليأس التام وفقدت كل رغبة في الحياة، ولدي خطة واضحة لإيذاء نفسي وأفكر جدياً في تنفيذها الآن."
    emotions, _ = analyze_intent(transcript)
    crisis_risk, score = detect_crisis(transcript, emotions)
    assert crisis_risk == "High Risk", f"Expected High Risk, got {crisis_risk}"
    assert score > 0.8, f"Expected score > 0.8, got {score}"
    assert any(e["label"] == "fear" or e["label"] == "sadness" for e in emotions), "Expected fear or sadness emotion"

def test_session_id_uniqueness():
    """Test that session IDs are unique."""
    session_id1 = get_session_id()
    session_id2 = get_session_id()
    assert session_id1 != session_id2, "Session IDs should be unique"