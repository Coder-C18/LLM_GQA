import os
import dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

dotenv.load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

query_embeddings_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001", task_type="retrieval_query",
                                                      google_api_key=api_key)
doc_embeddings_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001", task_type="retrieval_document",
                                                    google_api_key=api_key)
generate_model = GoogleGenerativeAI(model="gemini-pro",
                                    google_api_key=api_key)


def embeddings_query(query):
    query_vec = query_embeddings_model.embed_query(query)
    return query_vec


def doc_embeddings_query(queries):
    doc_vec = [doc_embeddings_model.embed_query(query) for query in queries]
    return doc_vec


def generate_answer(question, data):
    template = """
    Hướng dẫn thực hiện:
    1. Đọc và tổng hợp thông tin từ ngữ cảnh dưới đây:
        Ngữ cảnh: {data}
    2. Dựa trên thông tin đã tổng hợp, trả lời câu hỏi của người dùng một cách chi tiết, đầy đủ và chính xác. 
        Lưu ý:
        - Chỉ cung cấp câu trả lời trực tiếp, không cần giải thích thêm.
         - trả lời phải rõ ràng, mạch lạc và dễ hiểu.
        Câu hỏi của người dùng: {question}
    """
    prompt = PromptTemplate.from_template(template)
    chain = prompt | generate_model
    print(chain.invoke({"question": question, "data": data}))


question = "Tại sao tác giả lại thích đi bộ quanh công viên vào buổi sáng?"
data = "Mỗi buổi sáng, tôi thường dậy sớm để đi bộ quanh công viên gần nhà. Không khí trong lành và sự yên tĩnh của buổi sáng giúp tôi cảm thấy thư giãn và tỉnh táo hơn. Những giây phút này không chỉ giúp tôi khởi đầu một ngày mới đầy năng lượng mà còn giúp tôi suy nghĩ về những kế hoạch trong ngày. Thỉnh thoảng, tôi gặp những người bạn cũ hoặc những người mới trong công viên, và chúng tôi cùng trò chuyện một lát trước khi tiếp tục công việc của mình."

generate_answer(question, data)
