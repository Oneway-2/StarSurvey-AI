# streamlit run frontend/app.py

import streamlit as st
import requests
from typing import Dict, Any, List

# 설정
API_URL = "http://localhost:8001"  # FastAPI 서버 주소

def submit_survey(answers: Dict[str, Any], metadata: Dict[str, Any]):
    response = requests.post(
        f"{API_URL}/submit",
        json={"answers": answers, "metadata": metadata}
    )
    return response.json()

def fetch_responses() -> List[Dict[str, Any]]:
    try:
        response = requests.get(f"{API_URL}/responses")
        data = response.json()

        # 응답이 문자열 리스트인 경우 → 변환 또는 무시
        if isinstance(data, list) and all(isinstance(item, str) for item in data):
            st.warning("서버에서 설문 데이터를 문자열로 반환하고 있어요. JSON 객체로 반환되도록 수정이 필요합니다.")
            return []

        return data
    except Exception as e:
        st.error(f"설문 결과를 불러오는 중 오류 발생: {e}")
        return []


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

                result = submit_survey(answers, metadata)

                if result.get("status") == "success":
                    st.success("설문이 성공적으로 제출되었습니다!")
                    st.write("감정 분석 결과:", result.get("sentiment"))
                else:
                    st.error("설문 제출 중 오류가 발생했습니다.")

    # Tab 2: 설문 결과 조회
    with tabs[1]:
        st.subheader("제출된 설문 목록")
        responses = fetch_responses()

        if responses:
            for r in responses:
                st.markdown("---")
                st.write(f"🕒 등록일시: {r.get('reg_dt', 'N/A')}")
                st.write(f"⭐ 별점: {r.get('rating')}")
                st.write(f"👤 성별: {r.get('gender')}")
                st.write(f"🎂 나이대: {r.get('age_group')}")
                st.write(f"💬 피드백: {r.get('feedback')}")
                st.write(f"🧠 감정 분석: {r.get('sentiment')}")
        else:
            st.info("아직 제출된 설문이 없습니다.")

if __name__ == "__main__":
    main()