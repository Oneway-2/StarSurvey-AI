# # uvicorn backend.main:app --host 0.0.0.0 --port 8001 --reload
# # uvicorn backend.main:app --host 0.0.0.0 --port 8001 --reload --log-level debug

# from fastapi import FastAPI, HTTPException, Depends
# from pydantic import BaseModel
# from typing import Dict, Any
# import json
# import sys
# import os
# from sqlalchemy.orm import Session
# from sqlalchemy import text
# import traceback


# # ai 모듈 import를 위한 경로 설정
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from ai.sentiment import analyze_sentiment
# from backend.database import get_db, engine
# from backend import models

# # 데이터베이스 테이블 생성
# models.Base.metadata.create_all(bind=engine)

# app = FastAPI()

# class SurveyResponse(BaseModel):
#     answers: Dict[str, Any]
#     metadata: Dict[str, Any]

# @app.post("/submit")
# async def submit_survey(response: SurveyResponse, db: Session = Depends(get_db)):
#     print("받은응답머야:", response)
#     try:
#         # 감정 분석 수행
#         sentiment = analyze_sentiment(str(response.answers))
        
#         # 데이터베이스 저장
#         try:
#             db_response = models.SurveyResponse(
#                 rating=response.answers.get("rating"),
#                 gender=response.answers.get("gender"),
#                 age_group=response.answers.get("age_group"),
#                 feedback=response.answers.get("feedback"),
#                 sentiment=sentiment,
#             )

#             db.add(db_response)
#             db.commit()
#             db.refresh(db_response)

#         except Exception as e:
#             print(traceback.format_exc())  # 상세 에러 로그 출력
#             db.rollback()
#             raise HTTPException(status_code=500, detail=f"DB 저장 실패: {str(e)}")
        
#         return {
#             "status": "success",
#             "sentiment": sentiment,
#             "id": db_response.id
#         }
    
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))
    
# @app.get("/responses")
# def get_responses(db: Session = Depends(get_db)):
#     try:
#         responses = db.query(models.SurveyResponse).order_by(models.SurveyResponse.reg_dt.desc()).all()
#         return responses
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))    

# @app.get("/results/{survey_id}")
# async def get_survey_results(survey_id: str, db: Session = Depends(get_db)):
#     try:
#         result = db.query(models.SurveyResponse).filter(models.SurveyResponse.id == survey_id).first()
#         if not result:
#             raise HTTPException(status_code=404, detail="Survey not found")
#         return {
#             "status": "success",
#             "data": result
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/db-test")
# async def test_db_connection(db: Session = Depends(get_db)):
#     try:
#         db.execute(text("SELECT 1"))
#         return {"status": "success", "message": "Database connection successful"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")



