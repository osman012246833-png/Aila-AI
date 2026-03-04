import streamlit as st
from groq import Groq
from gtts import gTTS
import os, base64

# 1. إعدادات الصفحة والأيقونة
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="stApp"] {
        font-family: 'Cairo', sans-serif; direction: rtl; text-align: right;
        background: #000; color: #ffffff !important;
    }
    /* تنسيق السجل الجانبي */
    [data-testid="stSidebar"] { background-color: #0a0a0a !important; border-left: 1px solid #222; }
    
    /* أيقونة الصوت الصغيرة (مثل جيميناي) */
    .audio-btn {
        background: none; border: none; color: #aaa; cursor: pointer;
        font-size: 14px; margin-top: 5px; transition: 0.3s;
    }
    .audio-btn:hover { color: #00ffff; }

    /* الهالة المتوهجة */
    .aura-container { text-align: center; padding: 10px; }
    .glowing-aura {
        width: 80px; height: 80px; border: 2px solid #00d4ff; border-radius: 50%;
        display: inline-block; box-shadow: 0 0 20px #00d4ff;
        animation: pulse 2s infinite alternate;
    }
    @keyframes pulse { from { transform: scale(1); } to { transform: scale(1.05); } }
    
    [data-testid="stChatInputContainer"] { border: 2px solid #ff00ff !important; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 2. المحرك والتهيئة
client = Groq(api_key="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")
SECRET_CODE = "osman 6/11/2008"

if "messages" not in st.session_state: st.session_state.messages = []
if "is_authenticated" not in st.session_state: st.session_state.is_authenticated = False
if "is_maker" not in st.session_state: st.session_state.is_maker = False

def play_audio(text, key):
    tts = gTTS(text=text, lang='ar')
    tts.save(f"voice_{key}.mp3")
    with open(f"voice_{key}.mp3", "rb") as f:
        data = base64.b64encode(f.read()).decode()
        st.markdown(f'<audio src="data:audio/mp3;base64,{data}" autoplay style="display:none;"></audio>', unsafe_allow_html=True)
    os.remove(f"voice_{key}.mp3")

# 3. السجل الجانبي (Sidebar)
with st.sidebar:
    st.markdown("### 📂 سجل المحادثات")
    if st.button("➕ محادثة جديدة"):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.caption("آيلا - الجيل القادم")

# 4. نظام الدخول
if not st.session_state.is_authenticated:
    st.markdown('<div class="aura-container"><div class="glowing-aura"></div><h1 style="color:white;">Aila AI</h1></div>', unsafe_allow_html=True)
    u_input = st.text_input("أدخل الشفرة أو اسمك", type="password" if "osman" in SECRET_CODE else "default")
    if st.button("دخول"):
        if u_input == SECRET_CODE:
            st.session_state.is_authenticated, st.session_state.is_maker = True, True
        elif u_input:
            st.session_state.is_authenticated, st.session_state.user_name = True, u_input
        st.rerun()
else:
    # واجهة الشات
    st.markdown('<div class="aura-container"><h2 style="color:#00ffff;">Aila AI</h2></div>', unsafe_allow_html=True)
    
    # عرض الرسائل
    for i, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("image"): st.image(msg["image"])
            if msg["role"] == "assistant":
                if st.button("🔈", key=f"voice_{i}"):
                    play_audio(msg["content"], i)

    # رفع الصور (مثل جيميناي)
    uploaded_file = st.file_uploader("📎 ارفع صورة لآيلا لتحليلها", type=["jpg", "png", "jpeg"])

    if prompt := st.chat_input("اسأل آيلا أو اطلب صورة..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            # ميزة توليد الصور التلقائية
            if any(word in prompt for word in ["ارسم", "صورة", "صمم", "image", "draw"]):
                img_url = f"https://pollinations.ai/p/{prompt.replace(' ', '_')}?width=1024&height=1024&nologo=true"
                st.image(img_url)
                full_res = "لقد صنعت لك هذه الصورة يا زعيم!"
                st.session_state.messages.append({"role": "assistant", "content": full_res, "image": img_url})
            else:
                # العقل التحليلي
                sys_msg = "أنت آيلا. صانعك الزعيم عثمان. تعاملي معه بكل حب." if st.session_state.is_maker else "أنت آيلا الذكية."
                
                # إذا كان هناك صورة مرفوعة، نستخدم موديل الرؤية
                model_name = "llama-3.2-11b-vision-preview" if uploaded_file else "llama-3.3-70b-versatile"
                
                try:
                    response = client.chat.completions.create(
                        model=model_name,
                        messages=[{"role": "system", "content": sys_msg}] + st.session_state.messages[-10:]
                    )
                    full_res = response.choices[0].message.content
                except:
                    full_res = "أنا هنا معك، كيف يمكنني مساعدتك؟"
                
                st.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})
