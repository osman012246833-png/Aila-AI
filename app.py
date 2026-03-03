import streamlit as st
from groq import Groq
from gtts import gTTS
import os
import base64

# --- 1. الإعدادات وتثبيت التصميم (نفس الصورة بالظبط) ---
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="stApp"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl; text-align: right; background: #000; color: #ffffff !important;
    }
    .main-title { color: #ffffff; text-shadow: 0 0 20px #ff00ff; font-size: 2.5rem; font-weight: bold; text-align: center; }
    .stChatMessage { background-color: rgba(255, 255, 255, 0.05) !important; border-radius: 15px !important; border: 1px solid #ff00ff !important; }
    /* ستايل الميكروفون وأزرار الصوت */
    .audio-btn { cursor: pointer; font-size: 20px; margin-right: 10px; color: #00ffff; }
    </style>
    <div style="text-align: center;">
        <h1 class="main-title">آيلا | Aila AI</h1>
        <div style="display: flex; justify-content: center; gap: 10px; margin-bottom: 20px;">
            <div style="border: 1px solid #00ffff; border-radius: 20px; padding: 5px 15px; background: rgba(0, 255, 255, 0.1);">إشراف الزعيم عثمان</div>
            <div style="border: 1px solid #00ffff; border-radius: 20px; padding: 5px 15px; background: rgba(0, 255, 255, 0.1);">ذكرى 20/11/2008</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 2. الوظائف الذكية (صوت، ذاكرة، مصري) ---
def speak(text):
    tts = gTTS(text=text, lang='ar', slow=False)
    tts.save("temp.mp3")
    with open("temp.mp3", "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" controls autoplay style="display:none;"></audio>', unsafe_allow_html=True)
    os.remove("temp.mp3")

client = Groq(api_key="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")

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. إدارة المحادثة ---
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            if st.button(f"🔊 قراءة", key=f"btn_{i}"):
                speak(msg["content"])

if prompt := st.chat_input("تحدثي معي يا آيلا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # برمجة الشخصية (مصرية، رياضية، بحث)
        sys_msg = "أنتِ آيلا AI، صانعك هو الزعيم عثمان. تتحدثين باللهجة المصرية العامية بذكاء وخفة دم. تجيدين حل الرياضيات والبحث. لو طلب منك صورة، قولي 'جاري التخيل' واكتبي الوصف بالانجليزي بين علامتي []"
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": sys_msg}] + st.session_state.messages[-10:]
        )
        answer = response.choices[0].message.content
        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
