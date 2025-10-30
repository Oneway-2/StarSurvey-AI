# streamlit run frontend/app2.py

import streamlit as st
import pandas as pd
from typing import Dict, Any
import json
import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from datetime import datetime
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential



# 🔐 환경변수 로드
load_dotenv()

# 환경변수 가져오기
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
OPENAI_API_TYPE = os.getenv("OPENAI_API_TYPE", "azure")
OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION")
SEARCH_ENDPOINT = os.getenv("SEARCH_ENDPOINT")
SEARCH_API_KEY = os.getenv("SEARCH_API_KEY")
INDEX_NAME = os.getenv("INDEX_NAME")


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
    반환 형태: {"감정 분류": "긍정/부정/평안/슬픔/화남", "정확도": "85%", "원문": text}
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "user", "content": f"다음 텍스트의 감정을 분류해줘. 감정은 긍정, 부정, 평안, 슬픔, 화남 중 하나여야 하고, 신뢰도는 0~1 사이 숫자로 줘. 텍스트: {text}"}
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
                                "enum": ["긍정", "부정", "평안", "슬픔", "화남"],
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
        sentiment = result["sentiment"]
        confidence_percent = f"{int(result['confidence'] * 100)}%"
        print(f"감정 분류: {sentiment}, 정확도: {confidence_percent}, 원문: {text}")

        return {
            "감정 분류": sentiment,
            "정확도": confidence_percent,
            "원문": text
        }

    except Exception as e:
        return {
            "감정 분류": "분석 실패",
            "정확도": "0%",
            "원문": text,
            "오류": str(e)
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
                    "feedback": feedback,
                    "timestamp": datetime.now().isoformat()
                }

                result = analyze_sentiment(str(answers))                

                if "error" not in result:
                    st.success("설문이 성공적으로 제출되었습니다!")
                    st.write("감정 분석 결과:", result["감정 분류"])
                    st.write("신뢰도:", result["정확도"])

                    st.markdown(f"**🧠 감정 분류:** {result['감정 분류']}")
                    st.markdown(f"**📈 정확도:** {result['정확도']}")                    
                else:
                    st.error("설문 제출 중 오류가 발생했습니다.")
                    st.caption(f"오류 내용: {result['오류']}")




    # Tab 2: 설문 결과 조회
    with tabs[1]:
        st.subheader("제출된 설문 목록")        

        try:
            # Azure Search 클라이언트 초기화
            search_client = SearchClient(
                endpoint=SEARCH_ENDPOINT,
                index_name=INDEX_NAME,
                credential=AzureKeyCredential(SEARCH_API_KEY)
            )
            
            # 정렬 옵션
            sort_option = st.selectbox(
                "정렬 기준",
                ["별점 낮은순", "별점 높은순", "최신순"],
                index=0
            )
            
            # 정렬 기준 설정
            if sort_option == "최신순":
                order_by = "timestamp desc"
            elif sort_option == "별점 높은순":
                order_by = "rating desc"
            else:  # 별점 낮은순
                order_by = "rating asc"

            # 검색 실행
            results = list(search_client.search(
                search_text="*",
                order_by=order_by,
                select="id,timestamp,rating,gender,age_group,feedback"
            ))

            # 통계 정보 표시
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("총 응답 수", len(results))
            with col2:
                avg_rating = sum(doc.get('rating', 0) for doc in results) / len(results) if results else 0
                st.metric("평균 별점", f"{avg_rating:.1f}")
            with col3:
                positive_count = sum(1 for doc in results if doc.get('rating', 0) >= 4)
                st.metric("긍정적 응답", f"{positive_count}개")

            # 결과 표시
            st.markdown("### 📋 검색된 설문 응답")
            if not results:
                st.info("검색된 설문 응답이 없습니다.")
            
            for doc in results:
                with st.expander(f"⭐ {doc.get('rating')}점 | {doc.get('feedback')[:30]}...", expanded=True):
                    st.markdown(f"**🕒 시간:** {doc.get('timestamp', 'N/A')}")
                    st.markdown(f"**⭐ 별점:** {doc.get('rating', 'N/A')}")
                    st.markdown(f"**👤 성별:** {doc.get('gender', 'N/A')}")
                    st.markdown(f"**🎂 나이대:** {doc.get('age_group', 'N/A')}")
                    st.markdown(f"**💬 피드백:** {doc.get('feedback', 'N/A')}")

        except Exception as e:
            st.error(f"데이터 조회 중 오류가 발생했습니다: {str(e)}")
            st.write("상세 오류:", e.__class__.__name__)

if __name__ == "__main__":
    main()