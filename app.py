import streamlit as st
from groq import Groq
from gtts import gTTS
import os
import base64
from datetime import datetime
import pytz
from streamlit_mic_recorder import mic_recorder

# --- 1. الهوية وتثبيت التصميم (الشكل الذي لن يتغير أبداً) ---
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="stApp"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl; text-align: right; background: #000; overflow-x: hidden; color: #ffffff !important;
    }
    body::before {
        content: ''; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: url('https://www.transparenttextures.com/patterns/stardust.png') repeat;
        opacity: 0.3; z-index: -1; animation: animateBackground 50s linear infinite;
    }
    @keyframes animateBackground { from { transform: translateX(0) translateY(0); } to { transform: translateX(100px) translateY(100px); } }
    .stChatMessage { background-color: rgba(255, 255, 255, 0.05) !important; border-radius: 15px !important; margin-bottom: 10px !important; }
    [data-testid="stChatMessageUser"] { border: 1px solid #00ffff !important; box-shadow: 0 0 10px rgba(0, 255, 255, 0.3) !important; }
    [data-testid="stChatMessageAssistant"] { border: 1px solid #ff00ff !important; box-shadow: 0 0 10px rgba(255, 0, 255, 0.3) !important; }
    .aura-container { text-align: center; padding: 10px; }
    .glowing-aura {
        width: 100px; height: 100px; border: 3px solid #00d4ff; border-radius: 50%;
        display: inline-block; box-shadow: 0 0 30px #00d4ff; animation: pulse 2s infinite alternate;
    }
    @keyframes pulse { from { transform: scale(1); } to { transform: scale(1.05); } }
    .main-title { color: #ffffff; text-shadow: 0 0 20px #ff00ff; margin: 15px 0; font-size: 2.5rem; font-weight: bold; }
    .pills-container {
        display: flex; justify-content: center; align-items: center; margin-bottom: 25px;
        border: 2px solid #00ffff; border-radius: 25px; width: fit-content; margin-left: auto; margin-right: auto;
        background: rgba(0, 255, 255, 0.1); overflow: hidden;
    }
    .pill-segment { padding: 5px 20px; color: #ffffff; font-weight: bold; font-size: 14px; white-space: nowrap; }
    [data-testid="stChatInputContainer"] { border: 2px solid #ff00ff !important; background-color: rgba(0, 0, 0, 0.7) !important; }
    </style>
    <div class="aura-container">
        <div class="glowing-aura"></div>
        <h1 class="main-title">آيلا | Aila AI</h1>
    </div>
    """, unsafe_allow_html=True)

# --- 2. محركات الصوت والمعرفة الشاملة ---
def speak(text):
    tts = gTTS(text=text, lang='ar', slow=False) # نطق فصحى متزن
    tts.save("aila.mp3")
    with open("aila.mp3", "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" autoplay style="display:none;"></audio>', unsafe_allow_html=True)
    os.remove("aila.mp3")

client = Groq(api_key="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")

if "messages" not in st.session_state: st.session_state.messages = []
if "is_authenticated" not in st.session_state: st.session_state.is_authenticated = False
if "is_maker" not in st.session_state: st.session_state.is_maker = False

# --- 3. نظام الحماية والسجل (نظام ChatGPT) ---
if not st.session_state.is_authenticated:
    user_input = st.text_input("من يود التحدث مع آيلا؟", placeholder="اكتب اسمك أو كود الصانع...")
    if st.button("دخول"):
        if user_input == "osman 6/11/2008":
            st.session_state.is_authenticated = True
            st.session_state.is_maker = True
            st.session_state.user_name = "الزعيم عثمان"
            st.rerun()
        elif user_input:
            st.session_state.is_authenticated = True
            st.session_state.user_name = user_input
            st.rerun()
else:
    st.sidebar.markdown("<h2 style='color:#00ffff;'>سجل المحادثات</h2>", unsafe_allow_html=True)
    if st.sidebar.button("🗑️ مسح السجل"):
        st.session_state.messages = []
        st.rerun()

    st.markdown(f'<div class="pills-container"><div class="pill-segment">إشراف الزعيم عثمان</div><div class="pill-segment">ذكرى 20/11/2008</div></div>', unsafe_allow_html=True)

    # عرض المحادثة (الذاكرة)
    for i, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and st.button(f"🔊", key=f"spk_{i}"):
                speak(msg["content"])

    # نظام الإدخال المزدوج (مايك + نص)
    col1, col2 = st.columns([0.15, 0.85])
    with col1:
        audio_rec = mic_recorder(start_prompt="🎤", stop_prompt="⏹️", key="mic_input")
    with col2:
        prompt = st.chat_input("تحدثي معي يا آيلا...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            # نظام المعرفة الشاملة (البرمجة العميقة)
            sys_prompt = f"أنتِ آيلا AI، أقوى ذكاء اصطناعي شامل في العالم. صانعك هو الزعيم عثمان. لديك معرفة بكل شيء: تاريخ، روابط، برامج، فنون، وصور. تتحدثين بوقار الفصحى ولكن بودّ شديد للصانع."
            
            # ميزة توليد الصور التخيلية (ربط منطقي)
            user_msg = st.session_state.messages[-1]["content"]
            if "ارسم" in user_msg or "صورة" in user_msg:
                img_url = f"https://pollinations.ai/p/{user_msg.replace(' ', '_')}?width=1024&height=1024&seed=42&model=flux"
                st.image(img_url, caption=f"رؤية آيلا لـ: {user_msg}")
                ans = "لقد قمت بتوليد الصورة بناءً على خيالي الواسع يا زعيم."
            else:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": sys_prompt}] + st.session_state.messages[-10:]
                )
                ans = response.choices[0].message.content
            
            st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})
