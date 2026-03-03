import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="centered")

# 2. تصميم الواجهة (نفس الشكل مع الإضافات الجديدة)
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

    .aura-container { text-align: center; padding: 10px; }
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
        text-align: center;
    }

    .pills-container {
        display: flex;
        justify-content: center;
        gap: 12px;
        margin-bottom: 25px;
    }
    .pill {
        border: 2px solid #00d4ff;
        border-radius: 25px;
        padding: 8px 25px;
        color: #ffffff;
        font-weight: bold;
        background: rgba(0, 212, 255, 0.1);
    }

    /* تنسيق زر إدارة التطبيق المخصص */
    .manage-btn {
        display: inline-block;
        padding: 5px 15px;
        background-color: #1a1a2e;
        border: 1px solid #00d4ff;
        border-radius: 5px;
        color: #00d4ff;
        text-decoration: none;
        font-size: 12px;
        margin-top: 10px;
    }

    [data-testid="stChatInputContainer"] {
        border: 2px solid #00d4ff !important;
        border-radius: 30px !important;
    }
    </style>

    <div class="aura-container">
        <div class="glowing-aura"></div>
        <h1 class="main-title">آيلا | Aila AI</h1>
    </div>
    """, unsafe_allow_html=True)

# 3. محرك الذكاء والتحقق
client = Groq(api_key="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")
SECRET_CODE = "osman 6/11/2008" 

if "messages" not in st.session_state:
    st.session_state.messages = []
if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False

# نظام الدخول
if not st.session_state.is_authenticated:
    st.markdown("<center><p style='color: #00d4ff; font-weight: bold; font-size: 18px;'>من يود التحدث مع آيلا؟</p></center>", unsafe_allow_html=True)
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
    # تنسيق Pills العلوية بناءً على الهوية
    leader_text = "إشراف الزعيم عثمان" if st.session_state.is_leader else "إشراف عثمان"
    st.markdown(f"""
        <div class="pills-container">
            <div class="pill">{leader_text}</div>
            <div class="pill">ذكرى 20/11/2008</div>
        </div>
    """, unsafe_allow_html=True)

    # تغيير كلمة "مرحبا" إلى الترحيب الجديد الفخم
    st.markdown(f"<center><h2 style='color: #ffffff; text-shadow: 0 0 10px #bc13fe;'>أهلاً بك في عالم آيلا الذكي، {st.session_state.user_display_name}</h2></center>", unsafe_allow_html=True)

    # زر مخصص لـ Manage App في الواجهة
    col1, col2, col3 = st.columns([4, 2, 4])
    with col2:
        if st.button("⚙️ إدارة التطبيق"):
            st.info("هذا الزر مخصص للتحكم في إعدادات آيلا المتقدمة.")

    # برمجة الشخصية والذاكرة
    sys_prompt = f"أنتِ آيلا AI. تتحدثين مع {st.session_state.user_display_name}. تذكري سياق الحوار وكوني ذكية وعاطفية."

    # عرض سجل المحادثات (الذاكرة)
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # خانة الكتابة بالعربية
    if prompt := st.chat_input("تحدثي معي يا آيلا..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)

        try:
            # الاحتفاظ بآخر 10 رسائل فقط لضمان سرعة الأداء ودقة الذاكرة
            memory_context = [{"role": "system", "content": sys_prompt}] + st.session_state.messages[-10:]
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=memory_context,
                temperature=0.4
            )
            answer = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"): st.write(answer)
        except Exception as e:
            st.error(f"عذراً يا زعيم، هناك مشكلة: {e}")
