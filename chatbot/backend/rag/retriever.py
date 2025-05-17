import re
from typing import List
# from langchain_community.vectorstores import Chroma
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain.schema import Document
# from backend.config import settings

# #lấy embedding model trên huggingface
# embedding_model = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL_NAME)

# #load ChromaDB
# vectordb = Chroma(
#     persist_directory=settings.CHROMA_DB_DIR,
#     embedding_function=embedding_model
# )
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.schema import Document
from backend.config import settings

embedding_model = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL_NAME)

vectordb = Chroma(
    persist_directory=settings.CHROMA_DB_DIR,
    embedding_function=embedding_model
)

# đổi sang tiếng việt
VIETNAMESE_YEAR_MAP = {
    "một": "1", "hai": "2", "ba": "3", "bốn": "4", "năm": "5",
    "sáu": "6", "bảy": "7", "tám": "8", "chín": "9"
}

def normalize_query(text: str) -> str:
    """
    Chuẩn hóa câu hỏi người dùng để phù hợp với embedding + dữ liệu trong DB.
    """
    text = text.strip()

    # điều kiện thêm dấu hỏi
    if not text.endswith("?"):
        text += "?"

    #chuẩn hóa lại dữ liệu vì có khoảng trắng thừa
    text = re.sub(r"\s+", " ", text)

    # "năm nhất" -> "năm 1", "năm hai" -> "năm 2", "năm ba" -> "năm 3", "năm bốn" -> "năm 4"
    for word, digit in VIETNAMESE_YEAR_MAP.items():
        text = re.sub(rf"năm {word}\b", f"năm {digit}", text, flags=re.IGNORECASE)

    #trường hợp đặc biệt
    text = (
        text.lower()
            .replace("năm nhất", "năm 1")
            .replace("năm hai", "năm 2")
            .replace("năm ba", "năm 3")
            .replace("năm bốn", "năm 4")
            .replace("năm năm", "năm 5")
            .replace("năm sáu", "năm 6")
    )
    return text
# test thì k15 đang oke, chắc test lại lần nữa với k =5
def get_context_from_query(query: str, k: int = 10) -> List[Document]:
    """
    Truy vấn ngữ cảnh phù hợp từ vector database.
    """
    # chuẩn hóa lại query
    query = normalize_query(query)

    # thêm prefix cho BGE để embedding chính xác hơn
    embed_query = f"Represent this sentence for searching relevant documents: {query}"

    # hàm truy vấn
    docs = vectordb.similarity_search(embed_query, k=k)

    return docs
