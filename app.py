import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="App AI của tôi")
st.title("🤖 Trợ lý AI cá nhân")

# Lấy API Key từ hệ thống (Secrets)
api_key = os.environ.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    user_input = st.text_input("Hỏi tôi bất cứ điều gì:")
    if st.button("Gửi"):
        if user_input:
            response = model.generate_content(user_input)
            st.write(response.text)
else:
    st.error("Chưa cấu hình API Key!")