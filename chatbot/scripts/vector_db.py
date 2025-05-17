import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from backend.config import settings

# Hàm xử lý content nếu là list
def get_content_text(entry):
    content = entry.get("content", "")
    return "\n".join(content) if isinstance(content, list) else content

# Hàm định dạng nội dung để embedding
def format_entry(entry):
    metadata = entry.get("metadata", {})
    keywords = entry.get("keywords", [])
    keyword_text = ", ".join(keywords) if keywords else ""

    return (
        f"Nội dung: {get_content_text(entry)}\n"
        f"Tiêu đề: {entry.get('title', '')}\n"
        f"Phân loại nội dung: {entry.get('section', '')}\n"
        f"Mã trường: {metadata.get('ma_truong', '')}\n"
        f"Trưởng khoa: {metadata.get('truong_khoa', '')}\n"
        f"Số điện thoại: {metadata.get('so_dien_thoai', '')}\n"
        f"Địa chỉ: {metadata.get('dia_chi', '')}\n"
        f"Email: {metadata.get('diemaila_chi', '')}\n"
        f"Website: {entry.get('website', '')}\n"
        f"Hướng dẫn thực hiện: {entry.get('huong_dan', '')}\n"
        f"Thời gian nhập học: {metadata.get('thoi_gian_nhap_hoc', '')}\n"
        f"Thời gian đăng ký: {metadata.get('thoi_gian_dang_ky', '')}\n"
        f"Đối tượng: {entry.get('doi_tuong', '')}\n"
        f"Trường đại học: {metadata.get('truong_dai_hoc', '')}\n"
        f"Chính sách của trường Đại học Văn Lang: {entry.get('chinh_sach', '')}\n"
        f"Danh sách câu lạc bộ: {entry.get('clb', '')}\n"
        f"Mã ngành: {metadata.get('ma_nganh', '')}\n"
        f"Văn bằng: {metadata.get('van_bang', '')}\n"
        f"Tên ngành: {metadata.get('nganh', '')}\n"
        f"Chương trình: {metadata.get('program', '')}\n"
        f"Trường liên kết: {metadata.get('truong', '')}\n"
        f"Danh sách khoa: {metadata.get('danh_sach_khoa', '')}\n"
        f"Thông tin về  Khoa/Viện: {metadata.get('thong_tin', '')}\n"
        f"Số doanh nghiệp hợp tác: {metadata.get('so_doanh_nghiep_hop_tac', '')}\n"
        f"Số trường liên kết: {metadata.get('so_truong_lien_ket', '')}\n"
        f"Quốc gia liên kết: {metadata.get('quoc_gia_lien_ket', '')}\n"
        f"Số giảng viên: {metadata.get('so_giang_vien', '')}\n"
        f"Số lượng giảng viên tiến sĩ: {metadata.get('so_luong_giang_vien_tien_si', '')}\n"
        f"Số câu lạc bộ: {metadata.get('so_clb', '')}\n"
        f"Phòng học đại học văn lang: {metadata.get('phong_hoc', '')}\n"
        f"Phòng thí nghiệm: {metadata.get('phong_thi_nghiem', '')}\n"
        f"Thư viện đại học văn lang: {metadata.get('thu_vien', '')}\n"
        f"Giờ mở cửa thư viện: {metadata.get('gio_mo_cua', '')}\n"
        f"Số ngành đào tạo: {metadata.get('so_nganh_dao_tao', '')}\n"
        f"Trình độ: {metadata.get('trinh_do', '')}\n"
        f"Tên khoa: {metadata.get('ten_khoa', '')}\n"
        f"Thuộc về Khoa: {metadata.get('thuoc_khoa', '')}\n"
        f"Thuộc về Viện: {metadata.get('thuoc_vien', '')}\n"
        f"Tên viện: {metadata.get('ten_vien', '')}\n"
        f"Năm thành lập trường: {metadata.get('nam_thanh_lap', '')}\n"
        f"Loại hình: {metadata.get('loai_hinh', '')}\n"
        f"Loại học bổng: {metadata.get('loai', '')}\n"
        f"Khung giờ học/Ca học: {metadata.get('ca', '')}\n"
        f"Giờ học/Ca học: {metadata.get('thoi_gian', '')}\n"
        f"Mục đích: {metadata.get('muc_dich', '')}\n"
        f"Hình thức: {metadata.get('hinh_thuc', '')}\n"
        f"Mức hỗ trợ: {metadata.get('muc_ho_tro', '')}\n"
        f"Từ khóa: {keyword_text}"
    )

# Load dữ liệu
with open(settings.DATA_PATH, "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# Đảm bảo metadata hợp lệ (không chứa list)
def safe_metadata(metadata):
    cleaned = {}
    for key, value in metadata.items():
        if isinstance(value, list):
            cleaned[key] = ", ".join(map(str, value))
        elif isinstance(value, (str, int, float, bool)):
            cleaned[key] = value
        else:
            cleaned[key] = str(value)
    return cleaned

# Tạo tài liệu
docs = []
for item in raw_data:
    full_content = format_entry(item)
    metadata = safe_metadata(item.get("metadata", {}))
    docs.append(Document(page_content=full_content, metadata=metadata))
print(f"Tổng số tài liệu gốc: {len(docs)}")

# Tách chunk
splitter = RecursiveCharacterTextSplitter(
    chunk_size=settings.CHUNK_SIZE,
    chunk_overlap=settings.CHUNK_OVERLAP
)
split_docs = splitter.split_documents(docs)
print(f"Số chunk sau khi split: {len(split_docs)}")

# Tạo mô hình embedding
embedding_model = HuggingFaceEmbeddings(
    model_name=settings.EMBEDDING_MODEL_NAME,
    model_kwargs={"device": "cpu"}
)

# Ghi vào vector DB
vectordb = Chroma.from_documents(
    documents=split_docs,
    embedding=embedding_model,
    persist_directory=settings.CHROMA_DB_DIR
)
vectordb.persist()
print(f"Vector DB đã tạo xong tại: {settings.CHROMA_DB_DIR}")
print(f"Mô hình embedding: {settings.EMBEDDING_MODEL_NAME}")
