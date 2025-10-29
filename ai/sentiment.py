from typing import Dict, Any
import random

def analyze_sentiment(text: str) -> Dict[str, Any]:
    """
    간단한 더미 감정 분석 함수
    실제 프로덕션에서는 감정 분석 모델로 대체
    """
    # 더미 감정 분석 결과
    sentiments = ["positive", "neutral", "negative"]
    scores = {
        "positive": random.uniform(0.0, 1.0),
        "neutral": random.uniform(0.0, 1.0),
        "negative": random.uniform(0.0, 1.0)
    }
    
    # 가장 높은 점수의 감정을 선택
    predicted_sentiment = max(scores, key=scores.get)
    
    return {
        "sentiment": predicted_sentiment,
        "scores": scores,
        "text": text
    }