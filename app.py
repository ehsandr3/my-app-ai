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

# پیکربندی Gemini با مدیریت خطا
try:
    genai.configure(api_key=GEMINI_KEY)
    gemini_model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    pass

# تابع کمکی برای حذف پس‌زمینه
def remove_bg(image_bytes):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    try:
        response = requests.post(BG_REMOVE_API, headers=headers, data=image_bytes)
        if response.status_code == 200:
            return response.content
    except:
        return None
    return None

# ۲. تنظیمات ظاهر برنامه (ریسپانسیو، استایل و اکلیل)
st.set_page_config(page_title="دستیار هوشمند Gemini", layout="wide", page_icon="🚀")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
    
    html, body, [class*="css"] { 
        font-family: 'Vazirmatn', sans-serif; 
        direction: rtl; 
        text-align: right; 
    }

    /* استایل دکمه‌ها برای نمایش بهتر در موبایل و دسکتاپ */
    .stButton>button { 
        border-radius: 12px; 
        height: 3.2em; 
        background-color: #007BFF; 
        color: white; 
        transition: 0.3s; 
        border: none;
        font-weight: bold;
        width: 100%;
    }
    .stButton>button:hover { background-color: #0056b3; transform: scale(1.01); }

    /* ریسپانسیو کردن بدنه اصلی برای موبایل */
    @media (max-width: 768px) {
        .main .block-container { padding: 10px; }
        h1 { font-size: 1.6rem !important; }
        .stImage > img { width: 100% !important; }
    }

    /* باکس تبلیغات در سایدبار */
    .ad-box { 
        background-color: #f0f2f6; 
        padding: 15px; 
        border-radius: 10px; 
        border-right: 5px solid #25D366; 
        margin-top: 20px; 
        text-align: center;
    }

    /* --- افکت اکلیل ریز و براق --- */
    .glitter-container {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        pointer-events: none; z-index: 9999; overflow: hidden;
    }
    .glitter {
        position: absolute; top: -10px; background-color: white;
        border-radius: 50%; opacity: 0.6; animation: fall linear infinite;
        box-shadow: 0 0 4px #fff, 0 0 8px #fff;
    }
    @keyframes fall {
        0% { transform: translateY(0) scale(1); opacity: 0.8; }
        100% { transform: translateY(100vh) scale(0.5); opacity: 0; }
    }
    </style>

    <div class="glitter-container">
        <div class="glitter" style="left: 10%; width: 2px; height: 2px; animation-duration: 8s;"></div>
        <div class="glitter" style="left: 25%; width: 3px; height: 3px; animation-duration: 11s;"></div>
        <div class="glitter" style="left: 45%; width: 2px; height: 2px; animation-duration: 9s;"></div>
        <div class="glitter" style="left: 65%; width: 4px; height: 4px; animation-duration: 14s;"></div>
        <div class="glitter" style="left: 85%; width: 2px; height: 2px; animation-duration: 10s;"></div>
    </div>
    """, unsafe_allow_html=True)

# ۳. منوی کناری (Sidebar)
with st.sidebar:
    st.title("🤖 پنل ابزار AI")
    choice = st.radio("انتخاب ابزار:", ["💬 چت با Gemini", "🎨 تصویرساز", "🪄 ویرایشگر جادویی", "🎬 ابزارهای ویدیو"])
    
    st.divider()
    
    # بخش تبلیغات واتساپ
    st.markdown("""
        <div class="ad-box">
            <h4 style='margin:0; color: #128C7E;'>📢 به ما بپیوندید</h4>
            <p style='font-size: 13px; color: #555;'>آخرین اخبار هوش مصنوعی در واتساپ</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.link_button("✈️ گروه واتساپ ما را دنبال کنید", "https://chat.whatsapp.com/CPNm99lQda7I0pfaPnLX3J?mode=wwt", use_container_width=True)
    
    st.divider()
    
    if st.button("🗑️ پاکسازی کل حافظه", use_container_width=True):
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
            except:
                st.error("❌ خطا در اتصال! لطفاً فیلترشکن یا DNS خود را بررسی کنید.")

# --- بخش ۲: تصویرساز ---
elif choice == "🎨 تصویرساز":
    st.header("🎨 تولید عکس از متن")
    user_input = st.text_input("توضیح تصویر را اینجا بنویسید (فارسی یا انگلیسی):")
    if st.button("✨ شروع طراحی", use_container_width=True):
        if user_input:
            with st.spinner("در حال طراحی..."):
                try:
                    # ترجمه خودکار به انگلیسی برای کیفیت بهتر در تولید تصویر
                    res = gemini_model.generate_content(f"Translate this to a visual prompt: {user_input}. Only English.")
                    clean_prompt = res.text.strip().replace(' ', '%20')
                    url = f"https://pollinations.ai/p/{clean_prompt}?width=1024&height=1024&seed={time.time()}"
                    st.image(url, caption="نتیجه طراحی", use_container_width=True)
                except:
                    st.error("خطا در تولید تصویر.")
        else:
            st.warning("لطفاً توضیحی بنویسید.")

# --- بخش ۳: ویرایشگر جادویی ---
elif choice == "🪄 ویرایشگر جادویی":
    st.header("🪄 ویرایش و بازسازی هوشمند")
    file = st.file_uploader("عکس خود را انتخاب کنید", type=['png', 'jpg', 'jpeg'])
    
    if file:
        img = Image.open(file).convert("RGB")
        st.image(img, caption="تصویر اصلی", use_container_width=True)
        
        instruction = st.text_input("چه تغییری در این عکس ایجاد کنم؟")
        
        st.divider()
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚀 بازسازی با Gemini", use_container_width=True):
                if instruction:
                    with st.spinner("در حال بازسازی..."):
                        try:
                            prompt_query = f"Describe this image but with this change: {instruction}. Concise English only."
                            res = gemini_model.generate_content([prompt_query, img])
                            refined_prompt = res.text.strip().replace('\n', ' ')
                            encoded_prompt = requests.utils.quote(refined_prompt)
                            final_url = f"https://pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&seed={time.time()}"
                            st.image(final_url, caption="نتیجه جدید", use_container_width=True)
                        except Exception as e:
                            st.error(f"خطا: {e}")
                else:
                    st.warning("دستور تغییر را وارد کنید.")

        with col2:
            if st.button("✂️ حذف پس‌زمینه", use_container_width=True):
                with st.spinner("در حال حذف پس‌زمینه..."):
                    try:
                        buf = io.BytesIO()
                        img.save(buf, format='PNG')
                        byte_im = buf.getvalue()
                        result_bytes = remove_bg(byte_im)
                        if result_bytes:
                            st.image(Image.open(io.BytesIO(result_bytes)), caption="بدون پس‌زمینه", use_container_width=True)
                            st.download_button("📥 دانلود PNG", result_bytes, "no_bg.png", "image/png", use_container_width=True)
                        else:
                            st.error("خطا در سرویس حذف پس‌زمینه.")
                    except Exception as e:
                        st.error(f"خطا: {e}")

# --- بخش ۴: ابزارهای ویدیو ---
elif choice == "🎬 ابزارهای ویدیو":
    st.header("🎬 ابزارهای ویدیویی")
    st.info("این بخش در حال توسعه است. بزودی قابلیت تولید ویدیو اضافه خواهد شد!")
