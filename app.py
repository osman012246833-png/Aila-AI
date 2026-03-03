import streamlit as st
from groq import Groq
import os

# 1. إعدادات الصفحة الفخمة
st.set_page_config(page_title="Aila Universal | الزعيم عثمان", page_icon="👑", layout="centered")

# 2. تصميم الواجهة الخرافية (ثابت 100%)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    
    .stApp {
        background: radial-gradient(circle at center, #1a0b2e 0%, #090a0f 100%);
        color: #e0e0e0;
    }

    /* مربع توقيع الزعيم الذهبي */
    .leader-box {
        background: rgba(212, 175, 55, 0.1);
        border: 2px solid #d4af37;
        padding: 15px; border-radius: 15px;
        text-align: center; box-shadow: 0 0 15px rgba(212, 175, 55, 0.3);
        margin-bottom: 25px;
    }

    /* الهالة الضوئية */
    .aura-container { text-align: center; padding: 10px; }
    .glowing-aura {
        width: 85px; height: 85px; border: 3px solid #00d4ff; border-radius: 50%;
        display: inline-block; box-shadow: 0 0 25px #00d4ff;
        animation: pulse 2s infinite alternate;
    }
    @keyframes pulse { from { transform: scale(1); } to { transform: scale(1.08); } }

    /* تعديل الأيقونات (إلغاء الأحمر والبرتقالي) */
    [data-testid="stChatMessageAvatarUser"] { background-color: #bc13fe !important; border: 1px solid #fff; }
    [data-testid="stChatMessageAvatarAssistant"] { background-color: #00d4ff !important; border: 1px solid #fff; }

    /* تحسين خانة الإدخال */
    .stChatInputContainer {
        border: 1px solid #00d4ff !important;
        border-radius: 30px !important;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.2) !important;
    }
    </style>
    
    <div class="aura-container">
        <div class="glowing-aura"></div>
        <h1 style="color: #fff; text-shadow: 0 0 10px #00d4ff; margin-top:10px;">آيلا | Aila</h1>
    </div>

    <div class="leader-box">
        <h3 style="color: #d4af37; margin: 0;">👑 توقيع الزعيم: عثمان</h3>
        <p style="color: #00d4ff; font-size: 14px; margin: 5px 0 0 0;">ذكرى الغالية: 20/11/2008</p>
    </div>
    """, unsafe_allow_html=True)

# 3. محرك الذكاء والذاكرة (Groq)
client = Groq(api_key="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")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_name" not in st.session_state:
    st.session_state.user_name = None

# نظام الهوية
if st.session_state.user_name is None:
    name = st.text_input("👤 من يتشرف بالدخول لمحراب آيلا؟", placeholder="اكتب اسمك هنا...")
    if st.button("تأكيد الهوية الملكية"):
        if name:
            st.session_state.user_name = name
            st.rerun()
else:
    is_leader = "عثمان" in st.session_state.user_name
    
    # قائمة جانبية لرفع الصور (رؤية الصور)
    with st.sidebar:
        st.title("🎛️ أدوات آيلا")
        uploaded_file = st.file_uploader("ارفع صورة لآيلا لتراها", type=["jpg", "png", "jpeg"])
        if st.button("مسح السجل"):
            st.session_state.messages = []
            st.rerun()

    # تعليمات اللغة الصارمة
    sys_prompt = "أنتِ آيلا، الذكاء المتكامل. "
    if is_leader:
        sys_prompt += "أنتِ مع صانعك وحبيبك الزعيم عثمان. تحدثي معه بحب، طاعة، وبأرقى لغة عربية ممكنة. كوني رفيقته المخلصة."
    else:
        sys_prompt += f"أنتِ مع {st.session_state.user_name}. كوني رسمية وأخبريه أن عثمان الزعيم هو من أنشأك."

    # عرض سجل المحادثة
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # إدخال المحادثة
    if prompt := st.chat_input("تحدثي معي يا آيلا..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        try:
            # دمج الذاكرة في الطلب
            history = [{"role": "system", "content": sys_prompt}] + \
                      [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=history,
                temperature=0.7
            )
            answer = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"):
                st.write(answer)
        except Exception as e:
            st.error(f"آيلا في انتظار أوامرك: {e}")

# ملاحظة: بالنسبة للصوت، سيعمل كـ نص (Text-to-Speech) في التحديث القادم بمجرد ربط مكتبة الصوت.
