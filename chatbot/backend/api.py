from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from backend.rag.retriever import get_context_from_query
from backend.rag.prompt_template import build_prompt_with_context
from backend.rag.gemini_api import call_gemini_with_context
from backend.utils.word_filter import contains_bad_word

#tạo ứng dụng FastAPI
app = FastAPI()

#frontend gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],             # Cho phép tất cả domain
    allow_credentials=True,
    allow_methods=["*"],             # Cho tất cả phương thức: GET, POST,...
    allow_headers=["*"],             # Cho phép tất cả header
)
# định nghĩa schema cho request
class ChatRequest(BaseModel):
    query: str
#kiểm tra xem trang thái API
@app.get("/")
def root():
    return {"status": "online", "message": "Gemini RAG API is running"}

# endpoint chính xử lý truy vấn 
@app.post("/chat")
def chat_endpoint(body: ChatRequest):
    query = body.query.strip()
    # work filter (lấy trên github thầy gửi)
    if contains_bad_word(query):
        return {
            "response": "Câu hỏi của bạn có chứa nội dung không phù hợp. Vui lòng hỏi lại một cách lịch sự.",
            "documents": []
        }
    # truy xuất context từ tector_db
    docs = get_context_from_query(query)
    # thông báo tìm kh thấy
    if not docs:
        return {
            "response": "Không có dữ liệu phù hợp cho câu hỏi này.",
            "documents": []
        }
    # tạo prompt chat message
    messages = build_prompt_with_context(query, docs)
    #  gửi gemini lấy result
    response = call_gemini_with_context(messages)
    # trả kết quả
    return {
        "response": response,
        "documents": [doc.page_content for doc in docs]
    }
