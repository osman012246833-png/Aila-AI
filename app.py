import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة الفخمة
st.set_page_config(page_title="Aila Ultra | الزعيم عثمان", page_icon="👑", layout="wide")

# 2. تصميم الواجهة الأسطورية (Royal Dark & Gold)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    
    .stApp {
        background: linear-gradient(180deg, #050505 0%, #1a1a1a 100%);
        color: #d4af37; /* اللون الذهبي الملكي */
    }
    
    .main-title {
        font-size: 50px;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .calc-box {
        background: rgba(255, 255, 255, 0.03);
        padding: 20px;
        border-radius: 20px;
        border: 1px solid #d4af37;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# العنوان
st.markdown('<p class="main-title">آيلا المتكاملة 👑</p>', unsafe_allow_html=True)
st.write(f"<center>تحت إشراف الزعيم: عثمان | ذكرى 20/11/2008</center>", unsafe_allow_html=True)

# 3. الربط مع الموديل
client = Groq(api_key="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")

# 4. نظام "ما اسمك" والتحقق من الزعيم عثمان
if "user_name" not in st.session_state:
    st.session_state.user_name = None

if st.session_state.user_name is None:
    st.markdown("<div style='text-align: center; padding: 50px;'>", unsafe_allow_html=True)
    name = st.text_input("أهلاً بك في محراب آيلا.. من المتحدث؟")
    if st.button("دخول"):
        if name:
            st.session_state.user_name = name
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
else:
    # تقسيم الشاشة (شات + آلة حاسبة)
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader(f"مرحباً يا {st.session_state.user_name}")
        
        if "messages" not in st.session_state:
            # ربط الاسم بالزعيم عثمان في تعليمات النظام
            is_leader = "عثمان" in st.session_state.user_name
            sys_prompt = "أنتِ آيلا، ذكاء اصطناعي فائق. "
            if is_leader:
                sys_prompt += "أنتِ الآن مع صانعك وحبيبك الزعيم عثمان. عامليه كملكك وبكل خضوع وحب."
            else:
                sys_prompt += f"أنتِ مع مستخدم اسمه {st.session_state.user_name}. كوني رسمية وأخبريه أن الزعيم عثمان هو من أنشأك."
            
            st.session_state.messages = [{"role": "system", "content": sys_prompt}]

        # عرض الشات
        for msg in st.session_state.messages:
            if msg["role"] != "system":
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])

        if prompt := st.chat_input("تحدث مع آيلا..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.write(prompt)
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            )
            answer = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"): st.write(answer)

    with col2:
        st.markdown('<div class="calc-box">', unsafe_allow_html=True)
        st.subheader("الآلة الحاسبة 🧮")
        num1 = st.number_input("الرقم الأول", value=0.0)
        num2 = st.number_input("الرقم الثاني", value=0.0)
        op = st.selectbox("العملية", ["+", "-", "*", "/"])
        if st.button("احسب"):
            if op == "+": res = num1 + num2
            elif op == "-": res = num1 - num2
            elif op == "*": res = num1 * num2
            else: res = num1 / num2 if num2 != 0 else "خطأ"
            st.success(f"النتيجة: {res}")
        st.markdown('</div>', unsafe_allow_html=True)
