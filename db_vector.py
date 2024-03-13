import google.generativeai as gemini_client
from qdrant_client import QdrantClient


collection_name = "example_collection"
client = QdrantClient("localhost", port=6333)
GEMINI_API_KEY = "AIzaSyCieu0Mua9b0gjo-RbIGi-bTJGYlwzVN1U"  # add your key here
gemini_client.configure(api_key=GEMINI_API_KEY)


question = '  mô tả  Bộ phận Technical Promotion Office (TPO) của gem'
# question = 'gem chú trọng nâng cao cái gì? '

t = client.search(
    collection_name='docx',
    query_vector=gemini_client.embed_content(
        model="models/embedding-001",
        content=question,
        task_type="retrieval_query",
    )["embedding"],
    limit=5

)

matching_engine_response = [i.payload['text'] for i in t]
matching_engine_response = '\n'.join(matching_engine_response)
prompt=f"""
Thực hiện đúng 3 bước sau:
1. Đọc ngữ cảnh bên dưới và tổng hợp dữ liệu này
Ngữ cảnh: {matching_engine_response}
2. Trả lời câu hỏi chỉ sử dụng ngữ cảnh này câu hỏi của người dùng: {question}
"""

output = gemini_client.GenerativeModel('gemini-pro').generate_content(prompt).text

print(output)