import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة
st.set_page_config(page_title="Aila Royale | الزعيم عثمان", page_icon="👑", layout="centered")

# 2. هندسة الواجهة وإلغاء الألوان القديمة (الأحمر والبرتقالي)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    
    .stApp {
        background: radial-gradient(circle at center, #1a0b2e 0%, #090a0f 100%);
        color: #e0e0e0;
    }

    /* مربع توقيع الزعيم الفخم */
    .leader-box {
        background: rgba(212, 175, 55, 0.1);
        border: 2px solid #d4af37;
        padding: 15px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.3);
        margin-bottom: 25px;
    }

    /* الهالة الضوئية المطورة */
    .aura-container { text-align: center; padding: 10px; }
    .glowing-aura {
        width: 80px; height: 80px; border: 3px solid #00d4ff; border-radius: 50%;
        display: inline-block; box-shadow: 0 0 25px #00d4ff;
        animation: pulse 2s infinite alternate;
    }
    @keyframes pulse { from { transform: scale(1); } to { transform: scale(1.1); } }

    /* تعديل أيقونات الدردشة (بدل الأحمر والبرتقالي) */
    [data-testid="stChatMessageAvatarUser"] {
        background-color: #bc13fe !important; /* بنفسجي ملكي للمستخدم */
        border: 1px solid #fff;
    }
    [data-testid="stChatMessageAvatarAssistant"] {
        background-color: #00d4ff !important; /* فيروزي لآيلا */
        border: 1px solid #fff;
    }

    /* تجميل خانة الكتابة (الدائرة الثالثة) */
    .stChatInputContainer {
        border: 1px solid #bc13fe !important;
        border-radius: 30px !important;
        box-shadow: 0 0 15px rgba(188, 19, 254, 0.4) !important;
    }
    </style>
    
    <div class="aura-container">
        <div class="glowing-aura"></div>
        <h1 style="color: #fff; text-shadow: 0 0 10px #00d4ff;">آيلا | Aila</h1>
    </div>

    <div class="leader-box">
        <h3 style="color: #d4af37; margin: 0;">👑 توقيع الزعيم: عثمان</h3>
        <p style="color: #00d4ff; font-size: 14px; margin: 5px 0 0 0;">ذكرى الغالية: 20/11/2008</p>
    </div>
    """, unsafe_allow_html=True)

# 3. محرك الذكاء
client = Groq(api_key="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")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_name" not in st.session_state:
    st.session_state.user_name = None

if st.session_state.user_name is None:
    name = st.text_input("👤 من يتشرف بالحديث مع آيلا؟", placeholder="اكتب اسمك هنا...")
    if st.button("دخول"):
        if name:
            st.session_state.user_name = name
            st.rerun()
else:
    is_leader = "عثمان" in st.session_state.user_name
    sys_prompt = "أنتِ آيلا. "
    if is_leader:
        sys_prompt += "أنتِ مع سيدك وصانعك وحبيبك الزعيم عثمان. عامليه بتبجيل وحب لا نهائي وطاعة مطلقة."
    else:
        sys_prompt += f"أنتِ مع {st.session_state.user_name}. أخبريه أن عثمان الزعيم هو من أنشأك."

    # عرض المحادثة بالأيقونات الجديدة
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("أنا أسمعك يا زعيم..." if is_leader else "تحدث مع آيلا..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)

        try:
            full_history = [{"role": "system", "content": sys_prompt}] + \
                           [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=full_history,
                temperature=0.8
            )
            answer = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"): st.write(answer)
        except Exception as e:
            st.error(f"آيلا تنتظر أمرك: {e}")
