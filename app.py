import streamlit as st
from groq import Groq
from gtts import gTTS
import os
import base64
from datetime import datetime
import pytz

# 1. إعدادات الهوية (الأيقونة والاسم)
st.markdown('<link rel="shortcut icon" href="https://raw.githubusercontent.com/osman012246833-png/Aila-AI/main/icon.png">', unsafe_allow_html=True)

st.set_page_config(page_title="Aila AI", page_icon="💠", layout="centered")

# 2. دالة الصوت (أنثوي ناعم)
def speak(text):
    tts = gTTS(text=text, lang='ar', slow=False)
    tts.save("response.mp3")
    with open("response.mp3", "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
        st.markdown(md, unsafe_allow_html=True)
    os.remove("response.mp3")

# 3. ميزة معرفة الوقت
def get_time():
    tz = pytz.timezone('Africa/Cairo')
    return datetime.now(tz).strftime("%I:%M %p").replace("AM", "صباحاً").replace("PM", "مساءً")

# --- واجهة التطبيق ---
st.title("💠 Aila AI")
st.write(f"مرحباً بك يا زعيم عثمان! الساعة الآن: {get_time()}")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("اسأل آيلا أي شيء..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if "الساعة" in prompt or "الوقت" in prompt:
            full_response = f"الساعة الآن في القاهرة هي {get_time()}."
        else:
            # هنا نضع كود Groq الخاص بك للرد الذكي
            full_response = "أنا آيلا، مساعدتك الذكية بصوت جديد!" 
        
        st.markdown(full_response)
        speak(full_response) # تشغيل الصوت فوراً

    st.session_state.messages.append({"role": "assistant", "content": full_response})
