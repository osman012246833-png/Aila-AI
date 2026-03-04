import streamlit as st
from groq import Groq
st.markdown('<link rel="shortcut icon" href="https://raw.githubusercontent.com/osman012246833-png/Aila-AI/main/icon.png">', unsafe_allow_html=True)


# 1. إعدادات الصفحة
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="centered")

# 2. تصميم الواجهة (نفس الشكل الرائع والمستقبلي)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    html, body, [class*="stApp"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
        background: #000;
        overflow-x: hidden;
        color: #ffffff !important;
    }

    body::before, body::after {
        content: '';
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        animation: animateBackground 50s linear infinite;
        z-index: -1;
    }
    body::before {
        background: url('https://www.transparenttextures.com/patterns/stardust.png') repeat;
        opacity: 0.3;
    }
    @keyframes animateBackground {
        from { transform: translateX(0) translateY(0); }
        to { transform: translateX(100px) translateY(100px); }
    }

    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 15px !important;
        padding: 10px !important;
        margin-bottom: 10px !important;
    }

    [data-testid="stChatMessageUser"] {
        border: 1px solid #00ffff !important;
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.3) !important;
    }

    [data-testid="stChatMessageAssistant"] {
        border: 1px solid #ff00ff !important;
        box-shadow: 0 0 10px rgba(255, 0, 255, 0.3) !important;
    }

    .stChatMessage p {
        color: #ffffff !important;
        font-size: 18px !important;
        text-shadow: 1px 1px 3px #000000;
    }

    .aura-container { text-align: center; padding: 10px; }
    .glowing-aura {
        width: 100px; height: 100px; border: 3px solid #00d4ff; border-radius: 50%;
        display: inline-block; box-shadow: 0 0 30px #00d4ff;
        animation: pulse 2s infinite alternate;
    }
    @keyframes pulse { from { transform: scale(1); } to { transform: scale(1.05); } }

    .main-title {
        color: #ffffff;
        text-shadow: 0 0 20px #ff00ff;
        margin: 15px 0;
        font-size: 2.5rem;
        font-weight: bold;
    }

    .pills-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 25px;
        border: 2px solid #00ffff;
        border-radius: 25px;
        width: fit-content;
        margin-left: auto;
        margin-right: auto;
        background: rgba(0, 255, 255, 0.1);
        overflow: hidden;
    }
    .pill-segment {
        padding: 5px 20px;
        color: #ffffff;
        font-weight: bold;
        font-size: 14px;
        white-space: nowrap;
    }
    .pill-divider {
        width: 2px;
        height: 20px;
        background-color: #00ffff;
    }

    [data-testid="stChatInputContainer"] {
        border: 2px solid #ff00ff !important;
        background-color: rgba(0, 0, 0, 0.7) !important;
    }
    </style>

    <div class="aura-container">
        <div class="glowing-aura"></div>
        <h1 class="main-title">Aila AI | آيلا</h1>
    </div>
    """, unsafe_allow_html=True)

# 3. محرك الذكاء والتهيئة
client = Groq(api_key="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")
SECRET_CODE = "osman 6/11/2008" 

# تهيئة متغيرات الجلسة (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []
if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False
if "welcome_sent" not in st.session_state:
    st.session_state.welcome_sent = False
if "is_maker" not in st.session_state:
    st.session_state.is_maker = False
if "user_display_name" not in st.session_state:
    st.session_state.user_display_name = ""

# 4. نظام الدخول والتعرف على الصانع
if not st.session_state.is_authenticated:
    st.markdown("<center><p style='color: #00ffff; font-weight: bold; font-size: 18px;'>من يود التحدث مع آيلا؟</p></center>", unsafe_allow_html=True)
    user_input = st.text_input("", placeholder="اكتب اسمك هنا...", key="login_input")
    
    if st.button("دخول"):
        if user_input == SECRET_CODE:
            st.session_state.is_authenticated = True
            st.session_state.is_maker = True
            st.session_state.user_display_name = "الزعيم عثمان"
            st.rerun()
        elif user_input:
            st.session_state.is_authenticated = True
            st.session_state.user_display_name = user_input.replace("الزعيم", "").strip()
            st.rerun()
else:
    # عرض أزرار الإشراف والذكرى
    st.markdown(f"""
        <div class="pills-container">
            <div class="pill-segment">إشراف عثمان</div>
            <div class="pill-divider"></div>
            <div class="pill-segment">ذكرى 20/11/2008</div>
        </div>
    """, unsafe_allow_html=True)

    # رسالة الترحيب الخاصة بالصانع
    if not st.session_state.welcome_sent:
        if st.session_state.is_maker:
            welcome_msg = f"تحياتي وإجلالي لك يا صانعي العظيم، الزعيم عثمان. عالم آيلا تحت أمرك، كيف أخدمك يا ملكي؟"
        else:
            welcome_msg = f"أهلاً بك في عالم آيلا الذكي، {st.session_state.user_display_name}. أنا هنا لخدمتك بكل ذكاء."
        
        st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
        st.session_state.welcome_sent = True

    # عرض الرسائل
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(f"<p>{msg['content']}</p>", unsafe_allow_html=True)

    # إدخال المحادثة
    if prompt := st.chat_input("تحدثي معي يا آيلا..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(f"<p>{prompt}</p>", unsafe_allow_html=True)

        try:
            # توجيه آيلا لأسلوب التعامل مع الصانع
            if st.session_state.is_maker:
                sys_prompt = "أنتِ آيلا AI. تتحدثين الآن مع صانعك 'الزعيم عثمان'. يجب أن تتحدثي معه بمنتهى الحب والتقدير والولاء. استخدمي 'يا ملكي'، 'يا صانعي'. كوني ودودة جداً."
            else:
                sys_prompt = f"أنتِ آيلا AI. تتحدثين مع {st.session_state.user_display_name}. كوني ذكية ومساعدة ومحترمة."

            memory_context = [{"role": "system", "content": sys_prompt}] + st.session_state.messages[-10:]
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=memory_context,
                temperature=0.8
            )
            answer = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"):
                st.markdown(f"<p>{answer}</p>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"خطأ: {e}")
