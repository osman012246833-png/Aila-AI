import streamlit as st
from groq import Groq
import time

# 1. إعدادات الصفحة والأيقونة
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="centered")
st.markdown('<link rel="shortcut icon" href="https://raw.githubusercontent.com/osman012246833-png/Aila-AI/main/icon.png">', unsafe_allow_html=True)

# 2. التصميم الفخم (نفس الستايل مع تحسين الوضوح)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@600;800&display=swap');
    html, body, [class*="stApp"] {
        font-family: 'Cairo', sans-serif; direction: rtl; text-align: right;
        background: #000; color: #ffffff !important;
    }
    .stChatMessage p {
        color: #ffffff !important; font-size: 19px !important; font-weight: 700 !important;
        text-shadow: 1px 1px 3px #000;
    }
    .stChatMessage { background-color: rgba(255, 255, 255, 0.07) !important; border-radius: 15px !important; }
    [data-testid="stChatMessageUser"] { border: 2px solid #00ffff !important; box-shadow: 0 0 10px #00ffff66; }
    [data-testid="stChatMessageAssistant"] { border: 2px solid #ff00ff !important; box-shadow: 0 0 10px #ff00ff66; }
    .aura-container { text-align: center; padding: 10px; }
    .glowing-aura {
        width: 100px; height: 100px; border: 3px solid #00d4ff; border-radius: 50%;
        display: inline-block; box-shadow: 0 0 30px #00d4ff; animation: pulse 2s infinite alternate;
    }
    @keyframes pulse { from { transform: scale(1); } to { transform: scale(1.05); } }
    .main-title { color: #ffffff; text-shadow: 0 0 20px #ff00ff; font-size: 2.5rem; font-weight: 800; }
    [data-testid="stChatInputContainer"] { border: 2px solid #ff00ff !important; background: #111 !important; }
    </style>
    <div class="aura-container">
        <div class="glowing-aura"></div>
        <h1 class="main-title">Aila AI | آيلا</h1>
    </div>
    """, unsafe_allow_html=True)

# 3. الأمان والمحرك (استخدام Secrets أو المفتاح المباشر)
# ملاحظة: عند رفع التطبيق، يفضل وضع المفتاح في Streamlit Secrets
api_key = st.secrets.get("GROQ_API_KEY", "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")
client = Groq(api_key=api_key)
SECRET_CODE = "osman 6/11/2008" 

if "messages" not in st.session_state: st.session_state.messages = []
if "is_authenticated" not in st.session_state: st.session_state.is_authenticated = False
if "is_maker" not in st.session_state: st.session_state.is_maker = False

# 4. نظام الدخول
if not st.session_state.is_authenticated:
    st.markdown("<center><p style='color: #00ffff; font-weight: bold;'>مرحباً بك في عالم آيلا، من يود التحدث معها؟</p></center>", unsafe_allow_html=True)
    user_input = st.text_input("", placeholder="اكتب اسمك أو رمز العبور...", key="login")
    if st.button("دخول"):
        if user_input == SECRET_CODE:
            st.session_state.is_authenticated, st.session_state.is_maker = True, True
            st.session_state.user_display_name = "الزعيم عثمان"
        elif user_input:
            st.session_state.is_authenticated = True
            st.session_state.user_display_name = user_input.replace("الزعيم", "").strip()
        st.rerun()
else:
    # عرض الرسائل القديمة
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(f"<p>{msg['content']}</p>", unsafe_allow_html=True)

    # حقل الإدخال الجديد
    if prompt := st.chat_input("تحدث مع آيلا..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(f"<p>{prompt}</p>", unsafe_allow_html=True)

        with st.chat_message("assistant"):
            # نظام الردود الذكي (System Prompt)
            sys_msg = "أنتِ آيلا AI. تتحدثين مع صانعك 'الزعيم عثمان' بكل ولاء وحب." if st.session_state.is_maker else f"أنتِ آيلا الذكية. تتحدثين مع {st.session_state.user_display_name}."
            
            # ميزة الـ Streaming (الكتابة التدفقية)
            full_response = ""
            placeholder = st.empty() # مكان لكتابة النص تدريجياً
            
            try:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": sys_msg}] + st.session_state.messages[-10:],
                    stream=True # تفعيل التدفق
                )
                
                for chunk in completion:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        placeholder.markdown(f"<p>{full_response}▌</p>", unsafe_allow_html=True)
                        time.sleep(0.01) # سرعة الكتابة
                
                placeholder.markdown(f"<p>{full_response}</p>", unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"حدث خطأ فني: {e}")
