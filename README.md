# 🧠 Star Survey AI

Star(별점 , 만족도) + Survey(설문) + AI

수집된 만족도 설문 응답에 대한 리포트를 작성해주는 애플리케이션입니다. 

---

## 🤩 이 것을 고안한 이유
- 대고객으로부터 서비스 만족도를 받는 것은 서비스의 질을 향상시키는데 큰 도움이 됨
- 수집된 만족도 설문 내용을 모두 일일히 검토하는건 고된 일.
- 매일 00시, 하루동안 모인 설문 내용을 수집하고 AI가 그것을 요약해서 어떤 중요한 피드백이 있었는지 한눈에 제공하면 좋겠다는 생각이 들었음.
---
- 현재 프로토타입에는 구성되어있지 않지만,
- 관리자용 설문 설계 portal 이 있고, 그곳에서 관리자는 질문을 정할 수 있음.

<img src="image/설문페이지_prototype_이미지.png" alt="설문페이지 프로토타입" width="50%" />


## 🚀 주요 기능

### 📋 설문 제출 팝업 제공
- 성별, 나이대, 별점, 자유 피드백을 입력받는다.

### 📊 설문 결과 조회
- Azure Cognitive Search를 통해 저장된 설문 응답 조회
- 날짜별로 필터링 가능
- 별점 기준 정렬 (최신순, 높은순, 낮은순)
- 각 응답은 토글 형태로 펼쳐보기 가능

### 📝 AI 보고서 생성
- 선택된 날짜의 피드백을 기반으로 AI가 자동 요약 보고서 생성
- 긍정적 평가, 개선 필요 사항, 인사이트, 추천 액션 포함
- 템플릿 기반 Markdown 보고서 출력

### 📧 이메일 전송
- 생성된 보고서를 이메일로 전송 가능
- 이메일 주소 입력 후 버튼 클릭으로 전송 처리

---

## 🛠️ 기술 스택

- **Frontend**: Streamlit
- **Backend AI**: Azure OpenAI (GPT-4.1-mini)
- **Search & Storage**: Azure Cognitive Search
- **Deployment**: Azure App Service (Linux)
- **Email**: SMTP (Gmail 기반)

---

## ⚙️ 환경 설정 (.env)

```env
OPENAI_API_KEY=your_openai_key
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
OPENAI_API_VERSION=2023-07-01-preview
SEARCH_ENDPOINT=https://your-search-endpoint.search.windows.net
SEARCH_API_KEY=your_search_key
INDEX_NAME=survey-index
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

---
## ⚙️ Trouble Shooting