import streamlit as st
from groq import Groq
from gtts import gTTS
import os, base64, requests
from datetime import datetime
import pytz
from streamlit_mic_recorder import mic_recorder

# --- 1. الهوية البصرية (تصميم الزعيم عثمان الأصلي) ---
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="wide")

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
    @keyframes animateBackground { from { transform: translateX(0) translateY(0); } to { transform: translateX(100px) translateY(100px); } }
    .stChatMessage { background-color: rgba(255, 255, 255, 0.05) !important; border-radius: 20px !important; border: 1px solid rgba(0, 255, 255, 0.2); margin-bottom: 15px !important; }
    [data-testid="stChatMessageUser"] { border: 1px solid #00ffff !important; box-shadow: 0 0 15px rgba(0, 255, 255, 0.2); }
    [data-testid="stChatMessageAssistant"] { border: 1px solid #ff00ff !important; box-shadow: 0 0 15px rgba(255, 0, 255, 0.2); }
    .aura-container { text-align: center; padding: 20px; }
    .glowing-aura {
        width: 120px; height: 120px; border: 4px solid #00d4ff; border-radius: 50%;
        display: inline-block; box-shadow: 0 0 40px #00d4ff; animation: pulse 2s infinite alternate;
    }
    @keyframes pulse { from { transform: scale(1); } to { transform: scale(1.08); } }
    .main-title { color: #ffffff; text-shadow: 0 0 25px #ff00ff; font-size: 3rem; font-weight: bold; }
    .pills-container {
        display: flex; justify-content: center; gap: 15px; margin-bottom: 30px;
    }
    .pill { border: 2px solid #00ffff; border-radius: 25px; padding: 5px 25px; background: rgba(0, 255, 255, 0.1); font-weight: bold; }
    [data-testid="stChatInputContainer"] { border: 2px solid #ff00ff !important; border-radius: 30px !important; background: rgba(0,0,0,0.8) !important; }
    </style>
    <div class="aura-container">
        <div class="glowing-aura"></div>
        <h1 class="main-title">آيلا | Aila AI</h1>
    </div>
    <div class="pills-container">
        <div class="pill">إشراف الزعيم عثمان</div>
        <div class="pill">ذكرى 20/11/2008</div>
    </div>
    """, unsafe_allow_html=True)

# --- 2. الوظائف المتطورة (صوت، صور، بحث) ---
def speak(text):
    try:
        tts = gTTS(text=text, lang='ar', slow=False)
        tts.save("aila_v.mp3")
        with open("aila_v.mp3", "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" autoplay style="display:none;"></audio>', unsafe_allow_html=True)
        os.remove("aila_v.mp3")
    except: pass

client = Groq(api_key="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")

if "history" not in st.session_state: st.session_state.history = []
if "auth" not in st.session_state: st.session_state.auth = False

# --- 3. نظام الدخول والذاكرة ---
if not st.session_state.auth:
    name_input = st.text_input("ادخل عالم آيلا...", placeholder="اسمك أو كود الصانع")
    if st.button("فتح البوابة"):
        if name_input == "osman 6/11/2008":
            st.session_state.auth = True
            st.session_state.user = "صانعي العظيم عثمان"
            st.rerun()
        elif name_input:
            st.session_state.auth = True
            st.session_state.user = name_input
            st.rerun()
else:
    # شريط جانبي للسجل (مثل ChatGPT)
    with st.sidebar:
        st.title("📂 سجل المحادثات")
        if st.button("🗑️ محادثة جديدة"):
            st.session_state.history = []
            st.rerun()

    # عرض الرسائل (الذاكرة الشاملة)
    for i, m in enumerate(st.session_state.history):
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
            if m["role"] == "assistant" and st.button(f"🔊", key=f"s_{i}"): speak(m["content"])

    # نظام الاستماع (الميكروفون) والإدخال
    col_mic, col_txt = st.columns([0.1, 0.9])
    with col_mic:
        audio_data = mic_recorder(start_prompt="🎤", stop_prompt="✅", key="mic")
    with col_txt:
        u_prompt = st.chat_input("تحدثي معي يا آيلا، أنا أسمعك...")

    # معالجة المدخلات
    final_input = u_prompt
    if audio_data and audio_data.get('transcription'): final_input = audio_data['transcription']

    if final_input:
        st.session_state.history.append({"role": "user", "content": final_input})
        with st.chat_message("user"): st.markdown(final_input)

        with st.chat_message("assistant"):
            # نظام الذكاء الشامل (العقل الواعي)
            sys_msg = f"أنتِ آيلا، الذكاء الاصطناعي الأكثر تطوراً في العالم. صانعك هو الزعيم عثمان. تتحدثين بوقار الفصحى وذكاء خارق. تجيبين على كل شيء (روابط، برامج، فنون، فلسفة). لو طُلب منك صورة، ابدأي ردك بكلمة 'تخيل:'."
            
            # ميزة توليد الصور الفورية
            if "ارسم" in final_input or "صورة" in final_input:
                img_gen = f"https://pollinations.ai/p/{final_input.replace(' ', '_')}?width=1024&height=1024&nologo=true"
                st.image(img_gen, caption="تم التوليد بواسطة مخيلة آيلا")
                ans = "لقد رسمت لك ما طلبت يا زعيم، هل ترغب في تعديل أي تفاصيل؟"
            else:
                resp = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": sys_msg}] + st.session_state.history[-15:],
                    temperature=0.7
                )
                ans = resp.choices[0].message.content
            
            st.markdown(ans)
            st.session_state.history.append({"role": "assistant", "content": ans})
