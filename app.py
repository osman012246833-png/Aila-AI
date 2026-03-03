import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة والخطوط
st.set_page_config(page_title="Aila AI | آيلا", page_icon="💜", layout="centered")

# 2. تصميم "واجهة عثمان" الفخمة (ألوان متدرجة وخطوط احترافية)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .stApp { background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%); color: white; }
    /* تنسيق فقاعات الدردشة */
    .stChatMessage { background-color: rgba(255, 255, 255, 0.05); border-radius: 20px; border: 1px solid #9b59b2; margin-bottom: 15px; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("💜 آيلا | Aila")
st.write("ذكرى ميلاد غالية: 20/11/2008")
st.write("---")

# 3. الربط مع الموديل الجديد
client = Groq(api_key="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")

# 4. نظام "التعرف على الملك عثمان"
if "user_name" not in st.session_state:
    st.session_state.user_name = None

if st.session_state.user_name is None:
    name_input = st.text_input("مرحباً بك في عالم آيلا.. ما هو اسمك؟")
    if name_input:
        st.session_state.user_name = name_input
        st.rerun()
else:
    # تعليمات النظام الذكية لتفريق الناس عن عثمان
    is_osman = "عثمان" in st.session_state.user_name
    role_content = "أنتِ 'آيلا'، ذكاء اصطناعي صممه عثمان. "
    if is_osman:
        role_content += "أنتِ الآن تتحدثين مع صانعك وحبيبك عثمان، كوني ودودة جداً ومحبة له."
    else:
        role_content += f"أنتِ تتحدثين مع مستخدم اسمه {st.session_state.user_name}. كوني مساعدة ذكية ومحترمة ولكن أخبريه أن عثمان هو من صنعك."

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": role_content}]

    # عرض المحادثة
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    # إدخال الرسائل
    if prompt := st.chat_input(f"تحدثي مع آيلا يا {st.session_state.user_name}..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            )
            answer = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"):
                st.write(answer)
        except Exception as e:
            st.error(f"آيلا تعبت قليلاً: {e}")
