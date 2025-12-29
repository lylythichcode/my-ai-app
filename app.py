import streamlit as st
import pandas as pd
from datetime import datetime, date
import google.generativeai as genai
import os

# --- 1. CẤU HÌNH TRANG & GIAO DIỆN (CSS) ---
st.set_page_config(page_title="SmartTAB - Quản lý công việc", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #f8fbff; }
    .main-card { background-color: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); margin-bottom: 20px; }
    .footer { text-align: center; color: #888; font-size: 0.8em; margin-top: 50px; }
    .priority-high { border-left: 5px solid #ff4b4b; padding-left: 10px; }
    .priority-medium { border-left: 5px solid #ffa500; padding-left: 10px; }
    .priority-low { border-left: 5px solid #28a745; padding-left: 10px; }
    .task-done { text-decoration: line-through; color: #adb5bd; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. QUẢN LÝ TRẠNG THÁI (SESSION STATE) ---
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'show_app' not in st.session_state:
    st.session_state.show_app = False
if 'onboarding_complete' not in st.session_state:
    st.session_state.onboarding_complete = False

# --- 3. LOGIC XỬ LÝ (DỊCH TỪ REACT) ---
def add_task(title, priority, due_date):
    new_task = {
        "id": str(datetime.now().timestamp()),
        "title": title,
        "priority": priority,
        "due_date": due_date,
        "completed": False
    }
    st.session_state.tasks.append(new_task)

# --- 4. GIAO DIỆN LANDING PAGE ---
if not st.session_state.show_app:
    st.markdown("<h1 style='text-align: center; color: #1e90ff;'>🚀 SmartTAB</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Chào mừng bạn đến với hệ thống quản lý công việc thông minh.</p>", unsafe_allow_html=True)
    if st.button("Bắt đầu ngay", use_container_width=True):
        st.session_state.show_app = True
        st.rerun()
    st.stop()

# --- 5. GIAO DIỆN ONBOARDING (HƯỚNG DẪN) ---
if not st.session_state.onboarding_complete:
    st.info("💡 **Hướng dẫn nhanh:** Bạn có thể thêm công việc, chọn độ ưu tiên và để AI tư vấn cách hoàn thành hiệu quả nhất!")
    if st.button("Tôi đã hiểu"):
        st.session_state.onboarding_complete = True
        st.rerun()
    st.stop()

# --- 6. ỨNG DỤNG CHÍNH ---
st.markdown("<h1 style='text-align: center; color: #1e90ff;'>SmartTAB</h1>", unsafe_allow_html=True)

# Switch View (Chuyển đổi Lịch/Danh sách)
view = st.radio("Chế độ xem", ["📋 Danh sách", "📅 Lịch & AI"], horizontal=True)

if view == "📋 Danh sách":
    # Form thêm Task
    with st.markdown("<div class='main-card'>", unsafe_allow_html=True):
        with st.form("task_form", clear_on_submit=True):
            t_title = st.text_input("Tên công việc", placeholder="Nhập việc cần làm...")
            col1, col2 = st.columns(2)
            t_priority = col1.selectbox("Ưu tiên", ["High", "Medium", "Low"])
            t_date = col2.date_input("Hạn chót", value=date.today())
            if st.form_submit_button("+ Thêm công việc") and t_title:
                add_task(t_title, t_priority, t_date)
                st.toast("Đã thêm công việc!")
    st.markdown("</div>", unsafe_allow_html=True)

    # Bộ lọc & Tìm kiếm
    search = st.text_input("🔍 Tìm kiếm công việc...")
    
    # Hiển thị danh sách
    st.write("### Công việc của bạn")
    for i, task in enumerate(st.session_state.tasks):
        if search.lower() in task['title'].lower():
            p_class = f"priority-{task['priority'].lower()}"
            with st.container():
                c1, c2, c3 = st.columns([1, 8, 1])
                is_done = c1.checkbox("", value=task['completed'], key=f"check_{task['id']}")
                st.session_state.tasks[i]['completed'] = is_done
                
                title_html = f"<span class='task-done'>{task['title']}</span>" if is_done else task['title']
                c2.markdown(f"<div class='{p_class}'>{title_html} <br><small>📅 {task['due_date']}</small></div>", unsafe_allow_html=True)
                
                if c3.button("🗑️", key=f"del_{task['id']}"):
                    st.session_state.tasks.pop(i)
                    st.rerun()

else:
    # Chế độ Lịch & AI
    if st.session_state.tasks:
        df = pd.DataFrame(st.session_state.tasks)
        st.write("### 📅 Lịch trình sắp tới")
        st.dataframe(df[['due_date', 'title', 'priority']], use_container_width=True)
        
        st.write("### 🤖 Trợ lý AI Tư vấn")
        if st.button("Phân tích danh sách với Gemini"):
            api_key = os.environ.get("GEMINI_API_KEY")
            if api_key:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-1.5-flash")
                prompt = f"Dựa trên danh sách task sau: {str(st.session_state.tasks)}. Hãy đưa ra lời khuyên để tối ưu năng suất."
                response = model.generate_content(prompt)
                st.info(response.text)
            else:
                st.error("Lỗi: Chưa có API Key!")
    else:
        st.info("Hãy thêm công việc để xem lịch và nhận tư vấn AI.")

# Footer
st.markdown("<div class='footer'>Create by Hailyngvn</div>", unsafe_allow_html=True)