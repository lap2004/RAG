def build_prompt_with_context(query: str, context_docs: list) -> str:
    context_text = "\n\n".join(doc.page_content.strip() for doc in context_docs)

    return f"""
Bạn là trợ lý AI tư vấn tuyển sinh của Trường Đại học Văn Lang.

--- DỮ LIỆU THAM KHẢO ---
{context_text}

--- CÂU HỎI ---
{query}

--- YÊU CẦU ---
Hãy trình bày câu trả lời rõ ràng, có xuống dòng nếu là danh sách.
Nếu có danh sách con (như môn tự chọn), hãy dùng dấu cộng (+) hoặc thụt vào đầu dòng.
""".strip()
