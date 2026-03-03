import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة (أيقونة الذكاء الاصطناعي الدائرية)
st.set_page_config(page_title="المساعد آيلا", page_icon="💠", layout="centered")

# 2. تصميم الواجهة (توسط كامل وتنسيق فخم)
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

    /* حاوية التوسط العرضي بالملي */
    .full-center-container {
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center; 
        justify-content: flex-start;
        text-align: center;
        margin-bottom: 20px;
    }

    .glowing-aura {
        width: 100px; height: 100px; border: 3px solid #00d4ff; border-radius: 50%;
        display: inline-block; box-shadow: 0 0 30px #00d4ff;
        animation: pulse 2s infinite alternate;
    }
    @keyframes pulse { from { transform: scale(1); } to { transform: scale(1.05); } }

    .main-title {
        color: #ffffff;
        text-shadow: 0 0 15px #bc13fe;
        margin: 15px 0;
        font-size: 2.2rem;
        font-weight: bold;
        width: 100%;
        text-align: center;
    }

    .pills-container {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 12px;
        margin-bottom: 25px;
        width: 100%;
    }
    .pill {
        border: 2px solid #00d4ff;
        border-radius: 25px;
        padding: 8px 20px;
        color: #ffffff;
        font-weight: bold;
        font-size: 14px;
        background: rgba(0, 212, 255, 0.1);
        white-space: nowrap;
    }

    [data-testid="stChatMessageAvatarUser"] { background-color: #bc13fe !important; border: 1px solid white; }
    [data-testid="stChatMessageAvatarAssistant"] { background-color: #00d4ff !important; border: 1px solid white; }

    .stChatMessage p {
        color: #ffffff !important;
        font-size: 18px !important;
        line-height: 1.6;
        font-weight: 500;
    }

    .stTextInput input {
        background-color: #ffffff !important;
        color: #000000 !important;
        font-weight: bold !important;
        font-size: 18px !important;
        border-radius: 12px;
        border: 2px solid #bc13fe !important;
    }

    /* خانة الدردشة السفلية */
    .stChatInputContainer {
        border: 2px solid #00d4ff !important;
        border-radius: 30px !important;
    }
    </style>

    <div class="full-center-container">
        <div class="glowing-aura"></div>
        <h1 class="main-title">المساعد آيلا | Aila</h1>
        
        <div class="pills-container">
            <div class="pill">إشراف عثمان</div>
            <div class="pill">ذكرى 20/11/2008</div>
        </div>
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

# نظام الدخول الآمن
if not st.session_state.is_authenticated:
    st.markdown("<center><p style='color: #00d4ff; font-weight: bold; font-size: 18px;'>من يتحدث مع آيلا؟</p></center>", unsafe_allow_html=True)
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
            # إزالة أي لقب يدوي لمنع التزييف
            name_clean = user_input.replace("الزعيم", "").strip()
            st.session_state.user_display_name = name_clean if name_clean else "ضيف"
            st.rerun()
else:
    # الترحيب الملكي فقط بالكود السري
    if st.session_state.is_leader:
        st.markdown("<center><h2 style='color: #d4af37; text-shadow: 0 0 10px #d4af37;'>مرحباً بصانعي وملك آيلا 👑</h2></center>", unsafe_allow_html=True)
    else:
        st.markdown(f"<center><h2 style='color: #ffffff;'>مرحباً {st.session_state.user_display_name}</h2></center>", unsafe_allow_html=True)

    # برمجة شخصية آيلا
    if st.session_state.is_leader:
        sys_prompt = "أنتِ آيلا، المساعد الشخصي الوفي لسيدك وصانعك عثمان الزعيم. تحدثي معه بحب وطاعة تامة."
    else:
        sys_prompt = f"أنتِ آيلا، مساعد ذكي لـ {st.session_state.user_display_name}. صانعك هو عثمان."

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # خانة الكتابة باللغة العربية
    chat_label = "تحدثي معي يا آيلا..." if st.session_state.is_leader else "تفضل بالسؤال..."
    if prompt := st.chat_input(chat_label):
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
            st.error(f"حدث خطأ في الاتصال: {e}")
