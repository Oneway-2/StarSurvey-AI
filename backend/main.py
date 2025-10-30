from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import json
import sys
import os

# ai 모듈 import를 위한 경로 설정
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ai.sentiment import analyze_sentiment

app = FastAPI()

class SurveyResponse(BaseModel):
    answers: Dict[str, Any]
    metadata: Dict[str, Any]

@app.post("/submit")
async def submit_survey(response: SurveyResponse):
    try:
        # 감정 분석 수행
        sentiment = analyze_sentiment(str(response.answers))
        
        # TODO: DB 저장 로직 구현
        
        return {
            "status": "success",
            "sentiment": sentiment
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/results/{survey_id}")
async def get_survey_results(survey_id: str):
    try:
        # TODO: DB 조회 로직 구현
        return {
            "status": "success",
            "data": {
                "survey_id": survey_id,
                "results": []  # DB에서 조회한 결과
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/responses")
def get_responses():
    return list(db.query(SurveyResponse).order_by(SurveyResponse.reg_dt.desc()).all())    