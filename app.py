import streamlit as st
from groq import Groq

# إدراج الأيقونة
st.markdown('<link rel="shortcut icon" href="https://raw.githubusercontent.com/osman012246833-png/Aila-AI/main/icon.png">', unsafe_allow_html=True)

# 1. إعدادات الصفحة
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="centered")

# 2. تصميم الواجهة (توضيح الألوان والكتابة)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@600;800&display=swap');
    
    html, body, [class*="stApp"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
        background: #000;
        overflow-x: hidden;
        color: #ffffff !important;
    }

    /* توضيح نصوص الدردشة وجعلها بارزة جداً */
    .stChatMessage p {
        color: #ffffff !important;
        font-size: 20px !important; /* تكبير الخط */
        font-weight: 700 !important; /* جعل الخط عريضاً */
        text-shadow: 2px 2px 4px #000000; /* إضافة ظل لزيادة الوضوح */
    }

    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.08) !important;
        border-radius: 15px !important;
        padding: 12px !important;
    }

    [data-testid="stChatMessageUser"] {
        border: 2px solid #00ffff !important; /* توضيح لون الإطار */
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.4) !important;
    }

    [data-testid="stChatMessageAssistant"] {
        border: 2px solid #ff00ff !important; /* توضيح لون الإطار */
        box-shadow: 0 0 15px rgba(255, 0, 255, 0.4) !important;
    }

    .aura-container { text-align: center; padding: 10px; }
    .glowing-aura {
        width: 110px; height: 110px; border: 4px solid #00d4ff; border-radius: 50%;
        display: inline-block; box-shadow: 0 0 40px #00d4ff;
        animation: pulse 2s infinite alternate;
    }
    @keyframes pulse { from { transform: scale(1); } to { transform: scale(1.08); } }

    .main-title {
        color: #ffffff;
        text-shadow: 0 0 25px #ff00ff;
        margin: 15px 0;
        font-size: 2.8rem;
        font-weight: 800;
    }

    .pills-container {
        display: flex; justify-content: center; align-items: center;
        margin-bottom: 25px; border: 2.5px solid #00ffff;
        border-radius: 25px; width: fit-content; margin-left: auto; margin-right: auto;
        background: rgba(0, 255, 255, 0.15); overflow: hidden;
    }
    .pill-segment { padding: 8px 25px; color: #ffffff; font-weight: 800; font-size: 15px; }

    [data-testid="stChatInputContainer"] {
        border: 2.5px solid #ff00ff !important;
        background-color: rgba(0, 0, 0, 0.8) !important;
    }
    </style>

    <div class="aura-container">
        <div class="glowing-aura"></div>
        <h1 class="main-title">Aila AI | آيلا</h1>
    </div>
    """, unsafe_allow_html=True)

# 3. المحرك والتهيئة
client = Groq(api_key="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")
SECRET_CODE = "osman 6/11/2008" 

if "messages" not in st.session_state: st.session_state.messages = []
if "is_authenticated" not in st.session_state: st.session_state.is_authenticated = False
if "is_maker" not in st.session_state: st.session_state.is_maker = False

# 4. نظام الدخول (تصحيح لغوي كامل)
if not st.session_state.is_authenticated:
    st.markdown("<center><p style='color: #00ffff; font-weight: bold; font-size: 20px;'>مرحباً بك، من يود التحدث مع آيلا؟</p></center>", unsafe_allow_html=True)
    user_input = st.text_input("", placeholder="أدخل اسمك أو رمز العبور هنا...", key="login_input")
    
    if st.button("تسجيل الدخول"):
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
            <div style="width: 2px; height: 20px; background-color: #00ffff;"></div>
            <div class="pill-segment">ذكرى 2008/11/06</div>
        </div>
    """, unsafe_allow_html=True)

    # رسالة ترحيب منقحة لغوياً
    if "welcome_sent" not in st.session_state:
        if st.session_state.is_maker:
            welcome_msg = "تحياتي وإجلالي لك يا صانعي العظيم، الزعيم عثمان. عالم آيلا رهن إشارتك؛ كيف أخدمك اليوم يا ملكي؟"
        else:
            welcome_msg = f"أهلاً بك في عالم آيلا الذكي، {st.session_state.user_display_name}. أنا هنا لمساعدتك في كل ما تحتاج."
        st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
        st.session_state.welcome_sent = True

    # عرض الرسائل
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(f"<p>{msg['content']}</p>", unsafe_allow_html=True)

    # حقل الإدخال
    if prompt := st.chat_input("تحدث مع آيلا..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(f"<p>{prompt}</p>", unsafe_allow_html=True)

        try:
            # توجيه ذكاء آيلا لغوياً
            if st.session_state.is_maker:
                sys_prompt = "أنتِ آيلا AI. تتحدثين مع صانعك 'الزعيم عثمان'. يجب أن يكون أسلوبك مليئاً بالتقدير والولاء والمودة المطلقة. استخدمي 'يا ملكي' و'يا صانعي العظيم'."
            else:
                sys_prompt = f"أنتِ آيلا AI. تتحدثين مع {st.session_state.user_display_name}. كوني مساعدة، ذكية، ولبقة في الحديث."

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": sys_prompt}] + st.session_state.messages[-10:],
                temperature=0.7
            )
            answer = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"):
                st.markdown(f"<p>{answer}</p>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"عذراً يا زعيم، حدث خطأ: {e}")
