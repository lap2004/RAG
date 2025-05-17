import google.generativeai as genai
from backend.config import settings

# api gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

def call_gemini_with_context(prompt: str) -> str:
    """
    Gọi Gemini API với prompt dạng văn bản thuần (string).
    
    Args:
        prompt (str): Prompt đã ghép từ context + câu hỏi
    
    Returns:
        str: Phản hồi từ Gemini
    """
    try:
        model = genai.GenerativeModel(model_name=settings.GEMINI_MODEL)

        #prompt
        response = model.generate_content(prompt)

        #phản hồi
        return response.text.strip()

    except Exception as e:
        # ghi lại log
        return f"Lỗi khi gọi Gemini API: {str(e)}"

