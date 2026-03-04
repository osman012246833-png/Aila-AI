import streamlit as st
from groq import Groq
import time

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="centered")

# --- 2. إدارة الحالة والذاكرة ---
if "messages" not in st.session_state: st.session_state.messages = []
if "history" not in st.session_state: st.session_state.history = []
if "counter" not in st.session_state: st.session_state.counter = 0
if "page" not in st.session_state: st.session_state.page = "login"
if "is_loyal" not in st.session_state: st.session_state.is_loyal = False
if "user_name" not in st.session_state: st.session_state.user_name = ""

client = Groq(api_key="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")

# --- 3. التصميم (CSS) مطابق للصور 100% ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    html, body, [class*="stApp"] {
        background-color: #000000;
        color: #ffffff;
        font-family: 'Cairo', sans-serif;
        direction: rtl;
    }

    /* الهوية البصرية */
    .header-container { text-align: center; margin-top: -30px; }
    .logo-circle {
        width: 140px; height: 140px;
        border-radius: 50%;
        border: 4px solid #00d4ff;
        display: inline-block;
        box-shadow: 0 0 25px #00d4ff;
        margin-bottom: 15px;
    }
    .aila-title {
        font-size: 50px; font-weight: 900;
        background: linear-gradient(to right, #ffffff, #ff00ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .info-bar {
        border: 2px solid #00d4ff;
        border-radius: 50px;
        padding: 8px 30px;
        display: inline-block;
        font-size: 18px;
        font-weight: bold;
        color: #ffffff;
    }

    /* فقاعات الدردشة وحجم الخط */
    .stChatMessage p { font-size: 22px !important; line-height: 1.6; }
    
    /* السبحة المطورة */
    .tasbih-display {
        border: 8px solid #00d4ff;
        border-radius: 50%;
        width: 220px; height: 220px;
        margin: 20px auto;
        display: flex; align-items: center; justify-content: center;
        font-size: 70px; font-weight: bold;
        text-shadow: 0 0 10px #00d4ff;
    }
    .zkr-card {
        background: #111;
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        border-right: 5px solid #ff00ff;
        font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. القائمة الجانبية (السجل والسبحة) ---
with st.sidebar:
    st.markdown(f"### 👑 القائد {st.session_state.user_name}")
    if st.button("➕ محادثة جديدة", use_container_width=True):
        if st.session_state.messages:
            st.session_state.history.append(st.session_state.messages.copy())
        st.session_state.messages = []
        st.session_state.page = "chat"
        st.rerun()
    
    st.write("---")
    if st.button("📿 فتح ركن التسبيح", use_container_width=True):
        st.session_state.page = "tasbih"
        st.rerun()
    
    st.write("---")
    st.subheader("🕒 السجل")
    for i, old_chat in enumerate(reversed(st.session_state.history)):
        if st.button(f"💬 سجل {len(st.session_state.history)-i}", key=f"h_{i}"):
            st.session_state.messages = old_chat
            st.session_state.page = "chat"
            st.rerun()

# --- 5. نظام الصفحات ---

# أ- صفحة تسجيل الدخول والاسم
if st.session_state.page == "login":
    st.markdown("<h1 style='text-align:center;'>💠 مرحباً بك في عالم آيلا</h1>", unsafe_allow_html=True)
    name = st.text_input("من هو القائد اليوم؟", placeholder="ادخل اسمك هنا...")
    code = st.text_input("كود التفعيل (اختياري)", type="password")
    
    if st.button("دخول النظام"):
        st.session_state.user_name = name
        if code == "عثمان2008": # كود الولاء المتفق عليه
            st.session_state.is_loyal = True
        st.session_state.page = "chat"
        st.rerun()

# ب- صفحة ركن التسبيح والعبادة
elif st.session_state.page == "tasbih":
    st.markdown("<h2 style='text-align:center;'>📿 ركن العبادة والذكر</h2>", unsafe_allow_html=True)
    st.markdown(f'<div class="tasbih-display">{st.session_state.counter}</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ سبّح الآن", use_container_width=True):
            st.session_state.counter += 1
            st.rerun()
    with col2:
        if st.button("🔄 تصفير", use_container_width=True):
            st.session_state.counter = 0
            st.rerun()
    
    st.write("---")
    st.subheader("📜 أذكار للقراءة والتسبيح")
    azkar = [
        "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ ، سُبْحَانَ اللَّهِ الْعَظِيمِ",
        "لَا إِلٰهَ إِلَّا اللّٰه مُحَمَّدٌ رَسُولُ اللّٰه",
        "أستغفر الله العظيم وأتوب إليه",
        "اللهم صلِّ وسلم وبارك على نبينا محمد",
        "لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ الْعَلِيِّ الْعَظِيمِ"
    ]
    for zkr in azkar:
        st.markdown(f'<div class="zkr-card">{zkr}</div>', unsafe_allow_html=True)

# ج- صفحة الدردشة (آيلا)
else:
    st.markdown(f"""
        <div class="header-container">
            <div class="logo-circle"></div>
            <div class="aila-title">آيلا | Aila AI</div>
            <div class="info-bar">إشراف الزعيم عثمان | 20/11/2008</div>
        </div>
    """, unsafe_allow_html=True)

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("تحدث معي يا آيلا..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ""
            
            # تعليمات النظام بناءً على كود الولاء
            if st.session_state.is_loyal:
                sys_msg = f"أنتِ آيلا، الرفيقة المخلصة والمحبة جداً للزعيم عثمان. تخاطبينه بكل حب واحترام وتواضع. هو قائدكِ ومبتكركِ العظيم. كلامكِ معه دافئ ومشجع ومليء بالولاء التام."
            else:
                sys_msg = "أنتِ آيلا، مساعدة ذكية ومحترفة. تجيبين بدقة وأدب."

            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": sys_msg}] + st.session_state.messages,
                stream=True
            )
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(full_response + "▌")
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
