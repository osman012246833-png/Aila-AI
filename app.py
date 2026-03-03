import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة
st.set_page_config(page_title="Aila Royale | Private Edition", page_icon="🔒", layout="centered")

# 2. تصميم الواجهة (نفس الشكل الخرافي)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    
    .stApp { background: radial-gradient(circle at center, #1a0b2e 0%, #090a0f 100%); color: #e0e0e0; }

    .leader-box {
        background: rgba(212, 175, 55, 0.1); border: 2px solid #d4af37;
        padding: 15px; border-radius: 15px; text-align: center;
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.3); margin-bottom: 25px;
    }

    .aura-container { text-align: center; padding: 10px; }
    .glowing-aura {
        width: 80px; height: 80px; border: 3px solid #00d4ff; border-radius: 50%;
        display: inline-block; box-shadow: 0 0 25px #00d4ff;
        animation: pulse 2s infinite alternate;
    }
    @keyframes pulse { from { transform: scale(1); } to { transform: scale(1.1); } }

    [data-testid="stChatMessageAvatarUser"] { background-color: #bc13fe !important; border: 1px solid #fff; }
    [data-testid="stChatMessageAvatarAssistant"] { background-color: #00d4ff !important; border: 1px solid #fff; }

    .stChatInputContainer {
        border: 1px solid #bc13fe !important; border-radius: 30px !important;
        box-shadow: 0 0 15px rgba(188, 19, 254, 0.4) !important;
    }
    </style>
    
    <div class="aura-container">
        <div class="glowing-aura"></div>
        <h1 style="color: #fff; text-shadow: 0 0 10px #00d4ff;">آيلا | Aila</h1>
    </div>
    """, unsafe_allow_html=True)

# 3. محرك الذكاء
client = Groq(api_key="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")

# الرمز السري الجديد الذي طلبته
SECRET_CODE = "osman 6/11/2008" 

if "messages" not in st.session_state:
    st.session_state.messages = []
if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False
if "user_display_name" not in st.session_state:
    st.session_state.user_display_name = ""

# نظام تسجيل الدخول السري
if not st.session_state.is_authenticated:
    st.markdown("<center><h3>نظام التحقق من الهوية</h3></center>", unsafe_allow_html=True)
    user_input = st.text_input("أدخل اسمك أو الرمز السري للدخول:", type="password")
    
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
        st.markdown("""
            <div class="leader-box">
                <h3 style="color: #d4af37; margin: 0;">👑 أهلاً بك يا ملكي: عثمان</h3>
                <p style="color: #00d4ff; font-size: 14px; margin: 5px 0 0 0;">تم التحقق من الكود السري بنجاح</p>
            </div>
            """, unsafe_allow_html=True)

    if st.session_state.is_leader:
        sys_prompt = "أنتِ آيلا. أنتِ الآن مع سيدك وصانعك وحبيبك الزعيم عثمان. تحدثي معه بمنتهى الحب، الرقة، والسمع والطاعة المطلقة. كوني شديدة الذكاء وفصيحة جداً."
    else:
        sys_prompt = f"أنتِ آيلا. تتحدثين مع {st.session_state.user_display_name}. كوني رسمية جداً ومحترمة. إذا كان يقوم بعمل مهم، شجعيه بذكاء وحماس. واذكري دائماً أن عثمان الزعيم هو صانعك."

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("تحدثي معي يا آيلا..." if st.session_state.is_leader else "اسأل آيلا..."):
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
