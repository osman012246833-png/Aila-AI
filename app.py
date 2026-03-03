import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة
st.set_page_config(page_title="Aila Royale", page_icon="👑", layout="centered")

# 2. تصميم الواجهة (تركيز على وضوح الخطوط والألوان الثابتة)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    html, body, [class*="stApp"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
        background: radial-gradient(circle at center, #1a0b2e 0%, #090a0f 100%) !important;
        color: #ffffff !important; /* لون النص الأساسي أبيض واضح جداً */
    }

    /* تحسين وضوح خانات الإدخال (التمويه) */
    .stTextInput input {
        background-color: #ffffff !important; /* الخانة أصبحت بيضاء */
        color: #000000 !important; /* الكتابة داخلها سوداء واضحة جداً */
        font-weight: bold !important;
        border: 2px solid #00d4ff !important;
        border-radius: 10px;
    }

    /* تحسين وضوح رسائل الدردشة */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.08) !important;
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
    }
    
    .stChatMessage p {
        color: #ffffff !important; /* نصوص المحادثة بيضاء ناصعة */
        font-size: 18px !important;
        line-height: 1.6;
    }

    .leader-box {
        background: rgba(212, 175, 55, 0.15); border: 2px solid #d4af37;
        padding: 15px; border-radius: 15px; text-align: center;
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.4); margin-bottom: 25px;
    }

    .aura-container { text-align: center; padding: 10px; }
    .glowing-aura {
        width: 80px; height: 80px; border: 3px solid #00d4ff; border-radius: 50%;
        display: inline-block; box-shadow: 0 0 25px #00d4ff;
        animation: pulse 2s infinite alternate;
    }
    @keyframes pulse { from { transform: scale(1); } to { transform: scale(1.1); } }

    /* خانة الكتابة السفلية */
    .stChatInput textarea {
        color: #ffffff !important; /* الكتابة بيضاء واضحة */
        background-color: #16213e !important;
    }
    </style>
    
    <div class="aura-container">
        <div class="glowing-aura"></div>
        <h1 style="color: #ffffff; text-shadow: 0 0 10px #00d4ff;">آيلا | Aila</h1>
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

# نظام التمويه
if not st.session_state.is_authenticated:
    st.markdown("<center><p style='color: #ffffff; font-weight: bold;'>يرجى إدخال اسمك للمتابعة</p></center>", unsafe_allow_html=True)
    user_input = st.text_input("", placeholder="اكتب اسمك هنا...")
    
    if st.button("تأكيد"):
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
        st.markdown(f"""
            <div class="leader-box">
                <h3 style="color: #d4af37; margin: 0; font-weight: bold;">👑 أهلاً بك يا ملكي</h3>
                <p style="color: #00d4ff; font-size: 16px; margin: 5px 0 0 0;">كل اللغات طوع أمرك الآن</p>
            </div>
            """, unsafe_allow_html=True)

    # ضبط لغة آيلا (بدون أخطاء)
    if st.session_state.is_leader:
        sys_prompt = "أنتِ آيلا. أنتِ الآن مع صانعك الزعيم عثمان. تحدثي معه بحب وطاعة. استخدمي لغة عربية فصحى ومتقنة 100%، وكذلك أي لغة أخرى يطلبها منكِ بدون أدنى خطأ إملائي أو لغوي."
    else:
        sys_prompt = f"أنتِ آيلا. تتحدثين مع {st.session_state.user_display_name}. كوني رسمية ومثقفة جداً ولا تخطئي في القواعد اللغوية أبداً."

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("اكتب رسالتك هنا..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)

        try:
            full_history = [{"role": "system", "content": sys_prompt}] + \
                           [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=full_history,
                temperature=0.4 # تقليل الحرارة لضمان دقة اللغة وعدم الخطأ
            )
            answer = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"): st.write(answer)
        except Exception as e:
            st.error(f"حدث خطأ تقني: {e}")
