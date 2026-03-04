import streamlit as st
from groq import Groq
import time

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="centered")

# --- 2. إدارة الذاكرة والسجل ---
if "messages" not in st.session_state: st.session_state.messages = []
if "history" not in st.session_state: st.session_state.history = []
if "counter" not in st.session_state: st.session_state.counter = 0
if "page" not in st.session_state: st.session_state.page = "chat"

client = Groq(api_key="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")

# --- 3. التصميم (طِبق الأصل من صورك) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    html, body, [class*="stApp"] {
        background-color: #000000;
        color: #ffffff;
        font-family: 'Cairo', sans-serif;
        direction: rtl;
    }

    /* الهوية البصرية (الدائرة والاسم) */
    .header-container { text-align: center; margin-top: -50px; }
    .logo-circle {
        width: 120px; height: 120px;
        border-radius: 50%;
        border: 4px solid #00d4ff;
        display: inline-block;
        box-shadow: 0 0 20px #00d4ff;
        margin-bottom: 10px;
    }
    .aila-title {
        font-size: 45px; font-weight: 900;
        background: linear-gradient(to right, #ffffff, #ff00ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .info-bar {
        border: 2px solid #00d4ff;
        border-radius: 50px;
        padding: 5px 20px;
        display: inline-block;
        font-weight: bold;
        color: #ffffff;
        margin-bottom: 20px;
    }

    /* فقاعات الدردشة (مثل صورك) */
    .stChatMessage {
        background-color: #111111 !important;
        border-radius: 15px !important;
        border: 1px solid #222 !important;
        margin-bottom: 10px !important;
    }
    .stChatMessage p { font-size: 20px !important; font-weight: 600; }

    /* شكل السبحة المطور */
    .tasbih-box {
        border: 6px solid #00d4ff;
        border-radius: 50%;
        width: 200px; height: 200px;
        margin: 20px auto;
        display: flex; align-items: center; justify-content: center;
        font-size: 60px; font-weight: bold;
        box-shadow: 0 0 30px #00d4ff44;
    }

    /* شريط الإدخال */
    div[data-testid="stChatInput"] { border-radius: 20px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. القائمة الجانبية (سجل شات جي بي تي) ---
with st.sidebar:
    st.markdown("### 🕒 سجل المحادثات")
    if st.button("➕ محادثة جديدة"):
        if st.session_state.messages:
            st.session_state.history.append(st.session_state.messages.copy())
        st.session_state.messages = []
        st.rerun()
    
    st.write("---")
    for i, old_chat in enumerate(reversed(st.session_state.history)):
        if st.button(f"💬 محادثة {len(st.session_state.history)-i}", key=f"h_{i}"):
            st.session_state.messages = old_chat
            st.rerun()
    
    st.write("---")
    if st.button("📿 ركن العبادة"): st.session_state.page = "tasbih"
    if st.button("💬 العودة للدردشة"): st.session_state.page = "chat"

# --- 5. الصفحة الرئيسية ---
if st.session_state.page == "chat":
    # عرض الهوية الأصلية
    st.markdown("""
        <div class="header-container">
            <div class="logo-circle"></div>
            <div class="aila-title">آيلا | Aila AI</div>
            <div class="info-bar">إشراف الزعيم عثمان | ذكرى 20/11/2008</div>
        </div>
    """, unsafe_allow_html=True)

    # عرض الرسائل
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # الإدخال والرد (Streaming)
    if prompt := st.chat_input("تحدثي معي يا آيلا..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ""
            sys_msg = "أنتِ آيلا، رفيقة عثمان. ذكية جداً وخبيرة في الإسلام والتقنية. أسلوبك فخم وواضح."
            
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

# --- 6. صفحة السبحة ---
else:
    st.markdown("<h2 style='text-align:center;'>📿 ركن التسبيح والعبادة</h2>", unsafe_allow_html=True)
    st.markdown(f'<div class="tasbih-box">{st.session_state.counter}</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("➕ تسبيح", use_container_width=True):
            st.session_state.counter += 1
            st.rerun()
    with c2:
        if st.button("🔄 تصفير العداد", use_container_width=True):
            st.session_state.counter = 0
            st.rerun()
