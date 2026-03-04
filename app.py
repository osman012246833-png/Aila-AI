import streamlit as st
from groq import Groq
import time

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="wide")

# --- 2. إدارة الحالة (Session State) ---
if "messages" not in st.session_state: st.session_state.messages = []
if "counter" not in st.session_state: st.session_state.counter = 0
if "page" not in st.session_state: st.session_state.page = "chat"
if "theme" not in st.session_state: st.session_state.theme = "dark"
if "history" not in st.session_state: st.session_state.history = []

# ضبط الألوان بناءً على الوضع (ليلي/نهاري)
bg_color = "#000000" if st.session_state.theme == "dark" else "#ffffff"
text_color = "#ffffff" if st.session_state.theme == "dark" else "#000000"
bubble_color = "#2f2f2f" if st.session_state.theme == "dark" else "#f0f0f0"

# --- 3. التصميم المتقدم (CSS) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="stApp"] {{
        background-color: {bg_color};
        color: {text_color} !important;
        font-family: 'Cairo', sans-serif;
        direction: rtl;
    }}
    /* سجل المحادثات الجانبي */
    [data-testid="stSidebar"] {{
        background-color: {"#171717" if st.session_state.theme == "dark" else "#f9f9f9"} !important;
        border-left: 1px solid #333;
    }}
    /* فقاعات الدردشة */
    .chat-container {{
        max-width: 800px;
        margin: auto;
    }}
    .user-msg {{
        background-color: {bubble_color};
        padding: 12px 20px;
        border-radius: 20px;
        margin: 10px 0;
        display: inline-block;
        float: left;
        clear: both;
        font-size: 18px;
    }}
    .ai-msg {{
        padding: 12px 0;
        margin: 10px 0;
        display: block;
        clear: both;
        font-size: 19px;
        line-height: 1.6;
    }}
    /* السبحة */
    .tasbih-circle {{
        width: 220px; height: 220px;
        border-radius: 50%;
        border: 5px solid #00ffff;
        display: flex; align-items: center; justify-content: center;
        margin: 30px auto;
        font-size: 50px; font-weight: bold;
        box-shadow: 0 0 20px #00ffff55;
        background: radial-gradient(circle, #1a1a1a, #000);
    }}
    /* زر الإدخال */
    div[data-testid="stChatInput"] {{
        max-width: 800px !important;
        margin: auto !important;
    }}
    </style>
    """, unsafe_allow_html=True)

client = Groq(api_key="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")

# --- 4. الوظائف ---
def switch_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"

def start_new_chat():
    if st.session_state.messages:
        summary = st.session_state.messages[0]["content"][:30]
        st.session_state.history.append({"title": summary, "msgs": st.session_state.messages.copy()})
    st.session_state.messages = []

# --- 5. القائمة الجانبية (نفس ChatGPT) ---
with st.sidebar:
    st.title("💠 آيلا AI")
    if st.button("➕ محادثة جديدة", use_container_width=True):
        start_new_chat()
        st.rerun()
    
    st.write("---")
    st.subheader("🕒 سجل المحادثات")
    for idx, chat in enumerate(reversed(st.session_state.history)):
        if st.button(f"💬 {chat['title']}...", key=f"hist_{idx}"):
            st.session_state.messages = chat['msgs']
            st.rerun()
    
    st.write("---")
    if st.button("📿 ركن التسبيح"):
        st.session_state.page = "tasbih"
        st.rerun()
    
    label = "🌙 الوضع الليلي" if st.session_state.theme == "light" else "☀️ الوضع النهاري"
    st.button(label, on_click=switch_theme)

# --- 6. عرض الصفحات ---
if st.session_state.page == "tasbih":
    st.markdown("<h1 style='text-align:center;'>📿 السبحة الإلكترونية</h1>", unsafe_allow_html=True)
    st.markdown(f'<div class="tasbih-circle">{st.session_state.counter}</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ سبّح", use_container_width=True):
            st.session_state.counter += 1
            st.rerun()
    with col2:
        if st.button("🔄 تصفير", use_container_width=True):
            st.session_state.counter = 0
            st.rerun()
            
    if st.button("⬅️ العودة للدردشة"):
        st.session_state.page = "chat"
        st.rerun()

else:
    # واجهة الدردشة
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-msg">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="ai-msg"><b>آيلا:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)

    if prompt := st.chat_input("كيف يمكنني مساعدتك يا زعيم؟"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

    # الرد الذكي
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.markdown('<div class="ai-msg"><b>آيلا:</b><br></div>', unsafe_allow_html=True):
            placeholder = st.empty()
            full_res = ""
            sys_prompt = "أنتِ آيلا، مساعدة ذكية وصديقة للصانع الزعيم عثمان. خبيرة في الدين الإسلامي والتقنية."
            
            try:
                stream = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": sys_prompt}] + st.session_state.messages,
                    stream=True
                )
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        full_res += chunk.choices[0].delta.content
                        placeholder.markdown(full_res + "▌")
                placeholder.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})
            except:
                st.error("حدث خطأ في الاتصال.")
    st.markdown('</div>', unsafe_allow_html=True)
