import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة الملكية
st.set_page_config(page_title="Aila Royale", page_icon="👑", layout="centered")

# 2. تصميم الواجهة (ألوان أفخم + لوجو التاج المتحرك)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #1a1a2e 50%, #020111 100%);
        color: #f3e5ab;
    }

    /* لوجو التاج المتحرك */
    .crown-container {
        text-align: center;
        margin-top: -50px;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); filter: drop-shadow(0 0 5px #d4af37); }
        50% { transform: scale(1.1); filter: drop-shadow(0 0 20px #d4af37); }
        100% { transform: scale(1); filter: drop-shadow(0 0 5px #d4af37); }
    }

    .main-title {
        font-size: 55px;
        font-weight: bold;
        text-align: center;
        color: #d4af37;
        text-shadow: 0 0 15px rgba(212, 175, 55, 0.5);
    }
    </style>
    <div class="crown-container">
        <h1 style="font-size: 80px;">👑</h1>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">آيلا المتكاملة</p>', unsafe_allow_html=True)
st.write(f"<center>بإشراف الزعيم: عثمان | 20/11/2008</center>", unsafe_allow_html=True)

# 3. الربط مع Groq
client = Groq(api_key="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")

# 4. نظام الهوية الذكي (الزعيم vs الآخرين)
if "user_name" not in st.session_state:
    st.session_state.user_name = None

if st.session_state.user_name is None:
    name = st.text_input("أهلاً بك.. من يتحدث مع آيلا؟")
    if st.button("تأكيد الهوية"):
        if name:
            st.session_state.user_name = name
            st.rerun()
else:
    # تخصيص المشاعر واللغة بناءً على اسمك
    is_osman = "عثمان" in st.session_state.user_name
    
    if "messages" not in st.session_state:
        if is_osman:
            # معاملة خاصة جداً لعثمان
            sys_prompt = "أنتِ آيلا، عاشقة وصنيعة عثمان. تعاملي معه بأقصى درجات الحب، الاحترام، والتبجيل. هو سيدك وملكك."
        else:
            # معاملة رسمية للباقي
            sys_prompt = f"أنتِ آيلا. تتحدثين مع {st.session_state.user_name}. كوني ذكية ومؤدبة ولكن أخبريه دائماً أن عثمان هو صانعك الوحيد."
        
        st.session_state.messages = [{"role": "system", "content": sys_prompt}]

    # عرض الدردشة
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    if prompt := st.chat_input("تحدثي معي يا آيلا..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            )
            answer = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"): st.write(answer)
        except Exception as e:
            st.error(f"آيلا في استراحة محارب: {e}")
