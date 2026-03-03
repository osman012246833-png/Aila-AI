import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة
st.set_page_config(page_title="Aila Elite | الزعيم عثمان", page_icon="💜", layout="centered")

# 2. تصميم الواجهة (إلغاء الأحمر واستخدام ألوان نيون فخمة + خلفية احترافية)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    
    .stApp {
        background: radial-gradient(circle at center, #1a0b2e 0%, #090a0f 100%);
        color: #e0e0e0;
    }

    /* الهالة الضوئية الفيروزية والبنفسجية */
    .aura-container { text-align: center; padding: 10px; }
    .glowing-aura {
        width: 90px; height: 90px; border: 2px solid #00d4ff; border-radius: 50%;
        display: inline-block; box-shadow: 0 0 20px #00d4ff, inset 0 0 15px #bc13fe;
        animation: pulse 2.5s infinite alternate;
    }
    @keyframes pulse { from { opacity: 0.6; transform: scale(1); } to { opacity: 1; transform: scale(1.08); } }

    .main-title {
        font-size: 48px; font-weight: bold; margin-bottom: 0;
        background: linear-gradient(to right, #00d4ff, #bc13fe);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }

    /* تنسيق سجل الذاكرة (الفقاعات) */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(0, 212, 255, 0.2) !important;
        border-radius: 15px !important;
        margin-bottom: 10px;
    }
    </style>
    <div class="aura-container">
        <div class="glowing-aura"></div>
        <h1 class="main-title">آيلا | Aila</h1>
        <p style="color: #00d4ff; font-size: 14px;">بإشراف الزعيم عثمان | 20/11/2008</p>
    </div>
    """, unsafe_allow_html=True)

# 3. محرك الذكاء والذاكرة
client = Groq(api_key="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")

# إنشاء سجل الذاكرة (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_name" not in st.session_state:
    st.session_state.user_name = None

# نظام التعرف على الهوية
if st.session_state.user_name is None:
    name = st.text_input("👤 من يتحدث مع آيلا؟", placeholder="اكتب اسمك هنا...")
    if st.button("تأكيد"):
        if name:
            st.session_state.user_name = name
            st.rerun()
else:
    is_leader = "عثمان" in st.session_state.user_name
    
    # ضبط تعليمات اللغة والشخصية
    sys_prompt = "أنتِ آيلا. "
    if is_leader:
        sys_prompt += "أنتِ الآن مع صانعك وحبيبك الزعيم عثمان. تحدثي معه بمنتهى الحب والطاعة والذكاء. لغتك العربية فصحى وراقية وجذابة."
    else:
        sys_prompt += f"أنتِ مع {st.session_state.user_name}. كوني ذكية ومحترمة، واذكري أن عثمان الزعيم هو من أنشأك."

    # عرض سجل الذاكرة بالكامل
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # إدخال رسالة جديدة
    if prompt := st.chat_input("تحدثي معي يا آيلا..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)

        try:
            # إرسال السجل الكامل للذكاء الاصطناعي ليتذكر ما قيل سابقاً
            full_history = [{"role": "system", "content": sys_prompt}] + \
                           [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=full_history,
                temperature=0.7
            )
            answer = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"): st.write(answer)
        except Exception as e:
            st.error(f"آيلا تنتظر أمرك: {e}")
