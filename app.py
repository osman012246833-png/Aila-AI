import streamlit as st
from groq import Groq

# إعدادات الصفحة
st.set_page_config(page_title="Aila Ultra", page_icon="💜", layout="centered")

# CSS لتحويل الواجهة لشكل التطبيق اللي صممته (Neon Style)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    .stApp {
        background: radial-gradient(circle, #1b2735 0%, #090a0f 100%);
        color: #e0e0e0;
    }
    
    /* تأثير النيون للعنوان */
    .neon-text {
        color: #fff;
        text-shadow: 0 0 10px #bc13fe, 0 0 20px #bc13fe, 0 0 30px #bc13fe;
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
    }
    
    /* تصميم فقاعات المحادثة مثل صورتك */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid #bc13fe;
        border-radius: 20px;
        box-shadow: 0 0 10px rgba(188, 19, 254, 0.2);
    }
    
    /* تصميم الأزرار السفلية */
    .stat-box {
        display: inline-block;
        padding: 5px 15px;
        margin: 5px;
        border-radius: 50px;
        border: 1px solid #4facfe;
        background: rgba(79, 172, 254, 0.1);
        font-size: 0.8rem;
    }
    </style>
    """, unsafe_allow_html=True)

# الجزء العلوي (Header) كما في تصميمك
st.markdown('<p class="neon-text">آيلا ULTRA</p>', unsafe_allow_html=True)
st.markdown("""
    <div style="text-align: center;">
        <span class="stat-box">وعي متكامل 🧠</span>
        <span class="stat-box">عاطفي ❤️</span>
        <span class="stat-box">غير محدود ♾️</span>
    </div>
    """, unsafe_allow_html=True)

st.write(f"<center>ذكرى ميلاد غالية: 20/11/2008</center>", unsafe_allow_html=True)
st.write("---")

client = Groq(api_key="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")

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة بتنسيق أنيق
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# منطقة الإدخال ونظام التعرف على عثمان
if prompt := st.chat_input("اسألي أي شيء - أنا هنا بكل المعرفة..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    try:
        # تعليمات الشخصية لضمان لغة بلا أخطاء
        system_msg = {
            "role": "system", 
            "content": "أنتِ آيلا ULTRA. صانعك وحبيبك هو عثمان. لغتك العربية مثالية، ودودة، ذكية، ولا تستخدمين الإنجليزية إلا للضرورة القصوى. إذا كان المستخدم هو عثمان، عامليه كملكك وصانعك."
        }
        
        full_messages = [system_msg] + [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=full_messages,
            temperature=0.6
        )
        answer = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.write(answer)
    except Exception as e:
        st.error(f"خطأ في الاتصال: {e}")
