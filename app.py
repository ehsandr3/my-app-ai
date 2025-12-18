import streamlit as st
import requests
import io
import os
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

def remove_bg(image_bytes):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    try:
        response = requests.post(BG_REMOVE_API, headers=headers, data=image_bytes)
        if response.status_code == 200:
            return response.content
    except:
        return None
    return None

# ۲. تنظیمات ظاهر کاملاً ریسپانسیو (بهینه شده برای موبایل)
st.set_page_config(page_title="دستیار هوشمند Gemini", layout="wide", page_icon="🚀")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
    
    html, body, [class*="css"] { 
        font-family: 'Vazirmatn', sans-serif; 
        direction: rtl; 
        text-align: right; 
    }

    /* دکمه‌های تمام عرض و ریسپانسیو */
    .stButton>button { 
        border-radius: 12px; 
        height: 3.5em; 
        background-color: #007BFF; 
        color: white; 
        font-weight: bold; 
        width: 100%; 
        border: none;
        margin-bottom: 10px;
    }

    /* استایل باکس‌های سایدبار */
    .ad-box-whatsapp { background-color: #e6fcf5; border-right: 5px solid #25D366; padding: 12px; border-radius: 10px; margin-bottom: 8px; }
    .ad-box-ads { background-color: #e8f4fd; border-right: 5px solid #0088cc; padding: 12px; border-radius: 10px; margin-bottom: 8px; }
    .ad-box-rubika { background-color: #fff5f5; border-right: 5px solid #f04d4d; padding: 12px; border-radius: 10px; margin-bottom: 8px; }

    /* بهینه‌سازی برای موبایل */
    @media (max-width: 768px) {
        .main .block-container { padding: 10px !important; }
        h1 { font-size: 1.4rem !important; }
        .stImage > img { width: 100% !important; }
    }

    /* افکت اکلیل */
    .glitter-container { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 9999; overflow: hidden; }
    .glitter { position: absolute; top: -10px; background-color: white; border-radius: 50%; opacity: 0.5; animation: fall linear infinite; box-shadow: 0 0 4px #fff; }
    @keyframes fall { 0% { transform: translateY(0); opacity: 0.7; } 100% { transform: translateY(100vh); opacity: 0; } }
    </style>
    
    <div class="glitter-container">
        <div class="glitter" style="left:20%; width:2px; height:2px; animation-duration:8s;"></div>
        <div class="glitter" style="left:50%; width:3px; height:3px; animation-duration:12s;"></div>
        <div class="glitter" style="left:80%; width:2px; height:2px; animation-duration:10s;"></div>
    </div>
    """, unsafe_allow_html=True)

# ۳. منوی کناری (سایدبار)
with st.sidebar:
    st.title("🤖 پنل ابزار AI")
    choice = st.radio("انتخاب ابزار:", ["💬 چت با Gemini", "🎨 تصویرساز", "🪄 ویرایشگر جادویی", "🎬 ابزارهای ویدیو"])
    
    st.divider()
    
    # بخش واتساپ
    st.markdown('<div class="ad-box-whatsapp"><b>📢 گروه واتساپ</b><br><span style="font-size:12px;">آخرین اخبار هوش مصنوعی</span></div>', unsafe_allow_html=True)
    st.link_button("✈️ عضویت در واتساپ", "https://chat.whatsapp.com/CPNm99lQda7I0pfaPnLX3J", use_container_width=True)
    
    # بخش تلگرام
    st.markdown('<div class="ad-box-ads"><b>📬 تلگرام (تبلیغات)</b><br><span style="font-size:12px;">ارتباط با مدیر در تلگرام</span></div>', unsafe_allow_html=True)
    st.link_button("🆔 پیام در تلگرام", "https://t.me/appdotai", use_container_width=True)
    
    # بخش روبیکا
    st.markdown('<div class="ad-box-rubika"><b>📱 روبیکا (تبلیغات)</b><br><span style="font-size:12px;">ارتباط و نظرات در روبیکا</span></div>', unsafe_allow_html=True)
    st.link_button("🚩 ارتباط در روبیکا", "https://rubika.ir/Dreight8", use_container_width=True)
    
    st.divider()
    if st.button("🗑️ پاکسازی کل حافظه", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# ۴. منطق برنامه‌ها
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
            except: st.error("خطا در اتصال!")

elif choice == "🎨 تصویرساز":
    st.header("🎨 تولید عکس از متن")
    user_input = st.text_input("توضیح تصویر:")
    if st.button("✨ شروع طراحی", use_container_width=True):
        if user_input:
            with st.spinner("در حال طراحی..."):
                try:
                    res = gemini_model.generate_content(f"visual prompt: {user_input}. English.")
                    clean_p = res.text.strip().replace(' ', '%20')
                    st.image(f"https://pollinations.ai/p/{clean_p}?width=1024&height=1024&seed={time.time()}", use_container_width=True)
                except: st.error("خطا در تولید تصویر.")

elif choice == "🪄 ویرایشگر جادویی":
    st.header("🪄 ویرایش هوشمند")
    file = st.file_uploader("عکس انتخاب کنید", type=['png', 'jpg', 'jpeg'])
    if file:
        img = Image.open(file).convert("RGB")
        st.image(img, use_container_width=True)
        instruction = st.text_input("تغییر مورد نظر:")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 بازسازی جادویی", use_container_width=True):
                with st.spinner("در حال پردازش..."):
                    try:
                        res = gemini_model.generate_content([f"Describe: {instruction}", img])
                        encoded = requests.utils.quote(res.text.strip())
                        st.image(f"https://pollinations.ai/p/{encoded}?width=1024&height=1024", use_container_width=True)
                    except: st.error("خطا در مدل.")
        with col2:
            if st.button("✂️ حذف پس‌زمینه", use_container_width=True):
                with st.spinner("در حال حذف..."):
                    buf = io.BytesIO(); img.save(buf, format='PNG')
                    result = remove_bg(buf.getvalue())
                    if result:
                        st.image(Image.open(io.BytesIO(result)), use_container_width=True)
                        st.download_button("📥 دانلود", result, "no_bg.png", "image/png", use_container_width=True)

elif choice == "🎬 ابزارهای ویدیو":
    st.header("🎬 ابزارهای ویدیویی")
    st.info("بزودی...")
