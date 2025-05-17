import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import sys
import os
import json
from langchain_community.vectorstores import Chroma
# from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from backend.config import settings

# để tìm backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

#xử lý content nếu nó là list
def get_content_text(entry):
    content = entry.get("content", "")
    return "\n".join(content) if isinstance(content, list) else content

# gộp thông tin quan trọng vào page_content
def format_entry(entry):
    metadata = entry.get("metadata", {})
    keywords = entry.get("keywords", [])
    keyword_text = ", ".join(keywords) if keywords else ""

    return (
        f"Tiêu đề: {entry.get('title', '')}\n"
        f"Năm học: {entry.get('section', '')}\n"
        f"Mức hỗ trợ: {entry.get('muc_ho_tro', '')}\n"
        f"Nội dung: {get_content_text(entry)}\n"
        f"Mã ngành: {metadata.get('ma_nganh', '')}\n"
        f"Văn bằng: {metadata.get('van_bang', '')}\n"
        f"Tên ngành: {metadata.get('nganh', '')}\n"
        f"Chương trình liên kết: {metadata.get('program', '')}\n"
        f"Trường liên kết: {metadata.get('truong', '')}\n"
        f"Thuộc khối ngành: {metadata.get('nguon_file', '')}\n"
        f"Trưởng khoa: {entry.get('truong_khoa', '')}\n"
        f"Số điện thoại: {entry.get('so_dien_thoai', '')}\n"
        f"Địa chỉ: {entry.get('dia_chi', '')}\n"
        f"Email: {entry.get('email', '')}\n"
        f"Website: {entry.get('website', '')}\n"
        f"Danh sách khoa: {entry.get('danh_sach_khoa', '')}\n"
        f"Hướng dẫn: {entry.get('huong_dan', '')}\n"
        f"Thời gian nhập học: {entry.get('thoi_gian_nhap_hoc', '')}\n"
        f"Thời gian đăng kí: {entry.get('thoi_gian_dang_ky', '')}\n"
        f"Đối tượng: {entry.get('doi_tuong', '')}\n"
        f"Trường đại học: {entry.get('truong_dai_hoc', '')}\n"
        f"Chính sách: {entry.get('chinh_sach', '')}\n"
        f"Số doanh nghiệp hợp tác: {metadata.get('so_doanh_nghiep_hop_tac', '')}\n"
        f"Tỉ lệ tìm kiếm việc làm: {metadata.get('ty_le_tim_kiem_viec_lam', '')}\n"
        f"Số trường liên kết: {metadata.get('so_truong_lien_ket', '')}\n"
        f"Quốc gia liên kết: {metadata.get('quoc_gia_lien_ket', '')}\n"
        f"Số giảng viên: {metadata.get('so_giang_vien', '')}\n"
        f"Tỉ lệ giảng viên tiến sĩ: {metadata.get('ti_le_giang_vien_tien_si', '')}\n"
        f"Số học bổng: {metadata.get('so_hoc_bong', '')}\n"
        f"Giá trị học bổng: {metadata.get('gia_tri_hoc_bong', '')}\n"
        f"Số câu lạc bộ: {metadata.get('so_clb', '')}\n"
        f"Phòng học: {metadata.get('phong_hoc', '')}\n"
        f"Phòng thí nghiệm: {metadata.get('phong_thi_nghiem', '')}\n"
        f"Thư viện: {metadata.get('thu_vien', '')}\n"
        f"Số ngành đào tạo: {metadata.get('so_nganh_dao_tao', '')}\n"
        f"Trình độ: {metadata.get('trinh_do', '')}\n"
        f"Danh sách cơ sở: {metadata.get('danh_sach_co_so', '')}\n"
        f"Tên khoa: {metadata.get('ten_khoa', '')}\n"
        f"Tên viện: {metadata.get('ten_vien', '')}\n"
        f"Năm thành lập: {metadata.get('nam_thanh_lap', '')}\n"
        f"Loại hình: {metadata.get('loai_hinh', '')}\n"
        f"Mã trường: {entry.get('ma_truong', '')}\n"
        f"Loại học bổng: {metadata.get('loai', '')}\n"
        f"Từ khóa: {keyword_text}"
    )
# load json
with open(settings.DATA_PATH, "r", encoding="utf-8") as f:
    raw_data = json.load(f)

def safe_metadata(metadata):
    cleaned = {}
    for key, value in metadata.items():
        if isinstance(value, list):
            cleaned[key] = ", ".join(map(str, value))  # chuyển list thành chuỗi
        elif isinstance(value, (str, int, float, bool)):
            cleaned[key] = value
        else:
            cleaned[key] = str(value)  # fallback nếu là object
    return cleaned

docs = []
for item in raw_data:
    full_content = format_entry(item)
    metadata = safe_metadata(item.get("metadata", {}))  # dùng hàm mới
    docs.append(Document(page_content=full_content, metadata=metadata))
print(f"Tổng số tài liệu gốc: {len(docs)}")

# tạo document
# docs = []
# for item in raw_data:
#     full_content = format_entry(item)
#     metadata = item.get("metadata", {})
#     docs.append(Document(page_content=full_content, metadata=metadata))
# print(f"Tổng số tài liệu gốc: {len(docs)}")

# tách thành chunk
splitter = RecursiveCharacterTextSplitter(
    chunk_size=settings.CHUNK_SIZE,
    chunk_overlap=settings.CHUNK_OVERLAP
)
split_docs = splitter.split_documents(docs)
print(f"Số chunk sau khi split: {len(split_docs)}")

# Khởi tạo mô hình embedding
# embedding_model = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL_NAME)
embedding_model = HuggingFaceEmbeddings(
    model_name=settings.EMBEDDING_MODEL_NAME,
    model_kwargs={"device": "cpu"}
)

# tạo ChromaDB và ghi dữ liệu
vectordb = Chroma.from_documents(
    documents=split_docs,
    embedding=embedding_model,
    persist_directory=settings.CHROMA_DB_DIR
)
vectordb.persist()
print(f"Vector DB đã tạo xong tại: {settings.CHROMA_DB_DIR}")
print(f"Mô hình embedding: {settings.EMBEDDING_MODEL_NAME}")
