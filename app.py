import streamlit as st
import requests
import io
import os
import tempfile
import time
import google.generativeai as genai
from PIL import Image

# ۱. تنظیمات API Keys
GEMINI_KEY = "AIzaSyDI2K2xjOXyaXeX8DALmy4Oqx9m0WtTRjc" 
HF_TOKEN = "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"
BG_REMOVE_API = "https://api-inference.huggingface.co/models/briaai/RMBG-1.4"

# پیکربندی Gemini
try:
    genai.configure(api_key=GEMINI_KEY)
    gemini_model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    pass

# ۲. تنظیمات ظاهر برنامه
st.set_page_config(page_title="دستیار هوشمند Gemini", layout="wide", page_icon="🚀")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Vazirmatn', sans-serif; direction: rtl; text-align: right; }
    .stButton>button { border-radius: 12px; height: 3em; background-color: #007BFF; color: white; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# ۳. منوی کناری
with st.sidebar:
    st.title("🤖 پنل ابزار AI")
    choice = st.radio("انتخاب ابزار:", ["💬 چت با Gemini", "🎨 تصویرساز", "🪄 ویرایشگر جادویی", "🎬 ابزارهای ویدیو"])
    st.divider()
    if st.button("🗑️ پاکسازی کل حافظه"):
        st.session_state.clear()
        st.rerun()

# --- بخش ۱: چت هوشمند ---
if choice == "💬 چت با Gemini":
    st.header("💬 دستیار متنی Gemini")
    if "chat_history" not in st.session_state: st.session_state.chat_history = []
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.write(msg["content"])

    if prompt := st.chat_input("سوال شما..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        with st.chat_message("assistant"):
            try:
                response = gemini_model.generate_content(prompt)
                st.write(response.text)
                st.session_state.chat_history.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error("❌ خطا در اتصال! لطفاً فیلترشکن یا DNS خود را بررسی کنید.")

# --- بخش ۲: تصویرساز ---
elif choice == "🎨 تصویرساز":
    st.header("🎨 تولید عکس از متن")
    user_input = st.text_input("توضیح تصویر را اینجا بنویسید:")
    if st.button("✨ شروع طراحی"):
        if user_input:
            with st.spinner("در حال طراحی..."):
                try:
                    res = gemini_model.generate_content(f"Write a short visual English prompt for: {user_input}. ONLY return the prompt.")
                    url = f"https://pollinations.ai/p/{res.text.replace(' ', '%20')}?width=1024&height=1024&seed={time.time()}"
                    st.image(url, caption="نتیجه طراحی")
                except:
                    st.error("خطا در تولید تصویر.")
        else:
            st.warning("لطفاً توضیحی بنویسید.")

# --- بخش ۳: ویرایشگر جادویی ---
elif choice == "🪄 ویرایشگر جادویی":
    st.header("🪄 ویرایش هوشمند تصویر")
    file = st.file_uploader("عکس خود را انتخاب کنید", type=['png', 'jpg', 'jpeg'])
    
    if file:
        img = Image.open(file).convert("RGB")
        st.image(img, caption="تصویر اصلی", width=300)
        
        # کادر پرامپت دقیقاً زیر آپلودر
        instruction = st.text_input("چه تغییری در این عکس ایجاد کنم؟ (مثلاً: پیرهنش رو آبی کن)")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 ویرایش با Gemini"):
                if instruction:
                    with st.spinner("Gemini در حال پردازش..."):
                        try:
                            res = gemini_model.generate_content([f"Modify this image based on: {instruction}. Create a full English prompt for AI generation. ONLY return the prompt.", img])
                            final_url = f"https://pollinations.ai/p/{res.text.replace(' ', '%20')}?width=1024&height=1024"
                            st.image(final_url, caption="نتیجه بازسازی شده")
                        except Exception as e:
                         st.error("خطای دسترسی (403)! سرور قادر به اتصال نیست.")

                                     
