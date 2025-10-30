from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchFieldDataType,
)
from azure.core.credentials import AzureKeyCredential
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the clients
endpoint = os.getenv("SEARCH_ENDPOINT")
key = os.getenv("SEARCH_API_KEY")
index_name = os.getenv("INDEX_NAME")

# Create an index client
index_client = SearchIndexClient(endpoint=endpoint, credential=AzureKeyCredential(key))

# Define the index
index = SearchIndex(
    name=index_name,
    fields=[
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SimpleField(name="timestamp", type=SearchFieldDataType.String, sortable=True, filterable=True),
        SimpleField(name="rating", type=SearchFieldDataType.Int32, sortable=True, filterable=True),
        SimpleField(name="gender", type=SearchFieldDataType.String, searchable=True, filterable=True),
        SimpleField(name="age_group", type=SearchFieldDataType.Int32, sortable=True, filterable=True),
        SimpleField(name="feedback", type=SearchFieldDataType.String, searchable=True),
    ]
)

# Delete the index if it exists
try:
    index_client.delete_index(index_name)
    print(f"Deleted existing index: {index_name}")
except Exception as e:
    print(f"Index doesn't exist or error deleting: {str(e)}")

# Create the index
try:
    result = index_client.create_index(index)
    print(f"Created new index: {result.name}")
except Exception as e:
    print(f"Error creating index: {str(e)}")

# Initialize the search client
search_client = SearchClient(endpoint=endpoint, index_name=index_name, credential=AzureKeyCredential(key))

# 목업 데이터 생성을 위한 설정
import random
from datetime import datetime, timedelta

# 피드백 템플릿
positive_feedbacks = [
    "서비스가 정말 훌륭했어요. {}",
    "매우 만족스러운 경험이었습니다. {}",
    "직원분들이 친절하고 전문적이었어요. {}",
    "기대 이상으로 좋았습니다. {}",
    "확실히 추천할 만한 서비스예요. {}"
]

neutral_feedbacks = [
    "보통이었어요. {}",
    "나쁘지 않았습니다. {}",
    "괜찮았어요. {}",
    "기대했던 정도였습니다. {}",
    "평범한 서비스였어요. {}"
]

negative_feedbacks = [
    "아쉬운 점이 많았어요. {}",
    "기대에 미치지 못했습니다. {}",
    "개선이 필요해 보입니다. {}",
    "실망스러웠어요. {}",
    "서비스 품질이 떨어져요. {}"
]

detail_comments = [
    "다음에 또 이용하고 싶어요.",
    "조금 더 신경 써주시면 좋겠어요.",
    "가격 대비 괜찮았습니다.",
    "시설이 깨끗했어요.",
    "대기 시간이 길었어요.",
    "직원 교육이 필요해보여요.",
    "편리한 위치에 있어서 좋았어요.",
    "주차가 불편했어요.",
    "시설이 낡았어요.",
    "분위기가 좋았어요."
]

# 목업 데이터 생성 함수
def generate_mock_data(date, count):
    docs = []
    for i in range(count):
        # 기본 데이터 설정
        rating = random.randint(1, 5)
        gender = random.choice(["남성", "여성", "기타"])
        age_group = random.choice([20, 30, 40, 50, 60, 70])
        
        # 평점에 따른 피드백 선택
        if rating >= 4:
            feedback_template = random.choice(positive_feedbacks)
        elif rating == 3:
            feedback_template = random.choice(neutral_feedbacks)
        else:
            feedback_template = random.choice(negative_feedbacks)
        
        # 상세 코멘트 추가
        detail = random.choice(detail_comments)
        feedback = feedback_template.format(detail)
        
        # 시간 설정 (9AM ~ 10PM 사이)
        hour = random.randint(9, 22)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        timestamp = f"{date}T{hour:02d}:{minute:02d}:{second:02d}Z"
        
        doc = {
            "id": f"{date}-{i+1}",
            "rating": rating,
            "gender": gender,
            "age_group": age_group,
            "feedback": feedback,
            "timestamp": timestamp
        }
        docs.append(doc)
    return docs

# 날짜별 300개씩 데이터 생성
test_docs = []
dates = ["2025-10-28", "2025-10-29", "2025-10-30"]
for date in dates:
    test_docs.extend(generate_mock_data(date, 300))

# Upload the documents
try:
    result = search_client.upload_documents(documents=test_docs)
    print("\nUpload results:")
    for r in result:
        print(f"Document ID: {r.key}, Succeeded: {r.succeeded}")
except Exception as e:
    print(f"\nError uploading documents: {str(e)}")

# Wait for indexing to complete
import time
print("\nWaiting for indexing to complete...")
time.sleep(5)  # 5초 대기

# Test search with different options
try:
    # 검색 옵션 설정
    results = list(search_client.search(
        search_text="*",
        include_total_count=True,
        select="id,timestamp,rating,gender,age_group,feedback",
        order_by="timestamp desc"
    ))
    
    print(f"\nFound {len(results)} documents")
    
    if len(results) == 0:
        # 인덱스 통계 확인
        stats = index_client.get_index_statistics(index_name)
        print(f"\nIndex statistics:")
        print(f"Document count: {stats.document_count}")
        print(f"Storage size: {stats.storage_size} bytes")
        
        # 모든 문서 나열 시도
        print("\nTrying to list all documents...")
        all_docs = list(search_client.search(
            search_text="",
            include_total_count=True,
            select="id"
        ))
        print(f"Total documents found: {len(all_docs)}")
    
    for doc in results:
        print("\nDocument contents:")
        for key, value in doc.items():
            if not key.startswith("@"):
                print(f"{key}: {value}")

except Exception as e:
    print(f"\nError searching documents: {str(e)}")
    print(f"Error type: {type(e)}")
    import traceback
    print(f"Full error details:\n{traceback.format_exc()}")