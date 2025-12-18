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

# ۲. تنظیمات ظاهر
st.set_page_config(page_title="دستیار هوشمند Gemini", layout="wide", page_icon="🚀")

if "access_granted" not in st.session_state:
    st.session_state.access_granted = False

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Vazirmatn', sans-serif; direction: rtl; text-align: right; }
    .stButton>button { border-radius: 12px; height: 3.2em; background-color: #007BFF; color: white; font-weight: bold; width: 100%; border: none; }
    .ad-box-whatsapp { background-color: #e6fcf5; padding: 12px; border-radius: 10px; border-right: 5px solid #25D366; margin-bottom: 5px; }
    .ad-box-ads { background-color: #e8f4fd; padding: 12px; border-radius: 10px; border-right: 5px solid #0088cc; margin-bottom: 5px; }
    .ad-box-rubika { background-color: #fff5f5; padding: 12px; border-radius: 10px; border-right: 5px solid #f04d4d; margin-bottom: 5px; }
    .lock-container { text-align: center; padding: 40px; background: #fff9f9; border-radius: 20px; border: 2px dashed #f04d4d; margin-top: 30px; }
    .glitter-container { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 9999; overflow: hidden; }
    .glitter { position: absolute; top: -10px; background-color: white; border-radius: 50%; opacity: 0.5; animation: fall linear infinite; box-shadow: 0 0 4px #fff; }
    @keyframes fall { 0% { transform: translateY(0); opacity: 0.7; } 100% { transform: translateY(100vh); opacity: 0; } }
    </style>
    <div class="glitter-container">
        <div class="glitter" style="left:10%; width:2px; height:2px; animation-duration:8s;"></div>
        <div class="glitter" style="left:40%; width:3px; height:3px; animation-duration:12s;"></div>
        <div class="glitter" style="left:70%; width:2px; height:2px; animation-duration:10s;"></div>
        <div class="glitter" style="left:90%; width:3px; height:3px; animation-duration:15s;"></div>
    </div>
    """, unsafe_allow_html=True)

# بررسی دسترسی
if not st.session_state.access_granted:
    st.markdown('<div class="lock-container"><h1 style="color:#f04d4d;">🔒 بخش ابزارها قفل است</h1><p>برای استفاده از امکانات، ابتدا عضو گروه واتساپ شوید.</p></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: st.link_button("🟢 ۱. عضویت در واتساپ", "https://chat.whatsapp.com/CPNm99lQda7I0pfaPnLX3J", use_container_width=True)
    with c2: 
        if st.button("✅ ۲. عضو شدم، باز کن"):
            st.session_state.access_granted = True
            st.rerun()
    st.stop()

# ۳. منوی کناری
with st.sidebar:
    st.title("🤖 پنل ابزار AI")
    choice = st.radio("انتخاب ابزار:", ["💬 چت با Gemini", "🎨 تصویرساز", "🪄 ویرایشگر جادویی", "🎬 ابزارهای ویدیو"])
    st.divider()
    st.markdown('<div class="ad-box-whatsapp"><b>📢 گروه واتساپ</b><br>شما عضو هستید ✅</div>', unsafe_allow_html=True)
    st.link_button("✈️ لینک گروه واتساپ", "https://chat.whatsapp.com/CPNm99lQda7I0pfaPnLX3J", use_container_width=True)
    st.write("")
    st.markdown('<div class="ad-box-ads"><b>📬 تلگرام (تبلیغات)</b><br>ارتباط با مدیر</div>', unsafe_allow_html=True)
    st.link_button("🆔 پیام در تلگرام", "https://t.me/appdotai", use_container_width=True)
    st.write("")
    st.markdown('<div class="ad-box-rubika"><b>📱 روبیکا (تبلیغات)</b><br>ارتباط و نظرات</div>', unsafe_allow_html=True)
    st.link_button("🚩 ارتباط در روبیکا", "https://rubika.ir/Dreight8", use_container_width=True)
    st.divider()
    if st.button("🗑️ پاکسازی و قفل مجدد", use_container_width=True):
        st.session_state.clear()
        st.session_state.access_granted = False
        st.rerun()

# --- منطق برنامه‌ها ---
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
    u_in = st.text_input("توضیح تصویر:")
    if st.button("✨ شروع طراحی", use_container_width=True):
        if u_in:
            with st.spinner("در حال طراحی..."):
                try:
                    res = gemini_model.generate_content(f"visual prompt: {u_in}. English.")
                    clean_p = res.text.strip().replace(' ', '%20')
                    st.image(f"https://pollinations.ai/p/{clean_p}?width=1024&height=1024&seed={time.time()}", use_container_width=True)
                except: st.error("خطا!")

elif choice == "🪄 ویرایشگر جادویی":
    st.header("🪄 ویرایش هوشمند")
    file = st.file_uploader("عکس انتخاب کنید", type=['png', 'jpg', 'jpeg'])
    if file:
        img = Image.open(file).convert("RGB")
        st.image(img, caption="تصویر اصلی", use_container_width=True)
        instr = st.text_input("تغییر مورد نظر:")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 بازسازی جادویی", use_container_width=True):
                with st.spinner("در حال پردازش..."):
                    try:
                        res = gemini_model.generate_content([f"Describe: {instr}", img])
                        enc = requests.utils.quote(res.text.strip())
                        st.image(f"https://pollinations.ai/p/{enc}?width=1024&height=1024", use_container_width=True)
                    except: st.error("خطا!")
        with col2:
            if st.button("✂️ حذف پس‌زمینه", use_container_width=True):
                with st.spinner("در حال حذف..."):
                    buf = io.BytesIO(); img.save(buf, format='PNG')
                    res_bytes = remove_bg(buf.getvalue())
                    if res_bytes:
                        st.image(Image.open(io.BytesIO(res_bytes)), use_container_width=True)
                        st.download_button("📥 دانلود عکس", res_bytes, "no_bg.png", "image/png", use_container_width=True)

elif choice == "🎬 ابزارهای ویدیو":
    st.header("🎬 ابزارهای ویدیویی")
    st.info("بزودی...")
