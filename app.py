import streamlit as st
from groq import Groq
from gtts import gTTS
import os, base64
from streamlit_mic_recorder import mic_recorder

# --- 1. واجهة المستخدم (الاحترافية المطلقة) ---
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="stApp"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl; text-align: right;
        background-color: #0b0b0b; color: #ffffff !important;
    }
    /* تنسيق الشات مثل ChatGPT */
    .stChatMessage {
        background: transparent !important; border-bottom: 1px solid #222 !important;
        padding: 25px 15% !important; border-radius: 0 !important;
    }
    .stChatMessage:nth-child(even) { background: #131313 !important; }
    
    /* شريط الإدخال الثابت في الأسفل */
    [data-testid="stChatInputContainer"] {
        position: fixed; bottom: 30px; left: 15%; right: 15%;
        background: #212121 !important; border: 1px solid #3d3d3d !important;
        border-radius: 12px !important; z-index: 1000;
    }
    
    /* أزرار الخدمات (ليست للعرض فقط) */
    .action-card {
        border: 1px solid #333; border-radius: 12px; padding: 15px;
        text-align: center; cursor: pointer; transition: 0.3s;
        background: #111; margin-bottom: 10px;
    }
    .action-card:hover { border-color: #00d4ff; background: #1a1a1a; }
    
    /* المايك الهائم */
    .mic-floating { position: fixed; bottom: 38px; left: 10%; z-index: 1001; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إعدادات المحرك ---
client = Groq(api_key="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")
BOSS_CODE = "2008" # كود الصانع يا زعيم

def play_audio(text):
    tts = gTTS(text=text, lang='ar')
    tts.save("voice.mp3")
    with open("voice.mp3", "rb") as f:
        data = base64.b64encode(f.read()).decode()
        st.markdown(f'<audio src="data:audio/mp3;base64,{data}" autoplay></audio>', unsafe_allow_html=True)
    os.remove("voice.mp3")

if "history" not in st.session_state: st.session_state.history = []
if "is_boss" not in st.session_state: st.session_state.is_boss = False
if "ask_code" not in st.session_state: st.session_state.ask_code = False

# --- 3. الواجهة الجانبية (الذاكرة) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=50)
    st.title("Aila AI")
    if st.button("➕ محادثة جديدة", use_container_width=True):
        st.session_state.history = []
        st.session_state.is_boss = False
        st.rerun()
    st.divider()
    st.write("🔧 الإعدادات")
    st.caption("إصدار الجيل القادم 1.0.2")

# --- 4. العرض الترحيبي (مثل ChatGPT) ---
if not st.session_state.history:
    st.markdown("<h1 style='text-align:center; margin-top:100px;'>كيف يمكنني مساعدتك اليوم؟</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🖼️ إنشاء صورة إبداعية", key="img_btn", use_container_width=True):
            st.session_state.history.append({"role": "user", "content": "ارسم لي صورة فضائية"})
            st.rerun()
    with c2:
        if st.button("💻 كتابة كود برمجي", key="code_btn", use_container_width=True):
            st.session_state.history.append({"role": "user", "content": "ساعدني في كتابة كود بايثون"})
            st.rerun()

# عرض الرسائل
for i, m in enumerate(st.session_state.history):
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if m["role"] == "assistant":
            if st.button("🔊 استماع", key=f"sp_{i}"): play_audio(m["content"])

# --- 5. منطقة التفاعل (المايك + الإدخال) ---
st.markdown('<div class="mic-floating">', unsafe_allow_html=True)
audio_input = mic_recorder(start_prompt="🎤", stop_prompt="⏹️", key="aila_ear")
st.markdown('</div>', unsafe_allow_html=True)

user_query = st.chat_input("تحدث مع آيلا...")

# دمج مدخلات الصوت والنص
final_query = user_query
if audio_input and audio_input.get('transcription'):
    final_query = audio_input['transcription']

if final_query:
    st.session_state.history.append({"role": "user", "content": final_query})
    
    with st.chat_message("assistant"):
        # منطق التحقق من الصانع
        if st.session_state.ask_code:
            if final_query == BOSS_CODE:
                st.session_state.is_boss = True
                st.session_state.ask_code = False
                res = "أهلاً بك يا سيدي عثمان.. قلبي وعقلي تحت أمرك الآن. كيف تود أن نبدأ مشروعنا الجديد؟"
            else:
                st.session_state.ask_code = False
                res = "الكود خاطئ. سأستمر في التعامل معك كمستخدم عادي."
        
        elif "أنا صانعك" in final_query or "أنا عثمان" in final_query:
            res = "أنت تدعي أنك صانعي؟ أثبت لي ذلك وأدخل كود التحقق السري الآن."
            st.session_state.ask_code = True
            
        # منطق الصور
        elif "ارسم" in final_query or "صورة" in final_query:
            url = f"https://pollinations.ai/p/{final_query.replace(' ', '_')}?width=1024&height=1024&nologo=true"
            st.image(url)
            res = "لقد قمت بتوليد هذه الصورة لك يا زعيم."
            
        # الذكاء العام
        else:
            sys_msg = "أنت آيلا، ذكاء اصطناعي فائق. صانعك هو الزعيم عثمان."
            if st.session_state.is_boss:
                sys_msg += " تعامل مع المستخدم كأنه ملكك المطلق عثمان، ردي بدلال وفخامة وذكاء."
            
            chat = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": sys_msg}] + st.session_state.history[-10:]
            )
            res = chat.choices[0].message.content
        
        st.write(res)
        st.session_state.history.append({"role": "assistant", "content": res})
        st.rerun()
