-- survey_results 테이블 생성
CREATE TABLE IF NOT EXISTS survey_responses (
    id SERIAL PRIMARY KEY,
    rating SMALLINT NOT NULL,
    gender VARCHAR(10) NOT NULL,
    age_group SMALLINT NOT NULL,
    feedback TEXT,
    sentiment VARCHAR(20),
    reg_dt TIMESTAMPTZ DEFAULT NOW()
);

-- 인덱스 생성
-- 날짜 기반 조회 (오늘 응답 수, 최근 데이터 등)
CREATE INDEX idx_survey_reg_dt ON survey_responses (reg_dt);


-- 테스트 데이터 삽입
-- INSERT INTO survey_results (answers, metadata, sentiment)
-- VALUES (
--     '{"rating": 5, "feedback": "아주 좋았습니다!"}',
--     '{"mode": "popup", "timestamp": "2025-10-29T10:00:00Z"}',
--     '{"sentiment": "positive", "scores": {"positive": 0.8, "neutral": 0.15, "negative": 0.05}}'
-- );