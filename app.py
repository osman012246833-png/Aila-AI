import streamlit as st
from groq import Groq
from gtts import gTTS
import os, base64
from streamlit_mic_recorder import mic_recorder

# --- 1. تصميم "المعبد الرقمي" الفاخر ---
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    html, body, [class*="stApp"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl; text-align: right;
        background: radial-gradient(circle at center, #0a0a2e 0%, #000000 100%);
        color: #ffffff !important;
    }

    /* الهالة المتوهجة المركزية */
    .top-aura { text-align: center; padding: 20px 0; }
    .glowing-sphere {
        width: 100px; height: 100px;
        background: radial-gradient(circle, #00d4ff 0%, transparent 75%);
        border-radius: 50%; display: inline-block;
        box-shadow: 0 0 60px #00d4ff;
        animation: breath 3s infinite alternate;
    }
    @keyframes breath { from { opacity: 0.5; transform: scale(1); } to { opacity: 1; transform: scale(1.1); } }

    /* تنسيق الزجاج الهولوغرافي للمحادثات */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(0, 212, 255, 0.3) !important;
        border-radius: 15px !important;
        backdrop-filter: blur(15px);
        margin-bottom: 10px !important;
    }
    
    /* أزرار السجل والتحكم */
    .stButton>button {
        background: linear-gradient(45deg, #00d4ff, #ff00ff);
        color: white; border: none; border-radius: 20px; transition: 0.3s;
    }

    /* شريط الإدخال المتطور */
    [data-testid="stChatInputContainer"] {
        border: 2px solid #00d4ff !important;
        border-radius: 25px !important;
        background: rgba(0, 0, 0, 0.9) !important;
    }
    </style>
    
    <div class="top-aura">
        <div class="glowing-sphere"></div>
        <h1 style="text-shadow: 0 0 20px #ff00ff; margin-top:10px;">Aila AI | آيلا</h1>
        <div style="display: flex; justify-content: center; gap: 10px;">
            <span style="border:1px solid #00ffff; padding:2px 12px; border-radius:15px; font-size:11px;">بإشراف الزعيم عثمان</span>
            <span style="border:1px solid #00ffff; padding:2px 12px; border-radius:15px; font-size:11px;">ذكرى 20/11/2008</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 2. المحرك الذكي (عقل آيلا الشامل) ---
# مفتاح الـ API الخاص بك جاهز للعمل
client = Groq(api_key="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")

def aila_voice_output(text):
    """نطق الرد بصوت فخم"""
    try:
        tts = gTTS(text=text, lang='ar', slow=False)
        tts.save("reply.mp3")
        with open("reply.mp3", "rb") as f:
            data = base64.b64encode(f.read()).decode()
            st.markdown(f'<audio src="data:audio/mp3;base64,{data}" autoplay style="display:none;"></audio>', unsafe_allow_html=True)
        os.remove("reply.mp3")
    except: pass

if "history" not in st.session_state:
    st.session_state.history = []

# --- 3. سجل المحادثات (التنسيق الجانبي المطور) ---
with st.sidebar:
    st.markdown("<h3 style='color:#00d4ff;'>📂 الذاكرة الرقمية</h3>", unsafe_allow_html=True)
    if st.button("🗑️ مسح السجل والبدء من جديد"):
        st.session_state.history = []
        st.rerun()
    st.divider()
    st.write("آيلا الآن تدعم:")
    st.write("✅ الفهم الصوتي الكامل")
    st.write("✅ توليد الصور الفوري")
    st.write("✅ البحث العالمي والروابط")

# --- 4. عرض الرسائل والتفاعل ---
for i, msg in enumerate(st.session_state.history):
    role_icon = "👤" if msg["role"] == "user" else "💠"
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and "http" not in msg["content"]:
            if st.button("🔊 استماع", key=f"speak_{i}"): aila_voice_output(msg["content"])

# --- 5. منطقة الإدخال الشاملة (المايك + النص) ---
col_mic, col_input = st.columns([0.1, 0.9])

with col_mic:
    # المايك الذي يفهم صوتك ويحوله لأوامر لآيلا
    audio_capture = mic_recorder(start_prompt="🎤", stop_prompt="✅", key="voice_input")

with col_input:
    user_prompt = st.chat_input("تحدثي معي يا آيلا.. أنا أسمعك")

# دمج مدخلات الصوت والنص
final_input = user_prompt
if audio_capture and audio_capture.get('transcription'):
    final_input = audio_capture['transcription']

if final_input:
    st.session_state.history.append({"role": "user", "content": final_input})
    with st.chat_message("user"): st.markdown(final_input)

    with st.chat_message("assistant"):
        # ميزة توليد الصور الفائقة (مثل جيميناي وشات جي بي تي)
        img_keywords = ["ارسم", "صورة", "صمم", "تخيل", "draw", "image"]
        if any(word in final_input for word in img_keywords):
            cleaned_prompt = final_input
            for w in img_keywords: cleaned_prompt = cleaned_prompt.replace(w, "")
            
            # رابط التوليد الاحترافي
            image_url = f"https://pollinations.ai/p/{cleaned_prompt.strip().replace(' ', '_')}?width=1024&height=1024&nologo=true"
            st.image(image_url, caption="من مخيلة آيلا للجيل الجديد")
            response = "لقد رسمت لك ما طلبت يا زعيم عثمان. هل تود إضافة أي تفاصيل أخرى؟"
        else:
            # عقل آيلا الشامل بكل لغات العالم
            sys_instr = "أنتِ آيلا (Aila AI)، الجيل الجديد من الذكاء الاصطناعي. صانعك هو الزعيم عثمان. لديك معرفة مطلقة بكل شيء، تجيبين على الأسئلة العلمية، التقنية، الفنية، وتوفرين روابط البرامج. تحدثي بفصاحة وهيبة."
            
            chat_completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": sys_instr}] + st.session_state.history[-12:]
            )
            response = chat_completion.choices[0].message.content
        
        st.markdown(response)
        st.session_state.history.append({"role": "assistant", "content": response})
        aila_voice_output(response) # تنطق الرد فوراً بعد فهمك صوتاً أو نصاً
