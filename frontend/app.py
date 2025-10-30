import streamlit as st
import requests
from typing import Dict, Any

# 설정
API_URL = "http://localhost:8001"  # FastAPI 서버 주소

def submit_survey(answers: Dict[str, Any], metadata: Dict[str, Any]):
    response = requests.post(
        f"{API_URL}/submit",
        json={"answers": answers, "metadata": metadata}
    )
    return response.json()

def main():
    st.title("Star Survey AI")
    
    # 설문 모드 선택 (팝업/포털)
    # survey_mode = st.sidebar.radio(
    #     "Survey Mode",
    #     ["Popup", "Portal"]
    # )

    # if st.button("팝업 열기"):
    #     with st.modal("팝업 제목"):
    #         # st.write("여기에 팝업 내용을 작성하세요.")
    #         st.button("닫기")

    
    # 설문 폼
    with st.form("survey_form"):        
        # 별점입력
        rating = st.slider("별점을 선택해주세요", 1, 5, 3)
        # 성별입력
        gender = st.radio(
            "성별을 선택해주세요",
            ["남성", "여성", "기타"]
        )
        # 나이대 입력
        age_group = st.slider(
            "나이대를 선택해주세요",
            min_value=10,
            max_value=90,
            step=10,
            value=30
        )
        # 자유응답입력
        feedback = st.text_area(
            "피드백을 입력해주세요",
            placeholder="여기에 자유롭게 의견을 작성해주세요."
        )
        
        # 제출 버튼
        submitted = st.form_submit_button("제출")
        
        if submitted:
            # 응답 데이터 구성
            answers = {
                "rating": rating,
                "gender": gender,
                "age_group": age_group,     
                "feedback": feedback
            }
            
            metadata = {
                "mode": survey_mode,
                "timestamp": str(st.session_state.get("timestamp", ""))
            }
            
            # API 호출
            result = submit_survey(answers, metadata)
            
            # 결과 표시
            if result.get("status") == "success":
                st.success("설문이 성공적으로 제출되었습니다!")
                st.write("감정 분석 결과:", result.get("sentiment"))
            else:
                st.error("설문 제출 중 오류가 발생했습니다.")

if __name__ == "__main__":
    main()