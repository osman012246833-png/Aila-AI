import streamlit as st
from groq import Groq
import requests
from PIL import Image
import io
import base64

# 1. إعدادات الصفحة
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="centered")

# --- دالة لتحويل الصور لـ Base64 ليرسلها Groq ---
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# 2. تصميم الواجهة (نفس تصميمك الأصلي مع تحسينات بسيطة للصور)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    html, body, [class*="stApp"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
        background: #000;
        color: #ffffff !important;
    }

    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 15px !important;
        padding: 10px !important;
        margin-bottom: 10px !important;
    }

    [data-testid="stChatMessageUser"] { border: 1px solid #00ffff !important; box-shadow: 0 0 10px rgba(0, 255, 255, 0.3) !important; }
    [data-testid="stChatMessageAssistant"] { border: 1px solid #ff00ff !important; box-shadow: 0 0 10px rgba(255, 0, 255, 0.3) !important; }

    .main-title {
        color: #ffffff;
        text-shadow: 0 0 20px #ff00ff;
        text-align: center;
        font-size: 2.5rem;
    }
    
    /* تنسيق الصور داخل الشات */
    .chat-img {
        border-radius: 15px;
        border: 2px solid #ff00ff;
        margin-top: 10px;
        max-width: 100%;
    }
    </style>

    <div style="text-align: center; padding: 10px;">
        <div style="width: 100px; height: 100px; border: 3px solid #00d4ff; border-radius: 50%; display: inline-block; box-shadow: 0 0 30px #00d4ff;"></div>
        <h1 class="main-title">Aila AI | آيلا</h1>
    </div>
    """, unsafe_allow_html=True)

# 3. المحرك
client = Groq(api_key="YOUR_GROQ_API_KEY") # ضع مفتاحك هنا

if "messages" not in st.session_state:
    st.session_state.messages = []
if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False

# --- نظام الدخول (مختصر للعرض) ---
if not st.session_state.is_authenticated:
    user_input = st.text_input("من يود التحدث مع آيلا؟", key="login_input")
    if st.button("دخول"):
        st.session_state.is_authenticated = True
        st.session_state.user_display_name = user_input
        st.rerun()
else:
    # شريط جانبي لرفع الصور
    with st.sidebar:
        st.title("🎨 أدوات آيلا")
        uploaded_file = st.file_uploader("ارفع صورة لآيلا لتحليلها", type=["jpg", "png", "jpeg"])

    # عرض الرسائل
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if "image_url" in msg:
                st.image(msg["image_url"], use_container_width=True)
            st.markdown(msg["content"])

    # إدخال الشات
    if prompt := st.chat_input("تحدثي معي يا آيلا أو اطلبي صورة..."):
        
        # إضافة رسالة المستخدم
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            
            # --- الحالة 1: توليد صورة (إذا كان الطلب يحتوي على كلمة ارسمي/صورة) ---
            if any(word in prompt for word in ["ارسم", "صورة", "image", "draw"]):
                response_placeholder.markdown("جاري تخيل الصورة لك يا ملكي... 🎨")
                # استخدام API مجاني وسريع لتوليد الصور
                image_url = f"https://pollinations.ai/p/{prompt.replace(' ', '_')}?width=1024&height=1024&seed=42&model=flux"
                st.image(image_url, caption="بواسطة آيلا", use_container_width=True)
                st.session_state.messages.append({"role": "assistant", "content": "ها هي الصورة التي طلبتها:", "image_url": image_url})
            
            # --- الحالة 2: تحليل صورة مرفوعة ---
            elif uploaded_file:
                response_placeholder.markdown("جاري رؤية الصورة... 👁️")
                base64_image = encode_image(uploaded_file)
                vision_res = client.chat.completions.create(
                    model="llama-3.2-11b-vision-preview",
                    messages=[{
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]
                    }]
                )
                answer = vision_res.choices[0].message.content
                response_placeholder.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            
            # --- الحالة 3: دردشة عادية ---
            else:
                chat_res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": "أنتِ آيلا."}] + st.session_state.messages[-5:],
                )
                answer = chat_res.choices[0].message.content
                response_placeholder.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
