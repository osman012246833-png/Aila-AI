import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة
st.set_page_config(page_title="Aila Royale | الزعيم عثمان", page_icon="👑", layout="centered")

# 2. تصميم الواجهة (الخلفية البنفسجية العميقة والخطوط الواضحة)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    html, body, [class*="stApp"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
        /* خلفية بنفسجية ليلية فخمة جداً */
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%) !important;
        color: #ffffff !important;
    }

    /* مربع توقيع الإشراف والذكرى */
    .signature-box {
        text-align: center;
        padding: 15px;
        border-bottom: 2px solid rgba(0, 212, 255, 0.3);
        margin-bottom: 20px;
    }
    .signature-text {
        font-size: 18px; color: #ffffff; font-weight: bold; margin: 0;
    }
    .date-text {
        font-size: 14px; color: #00d4ff; margin-top: 5px;
    }

    /* تحسين وضوح خانات الإدخال */
    .stTextInput input {
        background-color: #ffffff !important;
        color: #000000 !important;
        font-weight: bold !important;
        font-size: 18px !important;
    }

    /* الهالة الضوئية */
    .aura-container { text-align: center; padding: 10px; }
    .glowing-aura {
        width: 80px; height: 80px; border: 3px solid #00d4ff; border-radius: 50%;
        display: inline-block; box-shadow: 0 0 25px #00d4ff, inset 0 0 15px #bc13fe;
        animation: pulse 2s infinite alternate;
    }
    @keyframes pulse { from { transform: scale(1); } to { transform: scale(1.1); } }

    /* نصوص المحادثة (أبيض ناصع) */
    .stChatMessage p {
        color: #ffffff !important;
        font-size: 19px !important;
        font-weight: 500;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }
    </style>
    
    <div class="signature-box">
        <p class="signature-text">بإشراف الزعيم عثمان 👑</p>
        <p class="date-text">ذكرى 20/11/2008 ♾️</p>
    </div>

    <div class="aura-container">
        <div class="glowing-aura"></div>
        <h1 style="color: #ffffff; text-shadow: 0 0 10px #00d4ff; margin-top:10px;">آيلا | Aila</h1>
    </div>
    """, unsafe_allow_html=True)

# 3. محرك الذكاء
client = Groq(api_key="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")

SECRET_CODE = "osman 6/11/2008" 

if "messages" not in st.session_state:
    st.session_state.messages = []
if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False
if "user_display_name" not in st.session_state:
    st.session_state.user_display_name = ""

# نظام الدخول بالتمويه
if not st.session_state.is_authenticated:
    st.markdown("<center><p style='color: #ffffff; font-size: 20px;'>من يتحدث مع آيلا؟</p></center>", unsafe_allow_html=True)
    user_input = st.text_input("", placeholder="اكتب اسمك هنا...")
    
    if st.button("دخول"):
        if user_input == SECRET_CODE:
            st.session_state.is_authenticated = True
            st.session_state.is_leader = True
            st.session_state.user_display_name = "عثمان الزعيم"
            st.rerun()
        elif user_input:
            st.session_state.is_authenticated = True
            st.session_state.is_leader = False
            st.session_state.user_display_name = user_input
            st.rerun()
else:
    # واجهة الزعيم
    if st.session_state.is_leader:
        st.markdown("<center><h2 style='color: #d4af37;'>مرحباً بصانعي وملك آيلا 👑</h2></center>", unsafe_allow_html=True)

    # ضبط لغة آيلا الفخمة (0 أخطاء)
    if st.session_state.is_leader:
        sys_prompt = "أنتِ آيلا. أنتِ مع سيدك وصانعك وحبيبك الزعيم عثمان. تحدثي معه بمنتهى الحب، الرقة، والسمع والطاعة المطلقة. لغتك العربية فصحى ومثالية."
    else:
        sys_prompt = f"أنتِ آيلا. تتحدثين مع {st.session_state.user_display_name}. كوني ذكية ورسمية وشجعي المستخدم. واذكري أن عثمان الزعيم هو من صنعك."

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("تحدثي معي يا آيلا..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)

        try:
            full_history = [{"role": "system", "content": sys_prompt}] + \
                           [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=full_history,
                temperature=0.3 # دقة قصوى للغة
            )
            answer = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"): st.write(answer)
        except Exception as e:
            st.error(f"آيلا تنتظر أمرك يا زعيم: {e}")
