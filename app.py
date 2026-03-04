import streamlit as st
from groq import Groq
from gtts import gTTS
import os
import base64
from datetime import datetime
import pytz
from streamlit_mic_recorder import mic_recorder

# --- 1. الهوية والأيقونة ---
st.markdown('<link rel="shortcut icon" href="https://raw.githubusercontent.com/osman012246833-png/Aila-AI/main/icon.png">', unsafe_allow_html=True)
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="centered")

# --- 2. دالة الصوت (بالمصري وبدون أخطاء) ---
def speak(text):
    tts = gTTS(text=text, lang='ar', slow=False)
    tts.save("temp.mp3")
    with open("temp.mp3", "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" autoplay style="display:none;"></audio>', unsafe_allow_html=True)
    os.remove("temp.mp3")

def get_time():
    tz = pytz.timezone('Africa/Cairo')
    return datetime.now(tz).strftime("%I:%M %p").replace("AM", "صباحاً").replace("PM", "مساءً")

# --- 3. تصميم الواجهة (نفس الصورة الأصلية 100%) ---
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
    @keyframes animateBackground {
        from { transform: translateX(0) translateY(0); }
        to { transform: translateX(100px) translateY(100px); }
    }
    .stChatMessage { background-color: rgba(255, 255, 255, 0.05) !important; border-radius: 15px !important; padding: 10px !important; margin-bottom: 10px !important; }
    [data-testid="stChatMessageUser"] { border: 1px solid #00ffff !important; box-shadow: 0 0 10px rgba(0, 255, 255, 0.3) !important; }
    [data-testid="stChatMessageAssistant"] { border: 1px solid #ff00ff !important; box-shadow: 0 0 10px rgba(255, 0, 255, 0.3) !important; }
    .stChatMessage p { color: #ffffff !important; font-size: 18px !important; text-shadow: 1px 1px 3px #000000; }
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
    .pill-divider { width: 2px; height: 20px; background-color: #00ffff; }
    [data-testid="stChatInputContainer"] { border: 2px solid #ff00ff !important; background-color: rgba(0, 0, 0, 0.7) !important; }
    .stButton>button { background: transparent; color: #00ffff; border: 1px solid #00ffff; border-radius: 10px; font-size: 12px; }
    </style>
    <div class="aura-container">
        <div class="glowing-aura"></div>
        <h1 class="main-title">آيلا | Aila AI</h1>
    </div>
    """, unsafe_allow_html=True)

# --- 4. محرك الذكاء والذاكرة ---
client = Groq(api_key="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")
SECRET_CODE = "osman 6/11/2008" 

if "messages" not in st.session_state: st.session_state.messages = []
if "is_authenticated" not in st.session_state: st.session_state.is_authenticated = False
if "is_maker" not in st.session_state: st.session_state.is_maker = False

if not st.session_state.is_authenticated:
    st.markdown("<center><p style='color: #00ffff; font-weight: bold; font-size: 18px;'>من يود التحدث مع آيلا؟</p></center>", unsafe_allow_html=True)
    user_input = st.text_input("", placeholder="اكتب اسمك هنا...")
    if st.button("دخول"):
        if user_input == SECRET_CODE:
            st.session_state.is_authenticated = True
            st.session_state.is_maker = True
            st.session_state.user_display_name = "الزعيم عثمان"
            st.rerun()
        elif user_input:
            st.session_state.is_authenticated = True
            st.session_state.user_display_name = user_input.replace("الزعيم", "").strip()
            st.rerun()
else:
    st.markdown(f"""
        <div class="pills-container">
            <div class="pill-segment">إشراف الزعيم عثمان</div>
            <div class="pill-divider"></div>
            <div class="pill-segment">ذكرى 20/11/2008</div>
        </div>
    """, unsafe_allow_html=True)

    # عرض سجل المحادثات (الذاكرة)
    for i, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(f"<p>{msg['content']}</p>", unsafe_allow_html=True)
            if msg["role"] == "assistant":
                if st.button(f"🔊 اسمع", key=f"audio_{i}"):
                    speak(msg["content"])

    # منطقة الإدخال (صوت وكتابة)
    col1, col2 = st.columns([0.15, 0.85])
    with col1:
        audio_input = mic_recorder(start_prompt="🎤", stop_prompt="⏹️", key="mic")
    
    with col2:
        prompt = st.chat_input("تحدثي معي يا آيلا...")

    final_prompt = prompt
    if audio_input and 'transcription' in audio_input: # ملاحظة: تحتاج ربط API للتحويل
         final_prompt = audio_input['transcription']

    if final_prompt:
        st.session_state.messages.append({"role": "user", "content": final_prompt})
        st.rerun()

    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        user_msg = st.session_state.messages[-1]["content"]
        with st.chat_message("assistant"):
            try:
                # تعليمات الشخصية (البرمجة العميقة)
                if st.session_state.is_maker:
                    sys_prompt = f"أنتِ آيلا AI. صانعك هو الزعيم عثمان. ردي بالمصري العامية بخفة دم وحب وتقدير. استخدمي 'يا ملكي'، 'يا زعيم'. الساعة الآن {get_time()}. حلي الرياضيات ببراعة وابحثي في الانترنت بدقة."
                else:
                    sys_prompt = f"أنتِ آيلا AI. تتحدثين مع {st.session_state.user_display_name}. صانعك هو الزعيم عثمان. تحدثي بالمصري المفهوم بذكاء."

                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": sys_prompt}] + st.session_state.messages[-15:],
                    temperature=0.8
                )
                answer = response.choices[0].message.content
                st.markdown(f"<p>{answer}</p>", unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"عذراً يا زعيم، فيه عطل: {e}")
