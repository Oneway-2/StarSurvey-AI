# streamlit run frontend/app2.py

import streamlit as st
import pandas as pd
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

# 페이지 설정
st.set_page_config(page_title="Survey Viewer", layout="wide")

# 감정분석~!!!!!!!!
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


def main():
    st.title("Star Survey AI")

    tabs = st.tabs(["📋 설문 제출", "📊 설문 결과 조회"])

    # Tab 1: 설문 제출
    with tabs[0]:
        with st.form("survey_form"):
            rating = st.slider("별점을 선택해주세요", 1, 5, 3)
            gender = st.radio("성별을 선택해주세요", ["남성", "여성", "기타"])
            age_group = st.slider("나이대를 선택해주세요", 10, 90, 30, step=10)
            feedback = st.text_area("피드백을 입력해주세요", placeholder="여기에 자유롭게 의견을 작성해주세요.")

            submitted = st.form_submit_button("제출")

            if submitted:
                answers = {
                    "rating": rating,
                    "gender": gender,
                    "age_group": age_group,
                    "feedback": feedback
                }

                metadata = {
                    "mode": "Popup",  # survey_mode가 주석 처리되어 있어 임시값 사용
                    "timestamp": str(st.session_state.get("timestamp", ""))
                }

                result = analyze_sentiment(str(answers))                

                if "error" not in result:
                    st.success("설문이 성공적으로 제출되었습니다!")
                    st.write("감정 분석 결과:", result["sentiment"])
                    st.write("신뢰도:", f"{result['confidence']:.2f}")
                else:
                    st.error("설문 제출 중 오류가 발생했습니다.")
                    st.caption(f"오류 내용: {result['error']}")


    # Tab 2: 설문 결과 조회
    with tabs[1]:
        st.subheader("제출된 설문 목록")

        
        # CSV 파일 경로
        CSV_PATH = os.path.join("ai_search", "mock_data.csv")

        # CSV 파일 불러오기
        # try:
        #     df = pd.read_csv(CSV_PATH)
        #     st.success("목업 데이터를 성공적으로 불러왔습니다.")
        # except Exception as e:
        #     st.error(f"데이터를 불러오는 중 오류 발생: {str(e)}")
        #     st.stop()



        # 데이터 미리보기
        # st.subheader("전체 응답 데이터")
        # st.dataframe(df, use_container_width=True)

        # # 선택적 필터링 예시
        # with st.expander("🔍 필터링 옵션"):
        #     selected_sentiment = st.multiselect("감정 선택", options=df["sentiment"].unique())
        #     if selected_sentiment:
        #         df = df[df["sentiment"].isin(selected_sentiment)]
        #         st.write(f"선택된 감정: {selected_sentiment}")

        # # 필터링된 결과 출력
        # st.subheader("📋 필터링된 결과")
        # st.dataframe(df, use_container_width=True)        

if __name__ == "__main__":
    main()