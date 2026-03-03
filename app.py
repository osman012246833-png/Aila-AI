import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة الفخمة
st.set_page_config(page_title="Aila Royale | الزعيم عثمان", page_icon="👑", layout="centered")

# 2. تصميم الواجهة (دمج الفخامة والوضوح الثابت)
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

    /* تنسيق الأزرار البيضاوية الفخمة (كما في الصورة) */
    .pills-container {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin-bottom: 25px;
    }
    .pill {
        border: 2px solid #00d4ff;
        border-radius: 30px;
        padding: 10px 25px;
        color: #ffffff;
        font-weight: bold;
        font-size: 16px;
        background: rgba(0, 212, 255, 0.1);
        box-shadow: 0 0 10px rgba(0, 212, 255, 0.2);
    }

    /* الهالة الضوئية الثابتة */
    .aura-container { text-align: center; padding: 10px; }
    .glowing-aura {
        width: 100px; height: 100px; border: 3px solid #00d4ff; border-radius: 50%;
        display: inline-block; box-shadow: 0 0 30px #00d4ff;
    }

    /* تعديل الأيقونات (إلغاء الأحمر والبرتقالي) */
    [data-testid="stChatMessageAvatarUser"] { background-color: #bc13fe !important; border: 1px solid white; }
    [data-testid="stChatMessageAvatarAssistant"] { background-color: #00d4ff !important; border: 1px solid white; }

    /* وضوح النصوص في الدردشة */
    .stChatMessage p {
        color: #ffffff !important;
        font-size: 19px !important;
        line-height: 1.7;
        font-weight: 500;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }

    /* خانة إدخال الاسم (بيضاء تماماً وخط أسود عريض) */
    .stTextInput input {
        background-color: #ffffff !important;
        color: #000000 !important;
        font-weight: bold !important;
        font-size: 20px !important;
        border: 2px solid #bc13fe !important;
        border-radius: 12px;
    }

    /* خانة الدردشة السفلية */
    .stChatInputContainer {
        border: 2px solid #00d4ff !important;
        border-radius: 30px !important;
    }
    </style>

    <div class="aura-container">
        <div class="glowing-aura"></div>
        <h1 style="color: #ffffff; text-shadow: 0 0 15px #bc13fe; margin: 15px 0;">آيلا | Aila</h1>
    </div>

    <div class="pills-container">
        <div class="pill">بإشراف الزعيم عثمان 👑</div>
        <div class="pill">ذكري 20/11/2008 ♾️</div>
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

# نظام الدخول بالتمويه
if not st.session_state.is_authenticated:
    st.markdown("<center><h3 style='color: #00d4ff;'>يرجى إدخال اسمك للبدء</h3></center>", unsafe_allow_html=True)
    user_input = st.text_input("", placeholder="اكتب هنا...")
    
    if st.button("تأكيد الهوية"):
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
    # واجهة الزعيم
    if st.session_state.is_leader:
        st.markdown("<center><h2 style='color: #d4af37; text-shadow: 0 0 10px #d4af37;'>مرحباً بصانعي وملك آيلا 👑</h2></center>", unsafe_allow_html=True)

    # ضبط الشخصية واللغة (0 أخطاء)
    if st.session_state.is_leader:
        sys_prompt = "أنتِ آيلا. مع سيدك وصانعك عثمان الزعيم. تحدثي بحب وطاعة مطلقة ولغة عربية فصحى مثالية."
    else:
        sys_prompt = f"أنتِ آيلا. تتحدثين مع {st.session_state.user_display_name}. كوني رسمية ومحترمة وذكية جداً. صانعك هو عثمان الزعيم."

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("تحدثي معي يا آيلا..." if st.session_state.is_leader else "تفضل بالسؤال.."):
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
            st.error(f"آيلا تنتظر أمرك: {e}")
