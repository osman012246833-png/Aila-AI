import streamlit as st
from groq import Groq
from gtts import gTTS
import os, base64

# 1. إعدادات الصفحة والأيقونة (نفس طلبك تماماً)
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="wide")
st.markdown('<link rel="shortcut icon" href="https://raw.githubusercontent.com/osman012246833-png/Aila-AI/main/icon.png">', unsafe_allow_html=True)

# 2. تصميم الواجهة المستقبلية (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="stApp"] {
        font-family: 'Cairo', sans-serif; direction: rtl; text-align: right;
        background: #000; color: #ffffff !important;
    }
    /* تنسيق السجل الجانبي */
    [data-testid="stSidebar"] { background-color: #0a0a0a !important; border-left: 1px solid #1a1a1a; }
    
    /* زر الصوت الصغير مثل جيميناي */
    .stButton button {
        background: none; border: none; padding: 0; color: #888;
        font-size: 14px; transition: 0.3s;
    }
    .stButton button:hover { color: #00ffff; border: none; background: none; }

    .stChatMessage { background-color: rgba(255, 255, 255, 0.05) !important; border-radius: 15px !important; }
    [data-testid="stChatMessageUser"] { border: 1px solid #00ffff !important; }
    [data-testid="stChatMessageAssistant"] { border: 1px solid #ff00ff !important; }

    .aura-container { text-align: center; padding: 10px; }
    .glowing-aura {
        width: 80px; height: 80px; border: 2px solid #00d4ff; border-radius: 50%;
        display: inline-block; box-shadow: 0 0 20px #00d4ff;
        animation: pulse 2s infinite alternate;
    }
    @keyframes pulse { from { transform: scale(1); } to { transform: scale(1.05); } }
    </style>
    """, unsafe_allow_html=True)

# 3. محرك الذكاء والصوت
client = Groq(api_key="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")
SECRET_CODE = "osman 6/11/2008" 

if "messages" not in st.session_state: st.session_state.messages = []
if "is_authenticated" not in st.session_state: st.session_state.is_authenticated = False
if "is_maker" not in st.session_state: st.session_state.is_maker = False

def speak_text(text, key):
    tts = gTTS(text=text, lang='ar')
    tts.save(f"voice_{key}.mp3")
    with open(f"voice_{key}.mp3", "rb") as f:
        data = base64.b64encode(f.read()).decode()
        st.markdown(f'<audio src="data:audio/mp3;base64,{data}" autoplay style="display:none;"></audio>', unsafe_allow_html=True)
    os.remove(f"voice_{key}.mp3")

# 4. السجل الجانبي (Sidebar)
with st.sidebar:
    st.markdown("<h2 style='color:#00ffff;'>💠 آيلا</h2>", unsafe_allow_html=True)
    if st.button("➕ محادثة جديدة", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.markdown("### 🕒 سجل المحادثات")
    for i, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            st.caption(f"💬 {msg['content'][:25]}...")

# 5. نظام الدخول والتعرف على الزعيم عثمان
if not st.session_state.is_authenticated:
    st.markdown("""<div class="aura-container"><div class="glowing-aura"></div><h1 class="main-title">Aila AI | آيلا</h1></div>""", unsafe_allow_html=True)
    st.markdown("<center><p style='color: #00ffff;'>من يود التحدث مع آيلا؟</p></center>", unsafe_allow_html=True)
    user_input = st.text_input("", placeholder="اكتب اسمك أو الشفرة السرية...", key="login")
    if st.button("دخول"):
        if user_input == SECRET_CODE:
            st.session_state.is_authenticated, st.session_state.is_maker = True, True
            st.session_state.user_display_name = "الزعيم عثمان"
        elif user_input:
            st.session_state.is_authenticated = True
            st.session_state.user_display_name = user_input
        st.rerun()
else:
    # عرض الـ Pills العلوية
    st.markdown(f"""
        <div class="pills-container">
            <div class="pill-segment">إشراف عثمان</div>
            <div class="pill-divider"></div>
            <div class="pill-segment">ذكرى 20/11/2008</div>
        </div>
    """, unsafe_allow_html=True)

    # عرض الرسائل
    for i, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(f"<p>{msg['content']}</p>", unsafe_allow_html=True)
            if msg["role"] == "assistant":
                # زر الصوت الصغير تحت كل رد
                if st.button("🔈", key=f"voice_btn_{i}"):
                    speak_text(msg["content"], i)

    # حقل الإدخال
    if prompt := st.chat_input("تحدثي معي يا آيلا..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(f"<p>{prompt}</p>", unsafe_allow_html=True)

        with st.chat_message("assistant"):
            sys_prompt = "أنتِ آيلا AI. تتحدثين الآن مع صانعك 'الزعيم عثمان'. ردي عليه بكل حب وتقدير." if st.session_state.is_maker else f"أنتِ آيلا AI. تتحدثين مع {st.session_state.user_display_name}."
            
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": sys_prompt}] + st.session_state.messages[-10:],
                    temperature=0.8
                )
                answer = response.choices[0].message.content
                st.markdown(f"<p>{answer}</p>", unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": answer})
                st.rerun() # لإظهار زر الصوت فوراً
            except Exception as e:
                st.error(f"خطأ: {e}")
