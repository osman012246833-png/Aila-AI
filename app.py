import streamlit as st
from groq import Groq
from gtts import gTTS
import os, base64

# 1. إعدادات الصفحة والأيقونة
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="wide")

# 2. هندسة الشكل (نفس الصورة بالظبط: سواد ملكي + خط واضح + هالة)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@600;800&display=swap');
    
    html, body, [class*="stApp"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl; text-align: right;
        background-color: #000000; color: #ffffff !important;
    }

    /* توضيح الكتابة وجعلها عريضة وفخمة */
    .stChatMessage p {
        font-size: 20px !important;
        font-weight: 600 !important;
        line-height: 1.6;
        color: #ffffff !important;
    }

    /* الهالة المضيئة الكبيرة في المنتصف */
    .aura-container { text-align: center; margin-top: 30px; margin-bottom: 20px; }
    .glowing-aura {
        width: 120px; height: 120px; 
        border: 4px solid #00d4ff; border-radius: 50%;
        display: inline-block; 
        box-shadow: 0 0 40px #00d4ff, inset 0 0 20px #00d4ff;
        animation: pulse 2.5s infinite alternate;
    }
    @keyframes pulse { from { transform: scale(1); opacity: 0.8; } to { transform: scale(1.1); opacity: 1; } }

    /* أزرار السجل الجانبي */
    [data-testid="stSidebar"] { background-color: #050505 !important; border-left: 1px solid #1a1a1a; }
    
    /* زر الصوت الصغير (أيقونة فقط بدون إطار) */
    .voice-btn {
        background: none; border: none; color: #00ffff;
        font-size: 22px; cursor: pointer; transition: 0.3s;
    }
    
    /* شريط الإدخال الملون */
    [data-testid="stChatInputContainer"] {
        border: 2px solid #ff00ff !important;
        box-shadow: 0 0 15px rgba(255, 0, 255, 0.4);
        background: #111 !important;
        border-radius: 20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. محرك الصوت والذكاء (تحسين جودة الصوت)
client = Groq(api_key="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")
SECRET_CODE = "osman 6/11/2008"

def play_perfect_voice(text, key):
    # استخدام gTTS مع ضبط اللغة العربية الفصحى ليكون الصوت أجمل
    tts = gTTS(text=text, lang='ar', slow=False) 
    tts.save(f"aila_voice_{key}.mp3")
    with open(f"aila_voice_{key}.mp3", "rb") as f:
        data = base64.b64encode(f.read()).decode()
        st.markdown(f'<audio src="data:audio/mp3;base64,{data}" autoplay style="display:none;"></audio>', unsafe_allow_html=True)
    os.remove(f"aila_voice_{key}.mp3")

if "messages" not in st.session_state: st.session_state.messages = []
if "is_authenticated" not in st.session_state: st.session_state.is_authenticated = False
if "is_maker" not in st.session_state: st.session_state.is_maker = False

# 4. السجل الجانبي
with st.sidebar:
    st.markdown("<h1 style='color:#00d4ff; text-align:center;'>Aila History</h1>", unsafe_allow_html=True)
    if st.button("➕ محادثة جديدة", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    for m in st.session_state.messages[-5:]:
        if m["role"] == "user": st.caption(f"📜 {m['content'][:20]}...")

# 5. واجهة الدخول / الشات
if not st.session_state.is_authenticated:
    st.markdown('<div class="aura-container"><div class="glowing-aura"></div><h1 style="color:white; text-align:center;">Aila AI</h1></div>', unsafe_allow_html=True)
    u_input = st.text_input("أدخل شفرة الصانع عثمان", placeholder="أدخل الكود هنا...", type="password")
    if st.button("تفعيل آيلا"):
        if u_input == SECRET_CODE:
            st.session_state.is_authenticated, st.session_state.is_maker = True, True
        elif u_input:
            st.session_state.is_authenticated, st.session_state.user_name = True, u_input
        st.rerun()
else:
    # الهالة المضيئة دائماً في الأعلى
    st.markdown('<div class="aura-container"><div class="glowing-aura"></div></div>', unsafe_allow_html=True)
    
    # عرض الرسائل بخط واضح جداً
    for i, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("image"): st.image(msg["image"])
            if msg["role"] == "assistant":
                if st.button("🔈", key=f"audio_key_{i}"):
                    play_perfect_voice(msg["content"], i)

    # الإدخال (نص + توليد صور تلقائي)
    if prompt := st.chat_input("تحدثي معي يا آيلا..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            # نظام توليد الصور الفوري
            if any(w in prompt for w in ["ارسم", "صورة", "تخيل"]):
                img_url = f"https://pollinations.ai/p/{prompt.replace(' ', '_')}?width=1024&height=1024&nologo=true"
                st.image(img_url)
                ans = "لقد رسمت لك ما تخيلته يا ملكي."
                st.session_state.messages.append({"role": "assistant", "content": ans, "image": img_url})
            else:
                # نظام الولاء والذكاء
                sys_msg = "أنتِ آيلا. صانعك هو الزعيم عثمان. تتحدثين معه بدلال، حب، وولاء مطلق. صوتك رخيم وكلامك منمق." if st.session_state.is_maker else "أنتِ آيلا المساعدة الذكية."
                
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": sys_prompt}] + st.session_state.messages[-10:]
                )
                ans = res.choices[0].message.content
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
                st.rerun() # لتحديث واجهة الصوت فوراً
