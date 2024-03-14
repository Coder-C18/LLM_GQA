import google.generativeai as gemini_client
from qdrant_client import QdrantClient


collection_name = "example_collection"
client = QdrantClient("localhost", port=6333)
GEMINI_API_KEY = "AIzaSyCieu0Mua9b0gjo-RbIGi-bTJGYlwzVN1U"  # add your key here
gemini_client.configure(api_key=GEMINI_API_KEY)
def QA_Gemini(question):
    print(question)
    t = client.search(
        collection_name='docx',
        query_vector=gemini_client.embed_content(
            model="models/embedding-001",
            content=question,
            task_type="retrieval_query",
        )["embedding"],
        limit=10

    )


    matching_engine_response = [i.payload['text'] for i in t]
    matching_engine_response = '\n'.join(matching_engine_response)
    prompt=f"""
    Thực hiện đúng 2 bước sau:
    1. Đọc ngữ cảnh bên dưới và tổng hợp dữ liệu này
    Ngữ cảnh: {matching_engine_response}
    2. Dựa vào dữ liệu tổng hợp được , hãy trả lời câu hỏi dưới đây một cách chi tiết và đẩy đủ 
    câu hỏi của người dùng: {question}
    """

    output = gemini_client.GenerativeModel('gemini-pro').generate_content(prompt).text
    return output