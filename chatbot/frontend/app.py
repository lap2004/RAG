import streamlit as st
import requests

API_URL = "http://localhost:8000/chat"

st.set_page_config(page_title="Chatbot Tuyển sinh Văn Lang", layout="centered")

st.markdown("""
    <style>
        .user-msg { background-color: #DCF8C6; padding: 10px; border-radius: 10px; margin-bottom: 5px; }
        .bot-msg { background-color: #F1F0F0; padding: 10px; border-radius: 10px; margin-bottom: 15px; }
        .chat-box { max-height: 500px; overflow-y: auto; }
        .reset-button { margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("Chatbot Tuyển sinh Văn Lang")

# Khởi tạo lịch sử chat
if "history" not in st.session_state:
    st.session_state.history = []

# Form nhập câu hỏi
with st.form(key="chat_form", clear_on_submit=True):
    query = st.text_input("Bạn muốn hỏi gì?", placeholder="Ví dụ: Chương trình đào tạo Năm 4 ngành Kiến trúc...")
    submitted = st.form_submit_button("Gửi")

# Gửi câu hỏi khi nhấn nút
if submitted and query:
    try:
        response = requests.post(API_URL, json={"query": query})
        if response.status_code == 200:
            result = response.json()
            st.session_state.history.append({
                "user": query,
                "bot": result["response"]
            })
        else:
            st.error("Lỗi khi gọi API. Kiểm tra server FastAPI.")
    except Exception as e:
        st.error(f"Lỗi: {e}")

# Hiển thị lịch sử hội thoại
st.markdown("<div class='chat-box'>", unsafe_allow_html=True)
for item in reversed(st.session_state.history):
    st.markdown(f"<div class='user-msg'><b>Bạn:</b> {item['user']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='bot-msg'><b>Chatbot:</b> {item['bot']}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Nút xóa lịch sử
if st.button("Xóa toàn bộ hội thoại", type="primary"):
    st.session_state.history.clear()
    st.success("Đã xóa toàn bộ lịch sử hội thoại.")
