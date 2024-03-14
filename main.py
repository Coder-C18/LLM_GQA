import time

from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
import google.generativeai as gemini_client
from qdrant_client.http.models import Distance, PointStruct, VectorParams

GEMINI_API_KEY = "AIzaSyCieu0Mua9b0gjo-RbIGi-bTJGYlwzVN1U"  # add your key here
client = QdrantClient("localhost", port=6333)
gemini_client.configure(api_key=GEMINI_API_KEY)

loader = Docx2txtLoader('D:\code\LLM_GQA\GEM_notebook (1).docx')
pages = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=2048, chunk_overlap=512)

docs = text_splitter.split_documents(pages)

document_chunks = [chunk.page_content for chunk in docs]

results = []
t = 1

for sentence in document_chunks:

    emb = gemini_client.embed_content(
        model="models/embedding-001",
        content=sentence,
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
client.create_collection('docx', vectors_config=
VectorParams(
    size=768,
    distance=Distance.COSINE,
)
                         )
client.upsert('docx', points)
