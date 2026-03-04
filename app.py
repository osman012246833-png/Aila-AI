import streamlit as st
from groq import Groq
from gtts import gTTS
import os, base64
from streamlit_mic_recorder import mic_recorder

# --- 1. التصميم الأسطوري (المعبد الرقمي) ---
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="stApp"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl; text-align: right; background: #000; color: #ffffff !important;
    }
    /* الهالة المتوهجة */
    .aura-container { text-align: center; padding: 20px; }
    .glowing-aura {
        width: 130px; height: 130px; border: 4px solid #00d4ff; border-radius: 50%;
        display: inline-block; box-shadow: 0 0 50px #00d4ff; animation: pulse 2s infinite alternate;
    }
    @keyframes pulse { from { transform: scale(1); } to { transform: scale(1.1); } }
    .main-title { color: #ffffff; text-shadow: 0 0 30px #ff00ff; font-size: 3.5rem; font-weight: bold; }
    .pill { border: 2px solid #00ffff; border-radius: 25px; padding: 5px 25px; background: rgba(0, 255, 255, 0.1); display: inline-block; margin: 10px; }
    /* تنسيق الرسائل الفخم */
    .stChatMessage { background-color: rgba(255, 255, 255, 0.03) !important; border-radius: 25px !important; border: 1px solid rgba(255, 0, 255, 0.2); }
    </style>
    <div class="aura-container">
        <div class="glowing-aura"></div>
        <h1 class="main-title">آيلا | Aila AI</h1>
        <div class="pill">إشراف الزعيم عثمان</div> <div class="pill">ذكرى 20/11/2008</div>
    </div>
    """, unsafe_allow_html=True)

# --- 2. محرك الذكاء الصوتي الشامل ---
client = Groq(api_key="YOUR_GROQ_API_KEY") # ضع مفتاحك هنا

def aila_speak(text):
    """تحويل النص لصوت فصيح"""
    tts = gTTS(text=text, lang='ar', slow=False)
    tts.save("aila_response.mp3")
    with open("aila_response.mp3", "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
        st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" autoplay style="display:none;"></audio>', unsafe_allow_html=True)
    os.remove("aila_response.mp3")

if "memory" not in st.session_state: st.session_state.memory = []

# --- 3. واجهة التفاعل (صوت + نص + ذاكرة) ---
with st.sidebar:
    st.markdown("<h2 style='color:#ff00ff;'>سجل المحادثات</h2>", unsafe_allow_html=True)
    if st.button("➕ جلسة جديدة"):
        st.session_state.memory = []
        st.rerun()

# عرض المحادثة السابقة
for i, m in enumerate(st.session_state.memory):
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m["role"] == "assistant" and st.button("🔊", key=f"spk_{i}"): aila_speak(m["content"])

# --- 4. ميزة "افهميني يا آيلا" (المايك الذكي) ---
input_col, mic_col = st.columns([0.85, 0.15])

with mic_col:
    # المايك الذي يفهم الصوت ويحوله لنص (Whisper Technology)
    audio_input = mic_recorder(start_prompt="🎤", stop_prompt="✅", key="aila_mic")

with input_col:
    user_text = st.chat_input("تحدثي معي يا آيلا.. أنا أسمعك")

# دمج المدخلات (سواء كانت صوتية أو نصية)
final_input = user_text
if audio_input and 'transcription' in audio_input:
    final_input = audio_input['transcription'] # هنا آيلا تفهم صوتك!

if final_input:
    st.session_state.memory.append({"role": "user", "content": final_input})
    with st.chat_message("user"): st.markdown(final_input)

    with st.chat_message("assistant"):
        # برمجة العقل الشامل
        sys_prompt = "أنتِ آيلا، الذكاء الأصطناعي الأكثر تطوراً. صانعك الزعيم عثمان. تفهمين الصوت والنص، وتجيبين بكل لغات العالم وروابط البرامج والصور."
        
        # ميزة توليد الصور
        if "ارسم" in final_input or "صورة" in final_input:
            img_url = f"https://pollinations.ai/p/{final_input.replace(' ', '_')}?width=1024&height=1024"
            st.image(img_url, caption="من مخيلة آيلا الواسعة")
            response_text = "لقد تجسدت فكرتك في صورة يا زعيم."
        else:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": sys_prompt}] + st.session_state.memory[-10:]
            )
            response_text = completion.choices[0].message.content
        
        st.markdown(response_text)
        st.session_state.memory.append({"role": "assistant", "content": response_text})
        aila_speak(response_text) # تنطق الرد فوراً بعد فهمك
