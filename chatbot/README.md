## cấu trúc
chatbot/
├── backend/                         # Backend FastAPI + RAG + LangChain
│   ├── api.py                       # FastAPI app và các route /chat,...
│   ├── rag/
│   │   ├── retriever.py             # Dùng LangChain + ChromaDB để truy vấn dữ liệu
│   │   ├── gemini_api.py            # Gọi Gemini API (Google Generative AI)
│   │   ├── prompt_template.py       # Prompt template cho RAG (nếu dùng langchain.prompt)
│   │   └── __init__.py
│   ├── config.py                    # Load biến môi trường (.env)
│   ├── data/                        # Dữ liệu JSON gốc
│   │   └── data_update.json         # Dữ liệu tư vấn tuyển sinh
│   └──utils/
│       ├── word_filter.json         # data word filter
│       └── word_filter.py           # lọc từ cấm
├── chroma_db/                       # Vector database (sinh ra tự động từ LangChain/Chroma)
├── scripts/
│   └── vector_db.py                 # Tạo embedding từ JSON và lưu vào ChromaDB
├── frontend/
│   └── app.py                       # Giao diện Streamlit chat trực tiếp với chatbot
├── .env                             # Chứa các API Key, cấu hình
├── requirements.txt                 # Thư viện cần cài (Gemini, LangChain, FastAPI, etc.)
├── README.md                        # Hướng dẫn sử dụng và cấu trúc dự án
└── main.py                          # Điểm khởi chạy FastAPI

## công nghệ sử dụng
LLM: Gemini 2.0 Flash (Google Generative AI)

RAG (Retrieval-Augmented Generation): LangChain + ChromaDB

Frontend: Streamlit 

Backend: FastAPI

Embedding Model: intfloat/e5-small-v2

## Cách chạy dự án
1. Cài đặt thư viện

pip install -r requirements.txt

2. Cấu hình .env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=models/gemini-2.0-flash
DATA_PATH=data/cleaned_new_1.json
CHROMA_DB_DIR=data/chroma_db
EMBEDDING_MODEL_NAME=BAAI/bge-large-en-v1.5
CHUNK_SIZE=500
CHUNK_OVERLAP=50

3. Tạo Vector DB từ dữ liệu (nếu có rồi khỏi chạy này nha)
python scripts/vector_db.py

4. Chạy API server
uvicorn backend.api:app --reload --port 8000
truy cập vào http://127.0.0.1:8000/docs và test trên FastAPI nhanh hơn 

5. Chạy giao diện chatbot
streamlit run frontend/app.py 
test xem giao diện oke kh 