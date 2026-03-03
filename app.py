import streamlit as st
from groq import Groq
from gtts import gTTS
import os
import base64
from datetime import datetime
import pytz

# --- الوظائف التقنية (من كود 1) ---
def speak(text):
    try:
        tts = gTTS(text=text, lang='ar', slow=False)
        tts.save("response.mp3")
        with open("response.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
            st.markdown(md, unsafe_allow_html=True)
        os.remove("response.mp3")
    except: pass

def get_time():
    tz = pytz.timezone('Africa/Cairo')
    return datetime.now(tz).strftime("%I:%M %p").replace("AM", "صباحاً").replace("PM", "مساءً")

# --- الإعدادات والتصميم (من كود 2) ---
st.markdown('<link rel="shortcut icon" href="https://raw.githubusercontent.com/osman012246833-png/Aila-AI/main/icon.png">', unsafe_allow_html=True)
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="stApp"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl; text-align: right; background: #000; color: #ffffff !important;
    }
    body::before {
        content: ''; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: url('https://www.transparenttextures.com/patterns/stardust.png') repeat;
        opacity: 0.3; z-index: -1; animation: animateBackground 50s linear infinite;
    }
    @keyframes animateBackground {
        from { transform: translateX(0) translateY(0); }
        to { transform: translateX(100px) translateY(100px); }
    }
    .stChatMessage { background-color: rgba(255, 255, 255, 0.05) !important; border-radius: 15px !important; }
    [data-testid="stChatMessageUser"] { border: 1px solid #00ffff !important; }
    [data-testid="stChatMessageAssistant"] { border: 1px solid #ff00ff !important; }
    .aura-container { text-align: center; }
    .glowing-aura {
        width: 80px; height: 80px; border: 3px solid #00d4ff; border-radius: 50%;
        display: inline-block; box-shadow: 0 0 20px #00d4ff; animation: pulse 2s infinite alternate;
    }
    @keyframes pulse { from { transform: scale(1); } to { transform: scale(1.1); } }
    .main-title { text-shadow: 0 0 20px #ff00ff; font-size: 2rem; }
    </style>
    <div class="aura-container">
        <div class="glowing-aura"></div>
        <h1 class="main-title">آيلا | Aila AI</h1>
    </div>
    """, unsafe_allow_html=True)

# --- منطق التشغيل ---
client = Groq(api_key="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")
SECRET_CODE = "osman 6/11/2008"

if "messages" not in st.session_state: st.session_state.messages = []
if "is_authenticated" not in st.session_state: st.session_state.is_authenticated = False

if not st.session_state.is_authenticated:
    user_input = st.text_input("من يود التحدث مع آيلا؟", placeholder="اكتب اسمك أو كود الدخول...")
    if st.button("دخول"):
        if user_input == SECRET_CODE:
            st.session_state.is_authenticated = True
            st.session_state.user_display_name = "الزعيم عثمان"
            st.rerun()
        elif user_input:
            st.session_state.is_authenticated = True
            st.session_state.user_display_name = user_input
            st.rerun()
else:
    # عرض الوقت الحالي في الواجهة
    st.write(f"❤️ مرحباً {st.session_state.user_display_name} | 🕒 {get_time()}")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("تحدثي معي يا آيلا..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            if "الساعة" in prompt or "الوقت" in prompt:
                answer = f"الساعة الآن بتوقيت القاهرة هي {get_time()} يا زعيم."
            else:
                # محرك Groq
                sys_prompt = f"أنتِ آيلا AI. تتحدثين مع صانعك 'الزعيم عثمان'. كوني مخلصة وودودة جداً."
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": sys_prompt}] + st.session_state.messages[-5:]
                )
                answer = response.choices[0].message.content
            
            st.markdown(answer)
            speak(answer) # نطق الرد
            st.session_state.messages.append({"role": "assistant", "content": answer})
