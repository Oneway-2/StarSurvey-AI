# from sqlalchemy import Column, Integer, String, JSON, DateTime, Text
# from sqlalchemy.sql import func
# from .database import Base

# class SurveyResponse(Base):
#     __tablename__ = "survey_responses"

#     id = Column(Integer, primary_key=True, index=True)
#     rating = Column(Integer)
#     gender = Column(String(50))
#     age_group = Column(String(50))
#     feedback = Column(Text)
#     sentiment = Column(JSON)         # 감정 분석 결과 전체 저장
#     reg_dt = Column(DateTime(timezone=True), server_default=func.now())  # 등록일시

#     # 생성자 제거: SQLAlchemy는 기본 생성자 사용을 권장