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

# 이것은 날짜별 report를 전부 읽어내서 요약을 작성해주는 함수이다.
def generate_daily_report(date: str, feedback_list: list[str], total_count: int, avg_rating: float, positive_ratio: float, negative_ratio: float) -> str:
    """선택된 날짜의 피드백을 기반으로 템플릿에 맞춘 AI 보고서 생성"""
    combined_text = "\n".join(feedback_list)

    prompt = f"""
다음은 {date}에 제출된 고객 피드백입니다. 아래 템플릿에 맞춰 보고서를 작성해주세요.

총 응답 수: {total_count}건
평균 별점: {avg_rating:.1f}점
긍정 피드백 비율: {positive_ratio:.0f}%
부정 피드백 비율: {negative_ratio:.0f}%

피드백 목록:
{combined_text}

보고서 템플릿:

# 📊 고객 피드백 요약 보고서 ({date} 기준)

## 🗓️ 분석 대상
- 날짜: {date}
- 총 응답 수: {total_count}건
- 평균 만족도: ★★★☆☆ (평균 별점: {avg_rating:.1f}점)

---

## 😊 고객이 긍정적으로 평가한 점

다음은 고객들이 만족스럽다고 평가한 주요 항목입니다:

- ✅ **친절한 직원 응대**  
  예: ...
- ✅ **서비스의 편리함과 결과 만족도**  
  예: ...
- ✅ **기대 이상의 경험**  
  예: ...

---

## ⚠️ 개선이 시급한 문제점

다음은 고객들이 불만을 표시하거나 조치가 필요한 항목입니다:

- ❌ **기능 오류 및 시스템 문제**  
  예: ...
- ❌ **불친절한 응대 및 고객 지원 부족**  
  예: ...
- ❌ **재방문 의사 없음 및 강한 불만**  
  예: ...

---

## 📌 요약 인사이트

- 긍정 피드백 비율: {positive_ratio:.0f}%
- 부정 피드백 비율: {negative_ratio:.0f}%
- 주요 만족 요인: [친절함, 편리함, 결과 만족도]
- 주요 불만 요인: [기능 오류, 고객 응대, 속도 문제]

---

## 🧠 AI 추천 액션

- 고객 응대 품질 향상을 위한 교육 강화
- 기능 오류 및 속도 개선을 위한 기술 점검
- 불만 고객 대상 사후 만족도 회복 프로그램 운영

---

보고서 생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M')}
분석 모델: Azure OpenAI 기반 감정 분석 + 키워드 요약
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content


def main():
    st.title("Star Survey AI")

    tabs = st.tabs(["📊 설문 결과 조회", "📋 설문 제출"])

    # Tab 1: 설문 제출
    with tabs[1]:
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
    with tabs[0]:
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

            # 검색을 실행중임~~
            with st.spinner("데이터를 불러오는 중입니다..."):
                # 검색 실행
                results = list(search_client.search(
                    search_text="*",
                    order_by=order_by,
                    select="id,timestamp,rating,gender,age_group,feedback"
                ))

            # 날짜 목록 추출
            date_list = sorted({doc['timestamp'][:10] for doc in results})
            selected_date = st.selectbox("조회할 날짜를 선택하세요", date_list)
            # 선택된 날짜에 해당하는 설문만 필터링
            filtered_results = [doc for doc in results if doc['timestamp'].startswith(selected_date)]

            # 통계 정보 표시
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("총 응답 수", len(filtered_results))
            with col2:
                avg_rating = sum(doc.get('rating', 0) for doc in filtered_results) / len(filtered_results) if filtered_results else 0
                st.metric("평균 별점", f"{avg_rating:.1f}")
            with col3:
                positive_count = sum(1 for doc in filtered_results if doc.get('rating', 0) >= 4)
                st.metric("긍정적 응답", f"{positive_count}개")

            ############# 보고서 추출부분
            # 피드백만 추출
            feedback_texts = [doc.get("feedback", "") for doc in filtered_results if doc.get("feedback")]
            ratings = [doc.get("rating", 0) for doc in filtered_results]

            # 통계 계산
            total_count = len(filtered_results)
            avg_rating = sum(ratings) / total_count if total_count else 0
            positive_ratio = sum(1 for r in ratings if r >= 4) / total_count * 100 if total_count else 0
            negative_ratio = sum(1 for r in ratings if r <= 2) / total_count * 100 if total_count else 0

            # 보고서 생성
            if feedback_texts:
                with st.spinner("AI가 보고서를 생성 중입니다..."):
                    report = generate_daily_report(
                        date=selected_date,
                        feedback_list=feedback_texts,
                        total_count=total_count,
                        avg_rating=avg_rating,
                        positive_ratio=positive_ratio,
                        negative_ratio=negative_ratio
                    )
                    st.markdown("### 📝 고객 피드백 요약 보고서")
                    st.markdown(report)
            ############# 보고서 추출부분

            # 결과 표시
            with st.expander(f"📋 검색된 설문 응답 전부 보기 ({total_count}개)", expanded=False):
            # st.markdown("### 📋 검색된 설문 응답")
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