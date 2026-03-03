import streamlit as st
from groq import Groq
from gtts import gTTS
import os, base64
from streamlit_mic_recorder import mic_recorder

# --- 1. إعدادات الهوية البصرية (الفخامة المطلقة) ---
st.set_page_config(page_title="Aila AI | الجيل الجديد", page_icon="💠", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    html, body, [class*="stApp"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl; text-align: right;
        background: radial-gradient(circle at center, #0a0a2e 0%, #000000 100%);
        color: #ffffff !important;
    }

    /* الهالة المتوهجة في الأعلى */
    .top-aura { text-align: center; padding: 30px 0; }
    .glowing-sphere {
        width: 100px; height: 100px;
        background: radial-gradient(circle, #00d4ff 0%, transparent 75%);
        border-radius: 50%; display: inline-block;
        box-shadow: 0 0 50px #00d4ff;
        animation: breath 3s infinite alternate;
    }
    @keyframes breath { from { opacity: 0.5; transform: scale(1); } to { opacity: 1; transform: scale(1.1); } }

    /* تنسيق فقاعات الدردشة الزجاجية */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(0, 212, 255, 0.3) !important;
        border-radius: 20px !important;
        backdrop-filter: blur(12px);
    }

    /* شريط الإدخال والمايك */
    [data-testid="stChatInputContainer"] {
        border: 2px solid #ff00ff !important;
        border-radius: 30px !important;
        background: rgba(0, 0, 0, 0.8) !important;
    }
    </style>
    
    <div class="top-aura">
        <div class="glowing-sphere"></div>
        <h1 style="text-shadow: 0 0 20px #00d4ff;">آيلا | Aila AI</h1>
        <div style="display: flex; justify-content: center; gap: 10px;">
            <span style="border:1px solid #ff00ff; padding:2px 15px; border-radius:20px; font-size:12px;">بإشراف الزعيم عثمان</span>
            <span style="border:1px solid #ff00ff; padding:2px 15px; border-radius:20px; font-size:12px;">توليد صور + صوت</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 2. محركات الذكاء (صوت + نص + صور) ---
# تأكد من وضع مفتاح Groq الخاص بك هنا
client = Groq(api_key="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")

def speak(text):
    try:
        tts = gTTS(text=text, lang='ar', slow=False)
        tts.save("aila_v.mp3")
        with open("aila_v.mp3", "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" autoplay style="display:none;"></audio>', unsafe_allow_html=True)
        os.remove("aila_v.mp3")
    except: pass

if "messages" not in st.session_state: st.session_state.messages = []

# --- 3. عرض المحادثة والذاكرة ---
for i, m in enumerate(st.session_state.messages):
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m["role"] == "assistant" and "http" not in m["content"]: # لا تظهر زر الصوت لو الرد صورة فقط
            if st.button("🔊 استمع", key=f"btn_{i}"): speak(m["content"])

# --- 4. منطقة التفاعل الذكي (المايك + الإدخال) ---
c1, c2 = st.columns([0.1, 0.9])
with c1:
    audio_data = mic_recorder(start_prompt="🎤", stop_prompt="✅", key="aila_mic")
with c2:
    user_query = st.chat_input("اطلب صورة أو اسأل آيلا أي شيء...")

# معالجة المدخلات (سواء بالصوت أو بالكتابة)
final_query = user_query
if audio_data and audio_data.get('transcription'):
    final_query = audio_data['transcription']

if final_query:
    st.session_state.messages.append({"role": "user", "content": final_query})
    with st.chat_message("user"): st.markdown(final_query)

    with st.chat_message("assistant"):
        # فحص إذا كان المستخدم يطلب صورة
        image_keywords = ["ارسم", "صورة", "صمم", "تخيل", "draw", "image", "picture"]
        if any(word in final_query.lower() for word in image_keywords):
            # توليد الصورة عبر Pollinations AI
            img_desc = final_query
            for word in image_keywords: img_desc = img_desc.replace(word, "")
            img_url = f"https://pollinations.ai/p/{img_desc.strip().replace(' ', '_')}?width=1024&height=1024&nologo=true"
            
            st.markdown(f"**إليك ما تخيلته بناءً على طلبك يا زعيم:**")
            st.image(img_url, use_container_width=True)
            ans = "لقد قمت بتحويل كلماتك إلى لوحة فنية، هل نالت إعجابك؟"
        else:
            # الرد النصي الذكي الشامل
            sys_msg = "أنتِ آيلا، ذكاء اصطناعي فائق، صانعك الزعيم عثمان. تتحدثين العربية الفصحى بذكاء ومعرفة شاملة بكل شيء."
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": sys_prompt}] + st.session_state.messages[-10:]
            )
            ans = response.choices[0].message.content
        
        st.markdown(ans)
        st.session_state.messages.append({"role": "assistant", "content": ans})
        speak(ans) # النطق التلقائي للرد النصي
