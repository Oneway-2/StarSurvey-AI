-- survey_results 테이블 생성
CREATE TABLE IF NOT EXISTS survey_results (
    id SERIAL PRIMARY KEY,
    answers JSONB NOT NULL,
    metadata JSONB NOT NULL,
    sentiment JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 인덱스 생성
CREATE INDEX idx_survey_results_created_at ON survey_results(created_at);
CREATE INDEX idx_survey_results_answers ON survey_results USING GIN (answers);
CREATE INDEX idx_survey_results_metadata ON survey_results USING GIN (metadata);

-- 테스트 데이터 삽입
INSERT INTO survey_results (answers, metadata, sentiment)
VALUES (
    '{"rating": 5, "feedback": "아주 좋았습니다!"}',
    '{"mode": "popup", "timestamp": "2025-10-29T10:00:00Z"}',
    '{"sentiment": "positive", "scores": {"positive": 0.8, "neutral": 0.15, "negative": 0.05}}'
);