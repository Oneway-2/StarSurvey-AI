from sqlalchemy import Column, Integer, String, JSON, DateTime, Text
from sqlalchemy.sql import func
from .database import Base

class SurveyResponse(Base):
    __tablename__ = "survey_responses"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer)
    gender = Column(String(50))
    age_group = Column(String(50))
    feedback = Column(Text)
    sentiment = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __init__(self, answers, sentiment):
        self.rating = answers.get("rating")
        self.gender = answers.get("gender")
        self.age_group = answers.get("age_group")
        self.feedback = answers.get("feedback")
        self.sentiment = sentiment