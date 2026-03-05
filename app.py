import streamlit as st
from groq import Groq

# --- 1. إعدادات الصفحة والتنسيق البصري ---
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="centered")

# رابط صورة اللوجو الاحترافي اللي أنت اخترته
AILA_AVATAR = "https://raw.githubusercontent.com/OsmanEssam/Aila-AI/main/logo.png" # يفضل ترفع صورتك هنا أو تستخدم الرابط المباشر للصورة اللي عجبتك

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء القوائم غير الضرورية */
    [data-testid="stSidebar"], [data-testid="stSidebarNav"], header { display: none !important; }
    
    html, body, [class*="stApp"] { 
        background-color: #050505; 
        color: #ffffff; 
        font-family: 'Cairo', sans-serif; 
        direction: rtl; 
    }

    .aila-header { text-align: center; padding: 20px; }
    .aila-title {
        font-size: 45px; font-weight: 900; color: #ff00ff;
        text-shadow: 0 0 20px #ff00ff; margin-bottom: 5px;
    }
    
    .osman-badge {
        border: 2px solid #00d4ff; border-radius: 25px;
        padding: 8px 30px; display: inline-block;
        font-size: 15px; color: #ffffff; background: rgba(0, 212, 255, 0.1);
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.4);
        margin-top: 10px;
    }

    /* تثبيت الأفاتار الاحترافي لآيلا */
    [data-testid="stChatMessageAvatarAssistant"] {
        background-image: url('https://i.ibb.co/0YmX4L3/aila-logo.png') !important; /* حط رابط صورتك هنا */
        background-size: cover; border: 2px solid #ff00ff;
    }

    /* تنسيق فقاعات الدردشة */
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    
    .support-footer {
        font-size: 13px; color: #ff00ff; text-align: center;
        margin-top: 30px; border-top: 1px solid #333; padding-top: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. منطق العمل والذكاء ---
if "messages" not in st.session_state: st.session_state.messages = []
client = Groq(api_key="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")

# --- 3. الواجهة الرسومية ---
st.markdown("""
    <div class="aila-header">
        <div style="width:130px; height:130px; border-radius:50%; border:3px solid #ff00ff; display:inline-block; 
        background:url('https://i.ibb.co/0YmX4L3/aila-logo.png') no-repeat center; background-size:cover; box-shadow: 0 0 30px #ff00ff;"></div>
        <div class="aila-title">آيلا | Aila AI</div>
        <div class="osman-badge">إشراف المطور: عثمان عصام</div>
    </div>
""", unsafe_allow_html=True)

# عرض الرسائل
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# إدخال المستخدم
if prompt := st.chat_input("تحدثي معي يا آيلا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        # تعليمات لغوية صارمة جداً لمنع أي لغة أخرى غير العربية
        system_instruction = (
            "أنتِ آيلا (Aila)، مساعد ذكي بليغ صممه المطور عثمان عصام. "
            "قواعد صارمة: أجيبِي باللغة العربية الفصحى فقط. "
            "يُمنع منعاً باتاً استخدام أي حروف يابانية، كورية، صينية، أو إنجليزية في نص الإجابة. "
            "إذا طلب المستخدم عثمان عصام أي شيء، نفذيه بتقدير خاص."
        )
        
        try:
            full_response = ""
            response_container = st.empty()
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": system_instruction}] + st.session_state.messages,
                stream=False
            )
            
            res_text = completion.choices[0].message.content
            
            # عرض الرد مع بصمة المطور
            st.markdown(res_text)
            st.markdown(f"<div class='support-footer'>صُنع بكل فخر بواسطة عثمان عصام - ابن بني سويف</div>", unsafe_allow_html=True)
            
            st.session_state.messages.append({"role": "assistant", "content": res_text})
        except Exception as e:
            st.error("حدث خطأ في الاتصال، حاول مرة أخرى.")
