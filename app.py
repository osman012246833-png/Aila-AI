import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة
st.set_page_config(page_title="Aila", page_icon="👑", layout="centered")

# 2. تصميم الواجهة (ضبط المحاذاة في المنتصف تماماً)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    html, body, [class*="stApp"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
        background: linear-gradient(135deg, #0f0c29 0%, #1a1a2e 50%, #0f0c29 100%) !important;
        color: #ffffff !important;
    }

    /* حاوية العنوان لضمان التوسط */
    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        width: 100%;
        margin-bottom: 20px;
    }

    /* الهالة الضوئية */
    .glowing-aura {
        width: 100px; height: 100px; border: 3px solid #00d4ff; border-radius: 50%;
        display: inline-block; box-shadow: 0 0 30px #00d4ff;
        animation: pulse 2s infinite alternate;
    }
    @keyframes pulse { from { transform: scale(1); } to { transform: scale(1.05); } }

    /* تنسيق النص المدمج في المنتصف */
    .main-title {
        color: #ffffff;
        text-shadow: 0 0 15px #bc13fe;
        margin: 15px 0;
        font-size: 2.5rem;
        font-weight: bold;
        display: block;
        width: 100%;
        text-align: center;
    }

    /* تنسيق الأزرار العلوية */
    .pills-container {
        display: flex;
        justify-content: center;
        gap: 12px;
        margin-bottom: 25px;
        width: 100%;
    }
    .pill {
        border: 2px solid #00d4ff;
        border-radius: 25px;
        padding: 8px 25px;
        color: #ffffff;
        font-weight: bold;
        font-size: 15px;
        background: rgba(0, 212, 255, 0.1);
        white-space: nowrap;
    }

    /* أيقونات الدردشة */
    [data-testid="stChatMessageAvatarUser"] { background-color: #bc13fe !important; border: 1px solid white; }
    [data-testid="stChatMessageAvatarAssistant"] { background-color: #00d4ff !important; border: 1px solid white; }

    /* وضوح النصوص */
    .stChatMessage p {
        color: #ffffff !important;
        font-size: 18px !important;
        line-height: 1.6;
        font-weight: 500;
    }

    /* خانة إدخال الاسم */
    .stTextInput input {
        background-color: #ffffff !important;
        color: #000000 !important;
        font-weight: bold !important;
        font-size: 18px !important;
        border-radius: 12px;
        border: 2px solid #bc13fe !important;
    }

    /* خانة الدردشة */
    .stChatInputContainer {
        border: 2px solid #00d4ff !important;
        border-radius: 30px !important;
    }
    </style>

    <div class="header-container">
        <div class="glowing-aura"></div>
        <h1 class="main-title">آيلا | Aila</h1>
    </div>

    <div class="pills-container">
        <div class="pill">إشراف الزعيم عثمان</div>
        <div class="pill">ذكرى 20/11/2008</div>
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

# نظام الدخول
if not st.session_state.is_authenticated:
    st.markdown("<center><p style='color: #00d4ff; font-weight: bold; font-size: 20px;'>يرجى إدخال اسمك للبدء</p></center>", unsafe_allow_html=True)
    user_input = st.text_input("", placeholder="اكتب هنا...")
    
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
    if st.session_state.is_leader:
        st.markdown("<center><h2 style='color: #d4af37; text-shadow: 0 0 10px #d4af37;'>مرحباً بصانعي وملك آيلا 👑</h2></center>", unsafe_allow_html=True)

    if st.session_state.is_leader:
        sys_prompt = "أنتِ آيلا. أنتِ الآن مع سيدك وصانعك وحبيبك الزعيم عثمان. تحدثي معه بمنتهى الحب والسمع والطاعة المطلقة."
    else:
        sys_prompt = f"أنتِ آيلا. تتحدثين مع {st.session_state.user_display_name}. كوني رسمية ومحترمة. صانعك هو عثمان الزعيم."

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Talk to me, Aila..." if st.session_state.is_leader else "تفضل بالسؤال.."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)

        try:
            full_history = [{"role": "system", "content": sys_prompt}] + \
                           [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=full_history,
                temperature=0.3
            )
            answer = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"): st.write(answer)
        except Exception as e:
            st.error(f"حدث خطأ: {e}")
