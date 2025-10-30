# uvicorn backend.main:app --host 0.0.0.0 --port 8001

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any
import json
import sys
import os
from sqlalchemy.orm import Session

# ai 모듈 import를 위한 경로 설정
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ai.sentiment import analyze_sentiment
from .database import get_db, engine
from . import models

# 데이터베이스 테이블 생성
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class SurveyResponse(BaseModel):
    answers: Dict[str, Any]
    metadata: Dict[str, Any]

@app.post("/submit")
async def submit_survey(response: SurveyResponse, db: Session = Depends(get_db)):
    try:
        # 감정 분석 수행
        sentiment = analyze_sentiment(str(response.answers))
        
        # 데이터베이스에 저장
        db_response = models.SurveyResponse(
            answers=response.answers,
            sentiment=sentiment
        )
        db.add(db_response)
        db.commit()
        db.refresh(db_response)
        
        return {
            "status": "success",
            "sentiment": sentiment,
            "id": db_response.id
        }
    except Exception as e:
        db.rollback()
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
def get_responses(db: Session = Depends(get_db)):
    try:
        responses = db.query(models.SurveyResponse).order_by(models.SurveyResponse.created_at.desc()).all()
        return responses
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    