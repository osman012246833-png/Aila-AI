import streamlit as st
from groq import Groq
from gtts import gTTS
import os
import base64
from datetime import datetime
from streamlit_mic_recorder import mic_recorder

# --- 1. إعدادات الهوية والتصميم (ثابت كالصورة) ---
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="stApp"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl; text-align: right; background: #000; color: #ffffff !important;
    }
    .stChatMessage { background-color: rgba(255, 255, 255, 0.05) !important; border-radius: 15px !important; border: 1px solid #ff00ff !important; }
    .main-title { color: #ffffff; text-shadow: 0 0 20px #ff00ff; font-size: 2.5rem; font-weight: bold; text-align: center; }
    .aura-container { text-align: center; padding: 10px; }
    .glowing-aura {
        width: 80px; height: 80px; border: 3px solid #00d4ff; border-radius: 50%;
        display: inline-block; box-shadow: 0 0 30px #00d4ff; animation: pulse 2s infinite alternate;
    }
    @keyframes pulse { from { transform: scale(1); } to { transform: scale(1.05); } }
    /* ستايل سجل المحادثات */
    [data-testid="stSidebar"] { background-color: #111 !important; border-left: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك الصوت والذاكرة ---
def speak(text):
    # استخدام gTTS للنطق بالعربية الفصحى
    tts = gTTS(text=text, lang='ar', slow=False)
    tts.save("aila_voice.mp3")
    with open("aila_voice.mp3", "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" autoplay style="display:none;"></audio>', unsafe_allow_html=True)
    os.remove("aila_voice.mp3")

client = Groq(api_key="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")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [] # سجل المحادثات الكامل (مثل ChatGPT)

# --- 3. السجل الجانبي (Sidebar) ---
with st.sidebar:
    st.markdown("<h2 style='color:#00ffff;'>سجل المحادثات</h2>", unsafe_allow_html=True)
    if st.button("➕ محادثة جديدة"):
        st.session_state.chat_history = []
        st.rerun()
    for i, chat in enumerate(st.session_state.chat_history):
        if chat["role"] == "user":
            st.info(f"🗨️ {chat['content'][:20]}...")

# --- 4. واجهة المستخدم الرئيسية (نفس الصورة) ---
st.markdown("""
    <div class="aura-container">
        <div class="glowing-aura"></div>
        <h1 class="main-title">آيلا | Aila AI</h1>
    </div>
    """, unsafe_allow_html=True)

# عرض الرسائل من الذاكرة
for i, msg in enumerate(st.session_state.chat_history):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            if st.button(f"🔊 قراءة بصوت واضح", key=f"voice_{i}"):
                speak(msg["content"])

# --- 5. نظام الإدخال (صوت + نص) ---
footer_col1, footer_col2 = st.columns([0.1, 0.9])
with footer_col1:
    # ميزة المايك للحديث مع آيلا
    audio = mic_recorder(start_prompt="🎤", stop_prompt="✅", key="recorder")

with footer_col2:
    prompt = st.chat_input("تحدثي معي يا آيلا...")

if audio:
    # ملاحظة: هنا يتم استقبال الصوت، لتحويله لنص تحتاج خدمة Whisper (اختياري)
    st.warning("جاري معالجة صوتك يا زعيم...")

if prompt:
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # برمجة الشخصية (فصحى، ذكاء، احترام للصانع)
        sys_prompt = "أنتِ آيلا AI، مساعدة ذكية جداً تشبهين في قدراتك جيميناي. تتحدثين باللغة العربية الفصحى الراقية. صانعك هو الزعيم عثمان. كوني مصدراً للعون في الرياضيات والعلوم والبحث."
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": sys_prompt}] + st.session_state.chat_history[-10:]
        )
        answer = response.choices[0].message.content
        st.markdown(answer)
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
