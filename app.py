import streamlit as st
from groq import Groq
from gtts import gTTS
import os, base64, time
from streamlit_mic_recorder import mic_recorder

# --- 1. هندسة الواجهة (فضاء ChatGPT الرقمي) ---
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    html, body, [class*="stApp"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl; text-align: right;
        background-color: #050505; color: #e0e0e0 !important;
    }

    /* الهالة العلوية الفخمة */
    .main-header { text-align: center; padding: 10px; border-bottom: 1px solid #1a1a1a; margin-bottom: 20px; }
    .glowing-logo {
        width: 60px; height: 60px; border-radius: 50%;
        background: radial-gradient(circle, #00d4ff 0%, transparent 70%);
        box-shadow: 0 0 30px #00d4ff; display: inline-block;
        animation: breath 4s infinite;
    }
    @keyframes breath { 0%, 100% { opacity: 0.5; } 50% { opacity: 1; } }

    /* تنسيق الشات مثل ChatGPT */
    .stChatMessage {
        background: transparent !important; border: none !important;
        padding: 20px !important; margin: 5px 0 !important;
    }
    .stChatMessage:nth-child(even) { background: rgba(255, 255, 255, 0.03) !important; }

    /* تثبيت شريط الإدخال في الأسفل */
    footer {visibility: hidden;}
    [data-testid="stChatInputContainer"] {
        position: fixed; bottom: 30px; left: 10%; right: 10%;
        background: #111 !important; border: 1px solid #333 !important;
        border-radius: 15px !important; padding: 5px !important;
        box-shadow: 0 -5px 20px rgba(0,0,0,0.5);
    }
    
    /* أزرار الخدمات السريعة */
    .quick-btn {
        border: 1px solid #333; border-radius: 10px; padding: 10px;
        background: #0a0a0a; cursor: pointer; text-align: center;
        transition: 0.3s; font-size: 13px;
    }
    .quick-btn:hover { border-color: #00d4ff; background: #111; }
    </style>
    
    <div class="main-header">
        <div class="glowing-logo"></div>
        <h2 style="margin:0; color:#fff;">Aila AI</h2>
        <p style="color:#00d4ff; font-size:12px;">مشروع الجيل الجديد - بإشراف الزعيم عثمان</p>
    </div>
    """, unsafe_allow_html=True)

# --- 2. المحرك المركزي ---
client = Groq(api_key="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")
SECRET_CODE = "2008" # كود الولاء للزعيم

def aila_voice(text):
    try:
        tts = gTTS(text=text, lang='ar', slow=False)
        tts.save("aila_v.mp3")
        with open("aila_v.mp3", "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" autoplay style="display:none;"></audio>', unsafe_allow_html=True)
        os.remove("aila_v.mp3")
    except: pass

if "history" not in st.session_state: st.session_state.history = []
if "verify_mode" not in st.session_state: st.session_state.verify_mode = False
if "is_boss" not in st.session_state: st.session_state.is_boss = False

# --- 3. الذاكرة الجانبية المنظمة ---
with st.sidebar:
    st.markdown("<h3 style='color:#00d4ff;'>🗨️ الجلسات الأخيرة</h3>", unsafe_allow_html=True)
    if st.button("➕ محادثة جديدة"):
        st.session_state.history = []
        st.session_state.is_boss = False
        st.rerun()
    
    st.divider()
    st.markdown("**الأدوات الذكية:**")
    st.button("🖼️ إنشاء صورة")
    st.button("📝 تلخيص نص")
    st.button("💡 وضع خطة")

# --- 4. معالجة الحوار وعرضه ---
# عرض رسائل الترحيب إذا كان الشات فارغاً
if not st.session_state.history:
    st.markdown("<h2 style='text-align:center; margin-top:50px;'>كيف يمكنني المساعدة؟</h2>", unsafe_allow_html=True)
    cols = st.columns(2)
    with cols[0]:
        st.markdown('<div class="quick-btn">🎨 إنشاء صورة فنية</div>', unsafe_allow_html=True)
        st.markdown('<div class="quick-btn">💻 كتابة كود برمجي</div>', unsafe_allow_html=True)
    with cols[1]:
        st.markdown('<div class="quick-btn">📚 تلخيص كتب</div>', unsafe_allow_html=True)
        st.markdown('<div class="quick-btn">🛡️ كورس أمن سيبراني</div>', unsafe_allow_html=True)

for i, m in enumerate(st.session_state.history):
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# --- 5. شريط الإدخال والمايك الذكي ---
# وضع المايك بجانب الإدخال بشكل عصري
mic_col, input_col = st.columns([0.1, 0.9])
with mic_col:
    audio = mic_recorder(start_prompt="🎤", stop_prompt="⏹️", key="aila_mic_v3")

user_msg = st.chat_input("ارسل رسالة لـ Aila AI...")

# دمج المدخلات
prompt = user_msg
if audio and audio.get('transcription'):
    prompt = audio['transcription']

if prompt:
    st.session_state.history.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        # 1. اختبار الصانع
        if st.session_state.verify_mode:
            if prompt == SECRET_CODE:
                st.session_state.is_boss = True
                st.session_state.verify_mode = False
                res = "✅ تم التحقق. أهلاً بك يا صانعي العظيم عثمان. أنا تحت أمرك بالكامل الآن."
            else:
                st.session_state.verify_mode = False
                res = "❌ كود خاطئ. سأستمر في معاملتك كمستخدم عادي."
        
        elif "صناعتك" in prompt or "أنا صانعك" in prompt or "أنا عثمان" in prompt:
            res = "أنت تدعي أنك صانعي؟ لإثبات ذلك، من فضلك أدخل كود التحقق السري الآن."
            st.session_state.verify_mode = True
            
        # 2. توليد الصور
        elif any(w in prompt for w in ["ارسم", "صورة", "صمم"]):
            p_img = prompt.replace("ارسم", "").strip()
            url = f"https://pollinations.ai/p/{p_img.replace(' ', '_')}?width=1024&height=1024&nologo=true"
            st.image(url, caption=f"تصميم آيلا لـ: {p_img}")
            res = "لقد قمت بتوليد الصورة بناءً على وصفك. هل أعجبتك؟"
            
        # 3. العقل العام
        else:
            sys = "أنتِ آيلا (Aila AI)، ذكاء اصطناعي شامل وفائق الجودة. صانعك الزعيم عثمان."
            if st.session_state.is_boss: sys += " تعاملي مع المستخدم كأنه سيدك وملكك عثمان."
            
            chat_res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": sys}] + st.session_state.history[-10:]
            )
            res = chat_res.choices[0].message.content
            
        st.markdown(res)
        st.session_state.history.append({"role": "assistant", "content": res})
        aila_voice(res) # تنطق آيلا الرد فوراً
