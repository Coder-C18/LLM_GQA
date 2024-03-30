from langchain_community.document_loaders.word_document import Docx2txtLoader
from qdrant_client import QdrantClient
from langchain.text_splitter import RecursiveCharacterTextSplitter
from LLM import gemini_client
from qdrant_client.http.models import Distance, PointStruct, VectorParams
import time
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='../.env')
client = QdrantClient(os.getenv('LOCATION_DB'), port=os.getenv('PORT_DB'))


def QA_Gemini(question, collection_name):
    print(question)
    t = client.search(
        collection_name=collection_name,
        query_vector=gemini_client.embed_content(
            model="models/embedding-001",
            content=question,
            task_type="retrieval_query",
        )["embedding"],
        limit=10

    )
    matching_engine_response = [i.payload['text'] for i in t]
    matching_engine_response = '\n'.join(matching_engine_response)
    prompt = f"""
    Thực hiện đúng 2 bước sau:
    1. Đọc ngữ cảnh bên dưới và tổng hợp dữ liệu này
    Ngữ cảnh: {matching_engine_response}
    2. Dựa vào dữ liệu tổng hợp được , hãy trả lời câu hỏi dưới đây một cách chi tiết và đẩy đủ 
    câu hỏi của người dùng: {question}
    """

    output = gemini_client.GenerativeModel('gemini-pro').generate_content(prompt).text
    return output


def get_list_collection_name():
    collections = client.get_collections()
    return [i.name for i in collections.collections]


def insert_db(file_path, collection_name):
    loader = Docx2txtLoader(file_path)
    pages = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2048, chunk_overlap=512)

    docs = text_splitter.split_documents(pages)

    document_chunks = [chunk.page_content for chunk in docs]

    results = []
    t = 1
    for index in range(len(document_chunks)):
        emb = gemini_client.embed_content(
            model="models/embedding-001",
            content=document_chunks[index],
            task_type="retrieval_document",
            title="Qdrant x Gemini",
        )['embedding']
        results.append(emb)
        if t % 60 == 0:
            time.sleep(60)
        t += 1

    points = [
        PointStruct(
            id=idx,
            vector=response,
            payload={"text": text},
        )
        for idx, (response, text) in enumerate(zip(results, document_chunks))
    ]
    client.create_collection(collection_name,
                             vectors_config=VectorParams(
                                 size=768,
                                 distance=Distance.COSINE,)
                             )
    client.upsert(collection_name, points)
