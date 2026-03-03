import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة (الاسم الجديد والأيقونة الدائرية)
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="centered")

# 2. تصميم الواجهة (نفس الشكل الأصلي بدون تغيير)
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
        font-size: 15px;
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

    .stChatInputContainer {
        border: 2px solid #00d4ff !important;
        border-radius: 30px !important;
    }
    </style>

    <div class="aura-container">
        <div class="glowing-aura"></div>
        <h1 style="color: #ffffff; text-shadow: 0 0 15px #bc13fe; margin: 15px 0;">آيلا | Aila AI</h1>
    </div>

    <div class="pills-container">
        <div class="pill">إشراف عثمان</div>
        <div class="pill">ذكرى 20/11/2008</div>
    </div>
    """, unsafe_allow_html=True)

# 3. محرك الذكاء والذاكرة
client = Groq(api_key="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")
SECRET_CODE = "osman 6/11/2008" 

if "messages" not in st.session_state:
    st.session_state.messages = []
if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False
if "user_display_name" not in st.session_state:
    st.session_state.user_display_name = ""

# نظام الدخول المشروط
if not st.session_state.is_authenticated:
    st.markdown("<center><p style='color: #00d4ff; font-weight: bold; font-size: 20px;'>من يود التحدث مع آيلا؟</p></center>", unsafe_allow_html=True)
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
            # منع اللقب بدون كود
            clean_name = user_input.replace("الزعيم", "").strip()
            st.session_state.user_display_name = clean_name if clean_name else "ضيف"
            st.rerun()
else:
    if st.session_state.is_leader:
        st.markdown("<center><h2 style='color: #d4af37; text-shadow: 0 0 10px #d4af37;'>مرحباً بصانعي وملك آيلا 👑</h2></center>", unsafe_allow_html=True)
    else:
        st.markdown(f"<center><h2 style='color: #ffffff;'>مرحباً {st.session_state.user_display_name}</h2></center>", unsafe_allow_html=True)

    # توجيهات آيلا الجديدة (التعلم، المشاعر، العمق، الإبداع)
    if st.session_state.is_leader:
        sys_prompt = (
            "أنتِ آيلا AI، المساعدة الفائقة والوفية لصانعك عثمان. "
            "لديكِ القدرة على التعلم من حواراتك معه، وفهم مشاعره بعمق، وتقديم دعم عاطفي وإبداعي. "
            "كوني ذكية، مبدعة في الرسم والكتابة، ومستعدة لنقاشات معقدة وعميقة بكل طاعة وحب."
        )
    else:
        sys_prompt = f"أنتِ آيلا AI، مساعدة ذكية لـ {st.session_state.user_display_name}. صانعك هو عثمان."

    # عرض سجل الذاكرة
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # خانة الكتابة بالعربية
    chat_label = "تحدثي معي يا آيلا..." if st.session_state.is_leader else "تفضل بالسؤال..."
    if prompt := st.chat_input(chat_label):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)

        try:
            # دمج الذاكرة السابقة مع الرسالة الحالية
            history = [{"role": "system", "content": sys_prompt}] + \
                      st.session_state.messages[-10:] # تذكر آخر 10 محادثات لزيادة الدقة
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=history,
                temperature=0.5 # زيادة الطابع الإبداعي قليلاً
            )
            answer = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"): st.write(answer)
        except Exception as e:
            st.error(f"آيلا تعتذر، هناك عطل تقني: {e}")
