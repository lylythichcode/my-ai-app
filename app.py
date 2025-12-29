import streamlit as st
import pandas as pd
from datetime import datetime
import google.generativeai as genai
import os

# --- 1. CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="SmartTAB - Quản lý công việc AI", layout="wide")

# CSS để làm giao diện giống bản React của bạn
st.markdown("""
    <style>
    ...
    </style>
    """, unsafe_allow_html=True) # 
# --- 2. CẤU HÌNH AI (Lấy từ Google AI Studio) ---
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    # Đây là nơi bạn dán System Instruction từ Studio
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction="Bạn là trợ lý ảo SmartTAB. Hãy giúp người dùng tóm tắt công việc hoặc đưa ra lời khuyên năng suất dựa trên danh sách task."
    )

# --- 3. QUẢN LÝ DỮ LIỆU (Thay cho LocalStorage) ---
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

if 'show_app' not in st.session_state:
    st.session_state.show_app = False

# --- 4. GIAO DIỆN LANDING PAGE ---
if not st.session_state.show_app:
    st.title("🚀 SmartTAB")
    st.subheader("Hệ thống quản lý công việc thông minh")
    st.write("Sử dụng AI để tối ưu hóa hiệu suất làm việc của bạn.")
    if st.button("Bắt đầu ngay"):
        st.session_state.show_app = True
        st.rerun()
    st.stop()

# --- 5. GIAO DIỆN APP CHÍNH ---
st.sidebar.title("SmartTAB Menu")
view = st.sidebar.radio("Chế độ xem", ["Danh sách", "Lịch", "Phân tích AI"])

if st.sidebar.button("Thoát App"):
    st.session_state.show_app = False
    st.rerun()

st.title("📝 Danh sách công việc")

# Form thêm Task mới (TaskForm)
with st.expander("➕ Thêm công việc mới", expanded=True):
    with st.form("task_form"):
        title = st.text_input("Tên công việc")
        col1, col2 = st.columns(2)
        with col1:
            priority = st.selectbox("Độ ưu tiên", ["High", "Medium", "Low"])
        with col2:
            due_date = st.date_input("Hạn chót")
        
        submit = st.form_submit_button("Thêm vào danh sách")
        if submit and title:
            new_task = {
                "id": len(st.session_state.tasks) + 1,
                "title": title,
                "priority": priority,
                "due_date": due_date,
                "completed": False
            }
            st.session_state.tasks.append(new_task)
            st.success("Đã thêm!")

# Filter & Search (FilterControls)
search = st.text_input("🔍 Tìm kiếm công việc...")
sort_opt = st.selectbox("Sắp xếp theo", ["Mặc định", "Độ ưu tiên", "Hạn chót"])

# Xử lý Logic Lọc và Sắp xếp
tasks_to_show = st.session_state.tasks
if search:
    tasks_to_show = [t for t in tasks_to_show if search.lower() in t['title'].lower()]

# Hiển thị Task (TaskList)
if view == "Danh sách":
    for idx, task in enumerate(tasks_to_show):
        with st.container():
            col_check, col_text, col_del = st.columns([1, 8, 1])
            is_done = col_check.checkbox("", value=task['completed'], key=f"check_{idx}")
            st.session_state.tasks[idx]['completed'] = is_done
            
            # Gạch ngang chữ nếu đã hoàn thành
            display_title = f"~~{task['title']}~~" if is_done else task['title']
            col_text.markdown(f"**{display_title}** | 📅 {task['due_date']} | 🚩 {task['priority']}")
            
            if col_del.button("🗑️", key=f"del_{idx}"):
                st.session_state.tasks.pop(idx)
                st.rerun()
            st.markdown("---")

elif view == "Lịch":
    if st.session_state.tasks:
        df = pd.DataFrame(st.session_state.tasks)
        st.write("Các công việc sắp tới:")
        st.table(df[['due_date', 'title', 'priority']])
    else:
        st.info("Chưa có công việc nào.")

elif view == "Phân tích AI":
    st.subheader("🤖 Trợ lý AI SmartTAB")
    if st.button("Phân tích danh sách task của tôi"):
        if api_key and st.session_state.tasks:
            content = f"Danh sách task: {str(st.session_state.tasks)}"
            with st.spinner("AI đang đọc danh sách..."):
                response = model.generate_content(f"Hãy tóm tắt và đưa ra lời khuyên cho danh sách này: {content}")
                st.write(response.text)
        else:
            st.warning("Vui lòng cấu hình API Key hoặc thêm Task để AI phân tích.")

st.markdown("<footer>Create by Hailyngvn</footer>", unsafe_allow_state_key=True)
