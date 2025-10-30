from typing import Dict, Any
import json
import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# 🔐 환경변수 로드
load_dotenv()

# 환경변수 가져오기
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
OPENAI_API_TYPE = os.getenv("OPENAI_API_TYPE", "azure")
OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION")

# Azure OpenAI 클라이언트 초기화
client = AzureOpenAI(
    api_key=OPENAI_API_KEY,
    api_version=OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)

def analyze_sentiment(text: str) -> Dict[str, Any]:
    """
    Azure OpenAI 기반 감정 분석 함수
    반환 형태: {"sentiment": "positive/negative/neutral", "confidence": 0.85}
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",  # Azure에서 배포한 모델 이름
            messages=[
                {"role": "user", "content": f"Analyze the sentiment of this text: {text}"}
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "sentiment_schema",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "sentiment": {
                                "type": "string",
                                "enum": ["positive", "negative", "neutral"],
                                "description": "감정 분류"
                            },
                            "confidence": {
                                "type": "number",
                                "minimum": 0,
                                "maximum": 1,
                                "description": "분석 신뢰도 (0~1)"
                            }
                        },
                        "required": ["sentiment", "confidence"]
                    }
                }
            },
            temperature=0.3
        )

        result = json.loads(response.choices[0].message.content)
        print(result["sentiment"], result["confidence"], text)
        return {
            "sentiment": result["sentiment"],
            "confidence": result["confidence"],
            "text": text
        }

    except Exception as e:
        return {
            "sentiment": "unknown",
            "confidence": 0.0,
            "text": text,
            "error": str(e)
        }

# 테스트
if __name__ == "__main__":
    sample = "오늘 시험을 잘 봤어요! 정말 기쁩니다."
    result = analyze_sentiment(sample)
    print(sample, result)