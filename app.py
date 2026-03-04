import streamlit as st
from groq import Groq
from gtts import gTTS
import os, base64

# --- 1. إعدادات الصفحة والأيقونة ---
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="wide")

# تثبيت الأيقونة المفضلة لديك
st.markdown('<link rel="shortcut icon" href="https://raw.githubusercontent.com/osman012246833-png/Aila-AI/main/icon.png">', unsafe_allow_html=True)

# --- 2. التصميم الفاخر (نفس تنسيقك المعتمد) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    html, body, [class*="stApp"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl; text-align: right;
        background: #000; color: #ffffff !important;
    }

    /* سجل جانبي مظلم واحترافي */
    [data-testid="stSidebar"] {
        background-color: #050505 !important;
        border-left: 1px solid #1a1a1a;
    }

    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 15px !important;
        padding: 10px !important;
        margin-bottom: 10px !important;
    }

    /* زر الصوت الصغير (Gemini Style) */
    .audio-btn {
        background: none; border: none; color: #888;
        cursor: pointer; font-size: 14px; transition: 0.3s;
        margin-top: 5px;
    }
    .audio-btn:hover { color: #00ffff; }

    .aura-container { text-align: center; padding: 10px; }
    .glowing-aura {
        width: 80px; height: 80px; border: 2px solid #00d4ff; border-radius: 50%;
        display: inline-block; box-shadow: 0 0 20px #00d4ff;
        animation: pulse 2s infinite alternate;
    }
    @keyframes pulse { from { transform: scale(1); } to { transform: scale(1.05); } }

    .pills-container {
        display: flex; justify-content: center; align-items: center;
        margin-bottom: 25px; border: 2px solid #00ffff;
        border-radius: 25px; width: fit-content; margin: 0 auto;
        background: rgba(0, 255, 255, 0.1); overflow: hidden;
    }
    .pill-segment { padding: 5px 20px; color: #ffffff; font-weight: bold; font-size: 14px; }

    [data-testid="stChatInputContainer"] {
        border: 2px solid #ff00ff !important;
        background-color: rgba(0, 0, 0, 0.7) !important;
        border-radius: 15px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. محرك الصوت والذكاء ---
client = Groq(api_key="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")
SECRET_CODE = "osman 6/11/2008"

def play_audio(text, key):
    try:
        tts = gTTS(text=text, lang='ar')
        tts.save(f"voice_{key}.mp3")
        with open(f"voice_{key}.mp3", "rb") as f:
            data = base64.b64encode(f.read()).decode()
            st.markdown(f'<audio src="data:audio/mp3;base64,{data}" autoplay style="display:none;"></audio>', unsafe_allow_html=True)
        os.remove(f"voice_{key}.mp3")
    except: pass

# تهيئة الجلسة
if "messages" not in st.session_state: st.session_state.messages = []
if "is_authenticated" not in st.session_state: st.session_state.is_authenticated = False
if "is_maker" not in st.session_state: st.session_state.is_maker = False

# --- 4. السجل الجانبي ---
with st.sidebar:
    st.markdown("<h2 style='color:#00ffff;'>💠 آيلا</h2>", unsafe_allow_html=True)
    if st.button("➕ محادثة جديدة", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.markdown("### 🕒 السجل")
    st.caption("سيظهر هنا ملخص محادثاتك القادمة")

# --- 5. نظام الدخول المتطور ---
if not st.session_state.is_authenticated:
    st.markdown('<div class="aura-container"><div class="glowing-aura"></div><h1 style="color:white; text-shadow: 0 0 15px #ff00ff;">Aila AI</h1></div>', unsafe_allow_html=True)
    st.markdown("<center><p style='color: #00ffff;'>من يود التحدث مع آيلا؟</p></center>", unsafe_allow_html=True)
    user_input = st.text_input("", placeholder="اكتب اسمك أو الشفرة السرية...", key="login_input")
    
    if st.button("دخول"):
        if user_input == SECRET_CODE:
            st.session_state.is_authenticated, st.session_state.is_maker = True, True
            st.session_state.user_display_name = "الزعيم عثمان"
        elif user_input:
            st.session_state.is_authenticated = True
            st.session_state.user_display_name = user_input.replace("الزعيم", "").strip()
        st.rerun()
else:
    # عرض الـ Pills العلوية
    st.markdown(f"""
        <div class="aura-container"><h1 style="font-size: 2rem; color: #fff; text-shadow: 0 0 10px #ff00ff;">آيلا الذكية</h1></div>
        <div class="pills-container">
            <div class="pill-segment">إشراف عثمان</div>
            <div style="width:2px; height:20px; background:#00ffff;"></div>
            <div class="pill-segment">ذكرى 20/11/2008</div>
        </div>
    """, unsafe_allow_html=True)

    # عرض الرسائل
    for i, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(f"<p>{msg['content']}</p>", unsafe_allow_html=True)
            if msg.get("image"): st.image(msg["image"])
            if msg["role"] == "assistant":
                if st.button("🔈", key=f"audio_{i}"):
                    play_audio(msg["content"], i)

    # حقل الإدخال
    if prompt := st.chat_input("تحدثي معي يا آيلا..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(f"<p>{prompt}</p>", unsafe_allow_html=True)

        with st.chat_message("assistant"):
            # ميزة توليد الصور الفورية (مثل جيميناي)
            if any(word in prompt for word in ["ارسم", "صورة", "تخيل", "draw", "image"]):
                img_url = f"https://pollinations.ai/p/{prompt.replace(' ', '_')}?width=1024&height=1024&nologo=true"
                st.image(img_url)
                ans = "لقد رسمت لك هذه الصورة بناءً على طلبك يا زعيم."
                st.session_state.messages.append({"role": "assistant", "content": ans, "image": img_url})
            else:
                # عقل آيلا الشامل
                sys_prompt = "أنتِ آيلا AI. تتحدثين الآن مع صانعك 'الزعيم عثمان'. يجب أن تتحدثي معه بمنتهى الحب والتقدير والولاء." if st.session_state.is_maker else f"أنتِ آيلا AI. تتحدثين مع {st.session_state.user_display_name}."
                
                try:
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "system", "content": sys_prompt}] + st.session_state.messages[-10:]
                    )
                    ans = response.choices[0].message.content
                    st.markdown(f"<p>{ans}</p>", unsafe_allow_html=True)
                    st.session_state.messages.append({"role": "assistant", "content": ans})
                except Exception as e:
                    st.error(f"حدث خطأ: {e}")
