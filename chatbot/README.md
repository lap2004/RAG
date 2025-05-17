chatbot/
├── backend/                         # Backend FastAPI + RAG + LangChain
│   ├── api.py                       # FastAPI app và các route /chat,...
│   ├── rag/                         # Module truy vấn và gọi Gemini
│   │   ├── retriever.py             # Truy vấn văn bản từ ChromaDB bằng LangChain
│   │   ├── gemini_api.py            # Gọi Gemini API để sinh câu trả lời
│   │   ├── prompt_template.py       # Prompt template cho RAG
│   │   └── __init__.py
│   ├── config.py                    # Load cấu hình từ file .env
│   ├── data/                        # Dữ liệu JSON gốc
│   │   └── data_update.json         # Dữ liệu tư vấn tuyển sinh
│   └── utils/                       
│       ├── word_filter.json         # Danh sách từ cấm
│       └── word_filter.py           # Hàm xử lý lọc từ cấm
├── chroma_db/                       # Vector database tạo bởi Chroma (tự động)
├── scripts/
│   └── vector_db.py                 # Script tạo embedding và lưu vào ChromaDB
├── frontend/
│   └── app.py                       # Giao diện người dùng bằng Streamlit
├── .env                             # Thông tin cấu hình và API key
├── requirements.txt                 # Danh sách thư viện cần cài đặt
├── README.md                        # Tài liệu hướng dẫn sử dụng
└── main.py                          # Điểm khởi chạy FastAPI
## công nghệ sử dụng

- LLM: Gemini 2.0 Flash (Google Generative AI)
- RAG (Retrieval-Augmented Generation): LangChain + ChromaDB
- Frontend: Streamlit
- Backend: FastAPI
- Embedding Model: BAAI/bge-large-en-v1.5
  
## Cách chạy dự án
1. Cài đặt thư viện
```python
pip install -r requirements.txt
```
2. Cấu hình .env
3. Thêm API key vào file .env:
  - GEMINI_API_KEY=your_gemini_api_key
  - GEMINI_MODEL=models/gemini-2.0-flash
  - DATA_PATH=data/data_20250515.json
  - CHROMA_DB_DIR=data/chroma_db
  - EMBEDDING_MODEL_NAME=BAAI/bge-large-en-v1.5
  - CHUNK_SIZE=500
  - CHUNK_OVERLAP=50

4. Tạo Vector DB từ dữ liệu (nếu có rồi khỏi chạy này nha)
```python
python scripts/vector_db.py
```

5. Chạy API server
```python
uvicorn backend.api:app --reload --port 8000
```
truy cập vào http://127.0.0.1:8000/docs và test trên FastAPI nhanh hơn 

6. Chạy giao diện chatbot
```python
streamlit run frontend/app.py
```
test xem giao diện oke kh 
