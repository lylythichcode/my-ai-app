import streamlit as st
import pandas as pd
from datetime import datetime
import google.generativeai as genai
import os

# --- CẤU HÌNH GIAO DIỆN CHUẨN SMARTTAB ---
st.set_page_config(page_title="SmartTAB", page_icon="📝", layout="centered")

# CSS để "nhái" lại giao diện xanh trắng của Google AI Studio
st.markdown("""
    <style>
    .stApp { background-color: #f0f7ff; }
    .main-title { color: #56ccf2; text-align: center; font-size: 3rem; font-weight: bold; margin-bottom: 0; }
    .slogan { text-align: center; color: #666; margin-bottom: 30px; }
    .stButton>button { 
        background-color: #56ccf2; color: white; border-radius: 10px; 
        border: none; height: 3em; width: 100%; font-weight: bold;
    }
    .task-card {
        background-color: white; padding: 20px; border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); border-left: 5px solid #56ccf2;
        margin-bottom: 10px;
    }
    footer { text-align: center; color: #999; margin-top: 50px; }
    </style>
    """, unsafe_allow_html=True)

# --- KHỞI TẠO DỮ LIỆU ---
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# --- GIAO DIỆN CHÍNH ---
st.markdown("<h1 class='main-title'>SmartTAB</h1>", unsafe_allow_html=True)
st.markdown("<p class='slogan'>Sắp xếp công việc, đơn giản hóa cuộc sống.</p>", unsafe_allow_html=True)

# Tabs như trong bản thiết kế
tab_list, tab_calendar = st.tabs(["📑 Danh sách công việc", "📅 Lịch & Trợ lý AI"])

with tab_list:
    # Form thêm Task
    with st.container():
        st.subheader("➕ Thêm công việc mới")
        t_name = st.text_input("Tên công việc", placeholder="Ví dụ: Hoàn thành dự án...")
        c1, c2 = st.columns(2)
        t_priority = c1.selectbox("Mức độ ưu tiên", ["Cao", "Trung bình", "Thấp"])
        t_date = c2.date_input("Ngày hết hạn")
        
        if st.button("Thêm công việc") and t_name:
            st.session_state.tasks.append({
                "title": t_name, "priority": t_priority, 
                "date": t_date, "done": False
            })
            st.rerun()

    st.markdown("---")
    
    # Hiển thị danh sách
    if not st.session_state.tasks:
        st.info("Chưa có công việc nào. Hãy thêm việc để bắt đầu!")
    else:
        for i, task in enumerate(st.session_state.tasks):
            with st.container():
                col_check, col_info, col_del = st.columns([1, 8, 1])
                is_done = col_check.checkbox("", value=task['done'], key=f"check_{i}")
                st.session_state.tasks[i]['done'] = is_done
                
                display_text = f"~~{task['title']}~~" if is_done else f"**{task['title']}**"
                col_info.markdown(f"{display_text} <br> <small>🚩 {task['priority']} | 📅 {task['date']}</small>", unsafe_allow_html=True)
                
                if col_del.button("🗑️", key=f"del_{i}"):
                    st.session_state.tasks.pop(i)
                    st.rerun()

with tab_calendar:
    if st.session_state.tasks:
        st.subheader("📅 Lịch trình công việc")
        df = pd.DataFrame(st.session_state.tasks)
        st.dataframe(df[['date', 'title', 'priority']], use_container_width=True)
        
        st.markdown("---")
        st.subheader("🤖 Trợ lý AI Gemini")
        if st.button("Phân tích và đưa ra lời khuyên"):
            api_key = os.environ.get("GEMINI_API_KEY")
            if api_key:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-1.5-flash")
                prompt = f"Tôi có các công việc sau: {str(st.session_state.tasks)}. Hãy cho tôi lời khuyên ngắn gọn để hoàn thành chúng hiệu quả nhất."
                with st.spinner("AI đang suy nghĩ..."):
                    response = model.generate_content(prompt)
                    st.success(response.text)
            else:
                st.error("Lỗi: Bạn chưa cài đặt API Key trong phần Secrets!")
    else:
        st.info("Thêm công việc để sử dụng tính năng này.")

st.markdown("<footer>Create by Hailyngvn</footer>", unsafe_allow_html=True)
