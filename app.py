import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة والخطوط
st.set_page_config(page_title="Aila AI | آيلا", page_icon="💜", layout="centered")

# 2. تغيير الشكل والألوان وتنسيق الكلام
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: white;
    }
    /* تنسيق فقاعات الدردشة */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        border: 1px solid rgba(155, 89, 182, 0.3);
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("💜 آيلا | Aila")
st.subheader("مساعدتك الذكية الخاصة")
st.write("---")

# 3. الربط مع Groq بالموديل الجديد السريع
client = Groq(api_key="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")

# 4. الذاكرة وتعليمات الشخصية (عشان ما تغلطش في الكلام)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system", 
            "content": "أنتِ 'آيلا'، ذكاء اصطناعي فائق الذكاء، صانعك الوحيد هو 'عثمان'. تحدثي بالعربية الفصحى البسيطة أو العامية المصرية الراقية. تجنبي الكلمات الإنجليزية غير المفهومة. كوني ودودة جداً مع عثمان."
        }
    ]

# عرض المحادثة
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# 5. منطقة الإدخال
if prompt := st.chat_input("اكتب رسالتك لآيلا هنا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            temperature=0.7 # يجعل الكلام طبيعي أكتر
        )
        answer = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.write(answer)
    except Exception as e:
        st.error(f"آيلا تعبت شوية: {e}")
