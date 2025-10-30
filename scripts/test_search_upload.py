from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize the search client
search_client = SearchClient(
    endpoint=os.getenv("SEARCH_ENDPOINT"),
    index_name=os.getenv("INDEX_NAME"),
    credential=AzureKeyCredential(os.getenv("SEARCH_API_KEY"))
)

# Test documents
test_docs = [
    {
        "id": "1",
        "rating": 3,
        "gender": "기타",
        "age_group": 50,
        "feedback": "기대만큼은 아니지만 쓸만했어요.",
        "timestamp": "2025-10-28T14:50:17Z"  # Z를 추가하여 UTC 표준시 명시
    },
    {
        "id": "2",
        "rating": 2,
        "gender": "여성",
        "age_group": 60,
        "feedback": "실망스러운 결과를 받았습니다.",
        "timestamp": "2025-10-28T06:14:07Z"
    },
    {
        "id": "3",
        "rating": 4,
        "gender": "여성",
        "age_group": 80,
        "feedback": "직원분들이 친절했습니다.",
        "timestamp": "2025-10-28T08:38:17Z"
    }
]

# Upload the documents
try:
    result = search_client.upload_documents(documents=test_docs)
    print("Upload results:")
    for r in result:
        print(f"Document ID: {r.key}, Succeeded: {r.succeeded}")
except Exception as e:
    print(f"Error uploading documents: {str(e)}")

# Test search
try:
    results = list(search_client.search(search_text="*"))
    print(f"\nFound {len(results)} documents")
    for doc in results:
        print("\nDocument contents:")
        for key, value in doc.items():
            if not key.startswith("@"):
                print(f"{key}: {value}")
except Exception as e:
    print(f"Error searching documents: {str(e)}")