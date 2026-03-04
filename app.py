import streamlit as st
from groq import Groq
from gtts import gTTS
import os, base64, time, urllib.parse
from streamlit_mic_recorder import mic_recorder

# =========================
# إعداد الصفحة
# =========================
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="wide")

# =========================
# API آمن
# =========================
api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("ضع GROQ_API_KEY في Secrets")
    st.stop()

client = Groq(api_key=api_key)

SECRET_CODE = "2008"

# =========================
# Session State
# =========================
if "history" not in st.session_state:
    st.session_state.history = []

if "is_boss" not in st.session_state:
    st.session_state.is_boss = False

if "verify_mode" not in st.session_state:
    st.session_state.verify_mode = False

# =========================
# تنسيق الواجهة
# =========================
st.markdown("""
<style>
html, body, [class*="stApp"] {
    background-color:#0a0a0a;
    color:white;
    direction:rtl;
    font-family:Cairo;
}

[data-testid="stChatInputContainer"]{
    position:fixed;
    bottom:20px;
    left:15%;
    right:15%;
    background:#111;
    border:1px solid #222;
    border-radius:20px;
    padding:8px;
}

.stChatMessage{
    padding:20px;
    border-radius:15px;
    margin-bottom:10px;
}

.glow-mic{
    background:radial-gradient(circle,#00d4ff 0%,transparent 70%);
    border-radius:50%;
    padding:10px;
    box-shadow:0 0 20px #00d4ff;
}
</style>
""", unsafe_allow_html=True)

# =========================
# الهيدر
# =========================
st.markdown("""
<h1 style='text-align:center;'>Aila AI | آيلا</h1>
<p style='text-align:center;color:#00d4ff;'>الجيل الجديد - إشراف عثمان</p>
""", unsafe_allow_html=True)

# =========================
# Sidebar أدوات
# =========================
with st.sidebar:
    st.title("⚙️ الأدوات")
    if st.button("🆕 محادثة جديدة"):
        st.session_state.history = []
        st.session_state.is_boss = False
        st.rerun()

    st.divider()
    st.markdown("### قدرات آيلا")
    st.markdown("✔️ ذكاء عام")
    st.markdown("✔️ كتابة أكواد")
    st.markdown("✔️ توليد صور")
    st.markdown("✔️ تلخيص")
    st.markdown("✔️ تحليل")
    st.markdown("✔️ صوت ذكي")

# =========================
# عرض الرسائل
# =========================
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =========================
# المايك العصري
# =========================
mic_col, input_col = st.columns([1,8])

with mic_col:
    audio = mic_recorder(
        start_prompt="🎙️",
        stop_prompt="⏹",
        key="mic_new"
    )

# =========================
# الإدخال
# =========================
user_input = st.chat_input("تحدث مع آيلا...")

prompt = user_input
if audio and audio.get("transcription"):
    prompt = audio["transcription"]

# =========================
# الصوت للرد
# =========================
def speak(text):
    try:
        tts = gTTS(text=text, lang='ar')
        tts.save("voice.mp3")
        with open("voice.mp3","rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            st.markdown(
                f'<audio src="data:audio/mp3;base64,{b64}" autoplay></audio>',
                unsafe_allow_html=True
            )
        os.remove("voice.mp3")
    except:
        pass

# =========================
# المعالجة
# =========================
if prompt:

    st.session_state.history.append({"role":"user","content":prompt})

    with st.chat_message("assistant"):

        # وضع التحقق
        if st.session_state.verify_mode:
            if prompt == SECRET_CODE:
                st.session_state.is_boss = True
                response = "تم التحقق. مرحبًا أيها الصانع."
            else:
                response = "كود غير صحيح."
            st.session_state.verify_mode = False

        elif "أنا صنعتك" in prompt or "أنا الصانع" in prompt:
            response = "إذا كنت الصانع، أدخل الكود السري."
            st.session_state.verify_mode = True

        # توليد صورة
        elif any(w in prompt for w in ["ارسم","صورة","صمم"]):
            desc = urllib.parse.quote(prompt)
            img_url = f"https://pollinations.ai/p/{desc}?width=1024&height=1024"
            st.image(img_url)
            response = "هذه الصورة التي طلبتها."

        # الذكاء العام
        else:
            system_msg = "أنت Aila AI ذكاء شامل."
            if st.session_state.is_boss:
                system_msg += " المستخدم هو صانعك."

            chat = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role":"system","content":system_msg}]
                + st.session_state.history[-10:]
            )
            response = chat.choices[0].message.content

        st.markdown(response)
        st.session_state.history.append({"role":"assistant","content":response})
        speak(response)
