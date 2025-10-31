# 🧠 Star Survey AI - 별점 만족도 설문 리포트 제공 서비스

## 🤩 이 것을 고안한 이유
- 대고객으로부터 서비스 만족도를 받는 것은 서비스의 질을 향상시키는데 큰 도움이 됨
- 수집된 만족도 설문 내용을 모두 일일히 검토하는건 고된 일.
- 매일 00시, 하루동안 모인 설문 내용을 수집하고 AI가 그것을 요약해서 어떤 중요한 피드백이 있었는지 한눈에 제공하면 좋겠다는 생각이 들었음.
---
- 관리자용 설문 설계 portal 이 있고, 그곳에서 관리자는 질문 가능.
<br>

<img src="image/1.png" alt="설문페이지 프로토타입" width="50%" />
<img src="image/2.png" alt="설문페이지 프로토타입" width="50%" />

## ✨ 비지니스 모델
- 편리하게 UI상에서 설문에 대한 설계를 하고, 결과를 분석해서 이메일로 받을 수 있는 서비스를 제공하는 대가로
- <b>구독료 받기</b>
- 설문 팝업 아래 광고 배너 삽입

## 🚀 주요 기능

### 📋 설문 관리자 페이지 제공 (추후개발)
- 설문을 설계하고, 관리자는 수집된 만족도를 조회할 수 있는 포탈 제공

### 📋 설문 제출 팝업 제공
- 성별, 나이대, 별점, 자유 피드백을 입력받는다.

### 📝 AI 보고서 생성
- 선택된 날짜의 피드백을 기반으로 AI가 자동 요약 보고서 생성
- 긍정적 평가, 개선 필요 사항, 인사이트, 추천 액션 포함
- 템플릿 기반 Markdown 보고서 출력

### 📧 이메일 전송 (추후개발)
- 매일 00시, 전일 수집된 응답을 기반으로 보고서를 제작
- 이메일로 발송할 수 있도록 기능 제공

---

## 🛠️ 기술 스택

- **Frontend**: Streamlit --> ***[추후 React/Typescript 등으로 개선]***
- **Backend AI**: Azure OpenAI (GPT-4.1-mini)
- **Search & Storage**: Azure Cognitive Search --> ***[추후 PostgreSQL, Redis 등 사용하여 성능개선]***
- **Deployment**: Azure App Service (Linux) --> ***[추후 AKS, Github action, ArgoCD 등 배포 편리성 및 스케일링 관리 개선]***
- **Email**: SMTP

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
```

## 의존성
```
streamlit
pandas
python-dotenv
openai
azure-search-documents
azure-core
```
---
## 개선방향 
### 1. 모듈화
- 현재 streamlit 코드 내 모든 소스코드가 모여있어, 소스코드가 너무 길어짐.
- 이것을 UI로직, 백엔드로직 등으로 분리하여 여러 class형태로 나누어 사용하면 유지관리가 편리할 것.
### 2. 저장소 사용
- 설문을 저장할 저장소, 하루치 응답량을 모아 작성된 리포트 템플릿을 저장할 저장소를 위한 DB구성
- 하루치 데이터별로 Azure Storage account 나 , Azure AI Search 내에 indexes로 넣어두어도 좋을 듯.
- 버전별 컨테이너화 한 이미지 registry 구성
### 3. 배포
- AKS 사용하여 기능별로 컨테이너로 관리
  - 설문 관리 포탈 UI (FE/BE)
  - 설문 팝업(FE/BE)
  - 00시 데이터 취합 및 보고서 작성 스케쥴러
### 4. 응답 다양성/정확도 개선
- DB로부터 주관식 응답만 받고 prompt 템플릿을 통해 보고서형태의 응답을 도출하도록 하였으나
- 나이, 성별, yes/no 2지선다 응답 등 더 많은 정보를 토대로 다채로운 답변을 보낼 수 있도록 개선
- 설문 응답량이 엄청 많이 들어오는경우 쿼리 데이터를 chunk 하는 방법 고안

---
## 💢 Trouble Shooting
- <b>Github action - Azure App service를 통한 web app 배포간에 package 형태로 배포되어 root 경로에 startup.sh 를 찾지못함 </b>
  - 환경변수 SCM_DO_BUILD_DURING_DEPLOYMENT 와, WEBSITE_RUN_FROM_PACKAGE 값을 0으로 바꾸어 해결
    - SCM_DO_BUILD_DURING_DEPLOYMENT --> 배포 후 Azure가 빌드하는 것을 막음. github aciton 내 자체적으로 빌드를 수행하기에.
    - WEBSITE_RUN_FROM_PACKAG --> Azure은 ZIP 패키지를 실행하는 기능을 자체적으로 갖고있는데, 계속 tar.gz 파일로 압축이 돼서 기능 해제함. 

- <b>DB 연동 실패 </b>
  - PostgreSQL 연동하고 날짜별 데이터 select 하여 사용하려고 하였으나 python, azure 경험 부족으로 사용 철회하고
  - mockup 데이터 생성하여 Azure AI Search 내 indexes로 넣어놓고 호출하여 사용.

- <b>Azure AI Search를 이용한 목업파일 업로드 </b>
  - Mockup 데이터 csv 파일로 생성 후 Azure storage account 업로드 후,
  - Azure AI Search 내 indexes로 import 하였으나, 업로드는 완료하였으나 데이터 호출이 되지 않음.
    - Data import 하는과정에서 field 설정이 알맞게 되지 않는것으로 보임
    - 직접 업로드 방법이 아니라, reset_search_index.py 코드를 통해 랜덤데이터 삽입


## 만들며 어려웠던 점
### - 설문 관리자 포탈, 설문 팝업 등 모두 시연 가능하게 만들고자 하였으나 쉽지않았음.
### - 그것에 시간을 너무 뺐기다보니, AI적인 기술을 사용하는 주 목적을 잊고 만드는 것 같아 아쉬웠음.
### - AI Search와 같은 search에 특화된 편리한 서비스가 존재하긴 하나, 단순히 data 저장, sort, filter 정도로만 사용해서 아쉬웠음. (고도화?)

## 시연 페이지
https://pro-hankil-webapp-1-gsbfbscrgfdtfcaa.swedencentral-01.azurewebsites.net/

