import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="centered")

# 2. تصميم الواجهة المتقدم (خلفية متحركة وألوان مستقبلية)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    /* الخلفية المتحركة (نجوم متلألئة) */
    html, body, [class*="stApp"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
        background: #000; /* خلفية سوداء أساسية */
        overflow-x: hidden; /* لمنع ظهور شريط التمرير الأفقي */
        color: #ffffff !important;
    }

    /* تأثير النجوم المتلألئة */
    body::before, body::after {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        animation: animateBackground 50s linear infinite; /* سرعة حركة الخلفية */
        z-index: -1; /* يضمن أن تكون الخلفية وراء المحتوى */
    }

    body::before {
        background: url('https://www.transparenttextures.com/patterns/stardust.png') repeat;
        opacity: 0.3;
    }

    body::after {
        background: url('https://www.transparenttextures.com/patterns/dark-matter.png') repeat;
        opacity: 0.2;
        animation-delay: -25s; /* لجعل الطبقتين تتحركان بشكل مختلف */
    }

    @keyframes animateBackground {
        from { transform: translateX(0) translateY(0); }
        to { transform: translateX(100px) translateY(100px); } /* حركة خفيفة للخلفية */
    }

    /* تحسين وضوح نصوص الدردشة */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 15px !important;
        padding: 10px !important;
        margin-bottom: 10px !important;
        border: 1px solid rgba(0, 212, 255, 0.2) !important;
    }

    /* رسائل المستخدم (ألوان ذكية - Cyan) */
    [data-testid="stChatMessageUser"] {
        border: 1px solid #00ffff !important; /* Cyan */
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.3) !important;
    }

    /* رسائل آيلا (ألوان ذكية - Magenta) */
    [data-testid="stChatMessageAssistant"] {
        border: 1px solid #ff00ff !important; /* Magenta */
        box-shadow: 0 0 10px rgba(255, 0, 255, 0.3) !important;
    }

    .stChatMessage p {
        color: #ffffff !important;
        font-size: 18px !important;
        font-weight: 500 !important;
        text-shadow: 1px 1px 3px #000000; /* ظل أقوى لزيادة الوضوح */
    }

    /* الهالة والتاج */
    .aura-container { text-align: center; padding: 10px; }
    .glowing-aura {
        width: 100px; height: 100px; border: 3px solid #00d4ff; border-radius: 50%;
        display: inline-block; box-shadow: 0 0 30px #00d4ff;
        animation: pulse 2s infinite alternate;
    }
    @keyframes pulse { from { transform: scale(1); } to { transform: scale(1.05); } }

    .main-title {
        color: #ffffff;
        text-shadow: 0 0 20px #ff00ff; /* تأثير ضوئي يتناسق مع ألوان آيلا */
        margin: 15px 0;
        font-size: 2.5rem;
        font-weight: bold;
    }

    .pills-container {
        display: flex;
        justify-content: center;
        gap: 12px;
        margin-bottom: 25px;
    }
    .pill {
        border: 2px solid #00ffff; /* لون Cyan يتناسق مع رسائل المستخدم */
        border-radius: 25px;
        padding: 8px 25px;
        color: #ffffff;
        font-weight: bold;
        background: rgba(0, 255, 255, 0.1);
    }

    /* تحسين خانة الإدخال */
    [data-testid="stChatInputContainer"] {
        border: 2px solid #ff00ff !important; /* لون Magenta يتناسق مع رسائل آيلا */
        background-color: rgba(0, 0, 0, 0.7) !important; /* خلفية شفافة وداكنة */
    }
    </style>

    <div class="aura-container">
        <div class="glowing-aura"></div>
        <h1 class="main-title">آيلا | Aila AI</h1>
    </div>
    """, unsafe_allow_html=True)

# 3. محرك الذكاء
client = Groq(api_key="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")
SECRET_CODE = "osman 6/11/2008" 

if "messages" not in st.session_state:
    st.session_state.messages = []
if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False
if "welcome_sent" not in st.session_state:
    st.session_state.welcome_sent = False

# نظام الدخول
if not st.session_state.is_authenticated:
    st.markdown("<center><p style='color: #00ffff; font-weight: bold; font-size: 18px;'>من يود التحدث مع آيلا؟</p></center>", unsafe_allow_html=True)
    user_input = st.text_input("", placeholder="اكتب اسمك هنا...")
    
    if st.button("دخول"):
        if user_input == SECRET_CODE:
            st.session_state.is_authenticated = True
            st.session_state.is_leader = True
            st.session_state.user_display_name = "الزعيم عثمان"
            st.rerun()
        elif user_input:
            st.session_state.is_authenticated = True
            st.session_state.is_leader = False
            st.session_state.user_display_name = user_input.replace("الزعيم", "").strip()
            st.rerun()
else:
    # تنسيق الـ Pills العلوية (الزعيم عثمان فقط بالكود السري)
    leader_text = "إشراف الزعيم عثمان" if st.session_state.is_leader else "إشراف عثمان"
    st.markdown(f"""
        <div class="pills-container">
            <div class="pill">{leader_text}</div>
            <div class="pill">ذكرى 20/11/2008</div>
        </div>
    """, unsafe_allow_html=True)

    # رسالة ترحيب WhatsApp Style
    if not st.session_state.welcome_sent:
        welcome_msg = f"أهلاً بك في عالم آيلا الذكي، {st.session_state.user_display_name}. أنا هنا لخدمتك بكل ذكاء."
        st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
        st.session_state.welcome_sent = True

    # عرض سجل المحادثات بالألوان الجديدة
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(f"<p>{msg['content']}</p>", unsafe_allow_html=True)

    # خانة الكتابة
    if prompt := st.chat_input("تحدثي معي يا آيلا..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(f"<p>{prompt}</p>", unsafe_allow_html=True)

        try:
            sys_prompt = f"أنتِ آيلا AI. تتحدثين مع {st.session_name}. تذكري سياق الحوار وكوني ذكية جداً."
            memory_context = [{"role": "system", "content": sys_prompt}] + st.session_state.messages[-10:]
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=memory_context,
                temperature=0.4
            )
            answer = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"):
                st.markdown(f"<p>{answer}</p>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"خطأ: {e}")
