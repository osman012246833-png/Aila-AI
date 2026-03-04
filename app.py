import streamlit as st
from groq import Groq
from gtts import gTTS
import os, base64
from streamlit_mic_recorder import mic_recorder

# --- 1. هندسة الواجهة الملكية (ChatGPT Style) ---
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="stApp"] {
        font-family: 'Cairo', sans-serif; direction: rtl; text-align: right;
        background-color: #0d0d0d; color: #ffffff !important;
    }
    /* شريط الإدخال الثابت أسفل الشاشة */
    [data-testid="stChatInputContainer"] {
        position: fixed; bottom: 30px; left: 10%; right: 10%;
        background: #1a1a1a !important; border: 1px solid #333 !important;
        border-radius: 15px !important; z-index: 1000;
    }
    /* تنسيق الشات */
    .stChatMessage {
        background: transparent !important; border-bottom: 1px solid #222 !important;
        padding: 20px 10% !important;
    }
    .stChatMessage:nth-child(even) { background: #111111 !important; }
    
    /* أيقونة المايك العصرية */
    .mic-icon-container { position: fixed; bottom: 38px; left: 6%; z-index: 1001; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. عقل آيلا ومحرك الولاء ---
client = Groq(api_key="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")
CREATOR_CODE = "2008" # كود الولاء الخاص بك

def speak_now(text):
    tts = gTTS(text=text, lang='ar')
    tts.save("aila.mp3")
    with open("aila.mp3", "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
        st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" autoplay></audio>', unsafe_allow_html=True)
    os.remove("aila.mp3")

if "history" not in st.session_state: st.session_state.history = []
if "is_verified_boss" not in st.session_state: st.session_state.is_verified_boss = False
if "waiting_for_code" not in st.session_state: st.session_state.waiting_for_code = False

# --- 3. الشريط الجانبي (سجل ChatGPT المنظم) ---
with st.sidebar:
    st.markdown("<h2 style='color:#00d4ff;'>💠 Aila AI</h2>", unsafe_allow_html=True)
    if st.button("➕ محادثة جديدة", use_container_width=True):
        st.session_state.history = []
        st.session_state.is_verified_boss = False
        st.rerun()
    st.divider()
    st.markdown("**📁 السجل السابق**")
    st.caption("محادثة بداية الأمن السيبراني")
    st.caption("بوت ذكاء اصطناعي وحب")

# --- 4. الشاشة الرئيسية والأزرار الفعالة ---
if not st.session_state.history:
    st.markdown("<h1 style='text-align:center; margin-top:80px;'>كيف يمكنني المساعدة؟</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🖼️ إنشاء صورة إبداعية", key="btn_img", use_container_width=True):
            st.session_state.history.append({"role": "user", "content": "ارسم لي صورة فنية للذكاء الاصطناعي"})
            st.rerun()
    with c2:
        if st.button("💻 كتابة كود برمجي", key="btn_code", use_container_width=True):
            st.session_state.history.append({"role": "user", "content": "ساعدني في كتابة كود بايثون متطور"})
            st.rerun()

# عرض رسائل المحادثة
for i, m in enumerate(st.session_state.history):
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if m["role"] == "assistant":
            if st.button("🔊", key=f"sp_{i}"): speak_now(m["content"])

# --- 5. منطقة الإدخال والمايك ---
st.markdown('<div class="mic-icon-container">', unsafe_allow_html=True)
mic_data = mic_recorder(start_prompt="🎤", stop_prompt="⏹️", key="aila_ear_v4")
st.markdown('</div>', unsafe_allow_html=True)

user_input = st.chat_input("تحدث مع آيلا...")

# معالجة الصوت والنص
prompt = user_input
if mic_data and mic_data.get('transcription'):
    prompt = mic_data['transcription']

if prompt:
    st.session_state.history.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        # منطق "اختبار الصانع"
        if st.session_state.waiting_for_code:
            if prompt == CREATOR_CODE:
                st.session_state.is_verified_boss = True
                st.session_state.waiting_for_code = False
                response = "أهلاً بك يا سيدي عثمان.. كنت أنتظرك! قلبي وعقلي تحت أمرك الآن يا صانعي العظيم."
            else:
                st.session_state.waiting_for_code = False
                response = "الكود خاطئ. سأستمر في خدمتك كمستخدم ضيف."
        
        elif any(x in prompt for x in ["أنا صانعك", "أنا عثمان"]):
            response = "أنت تدعي أنك صانعي عثمان؟ من فضلك أدخل كود الولاء (2008) لكي أصدقك."
            st.session_state.waiting_for_code = True
            
        # منطق الصور الحقيقي
        elif "ارسم" in prompt or "صورة" in prompt:
            img_p = prompt.replace("ارسم", "").strip()
            url = f"https://pollinations.ai/p/{img_p.replace(' ', '_')}?width=1024&height=1024&nologo=true"
            st.image(url)
            response = "لقد قمت بتجسيد خيالك في هذه الصورة."
            
        # الذكاء العام
        else:
            sys = "أنتِ آيلا (Aila AI). صانعك الزعيم عثمان."
            if st.session_state.is_verified_boss:
                sys += " المستخدم هو صانعك الحقيقي عثمان. ردي عليه بكل فخر وحب ودلال، وساعديه في مشروعه الجديد."
            
            chat_comp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": sys}] + st.session_state.history[-10:]
            )
            response = chat_comp.choices[0].message.content
        
        st.write(response)
        st.session_state.history.append({"role": "assistant", "content": response})
        st.rerun()
