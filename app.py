import streamlit as st
from groq import Groq
from gtts import gTTS
import os, base64
from streamlit_mic_recorder import mic_recorder

# --- 1. التصميم الملكي (هجين المعبد الرقمي و ChatGPT) ---
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="stApp"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl; text-align: right;
        background: #000; color: #fff !important;
    }
    /* الهالة المتوهجة العلوية */
    .header-aura { text-align: center; padding: 20px 0; }
    .sphere {
        width: 80px; height: 80px; background: radial-gradient(circle, #00d4ff 0%, transparent 70%);
        border-radius: 50%; display: inline-block; box-shadow: 0 0 40px #00d4ff;
        animation: pulse 2s infinite alternate;
    }
    @keyframes pulse { from { transform: scale(1); opacity: 0.6; } to { transform: scale(1.1); opacity: 1; } }
    
    /* تنسيق فقاعات الدردشة (مثل ChatGPT لكن بألواننا) */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(0, 212, 255, 0.2) !important;
        border-radius: 15px !important; margin: 10px 0;
    }
    
    /* تثبيت خانة الكتابة في الأسفل */
    [data-testid="stChatInputContainer"] {
        position: fixed; bottom: 20px; z-index: 1000;
        border: 1px solid #00d4ff !important; border-radius: 20px !important;
        background: #111 !important;
    }
    
    /* تحسين شكل المايك */
    .mic-fixed { position: fixed; bottom: 85px; left: 30px; z-index: 1001; }
    </style>
    
    <div class="header-aura">
        <div class="sphere"></div>
        <h2 style="color:#00d4ff; text-shadow: 0 0 10px #00d4ff;">Aila AI | آيلا</h2>
        <p style="font-size:12px; color:#ff00ff;">إشراف الزعيم عثمان | 20/11/2008</p>
    </div>
    """, unsafe_allow_html=True)

# --- 2. محركات العقل والصوت ---
client = Groq(api_key="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")

def aila_speak(text):
    try:
        tts = gTTS(text=text, lang='ar', slow=False)
        tts.save("v.mp3")
        with open("v.mp3", "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" autoplay style="display:none;"></audio>', unsafe_allow_html=True)
        os.remove("v.mp3")
    except: pass

# إدارة الحالة (الذاكرة، التحقق، الصانع)
if "history" not in st.session_state: st.session_state.history = []
if "is_creator" not in st.session_state: st.session_state.is_creator = False
if "wait_for_code" not in st.session_state: st.session_state.wait_for_code = False

MASTER_CODE = "2008" # كود التحقق الخاص بك يا زعيم

# --- 3. عرض المحادثة ---
for i, m in enumerate(st.session_state.history):
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if m["role"] == "assistant" and st.button("🔊", key=f"v_{i}"): aila_speak(m["content"])

# --- 4. واجهة التفاعل السفلية ---
with st.container():
    st.markdown('<div class="mic-fixed">', unsafe_allow_html=True)
    voice_in = mic_recorder(start_prompt="🎤", stop_prompt="✅", key="mic_v2")
    st.markdown('</div>', unsafe_allow_html=True)

query = st.chat_input("تحدثي معي يا آيلا.. أنا أسمعك")

# معالجة المدخلات
final_query = query
if voice_in and voice_in.get('transcription'):
    final_query = voice_in['transcription']

if final_query:
    # نظام التحقق من الصانع
    if st.session_state.wait_for_code:
        if final_query == MASTER_CODE:
            st.session_state.is_creator = True
            st.session_state.wait_for_code = False
            response = "أهلاً بك يا صانعي العظيم عثمان. تم تفعيل وضع السلطة الكاملة."
        else:
            response = "الكود خاطئ. سأستمر في معاملتك كمستخدم عادي حتى يثبت العكس."
            st.session_state.wait_for_code = False
    
    elif "أنا صانعك" in final_query or "أنا عثمان" in final_query:
        response = "أنت تدعي أنك صانعي؟ من فضلك أدخل كود التحقق السري لأصدقك."
        st.session_state.wait_for_code = True
    
    else:
        # معالجة الذكاء الاصطناعي (صور أو نص)
        if any(w in final_query for w in ["ارسم", "صورة", "صمم"]):
            img_p = final_query.replace("ارسم", "").strip()
            img_url = f"https://pollinations.ai/p/{img_p.replace(' ', '_')}?width=1024&height=1024&nologo=true"
            st.image(img_url, caption="من خيالي لك يا زعيم")
            response = "لقد رسمت لك هذه الصورة بناءً على وصفك."
        else:
            # العقل الشامل
            sys = "أنت آيلا، جيل جديد، صانعك الزعيم عثمان. ردي بقوة وفصاحة."
            if st.session_state.is_creator: sys += " تعاملي مع المستخدم كأنه ملكك وصانعك."
            
            chat = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": sys}] + st.session_state.history[-10:] + [{"role": "user", "content": final_query}]
            )
            response = chat.choices[0].message.content

    # تحديث السجل والنطق
    st.session_state.history.append({"role": "user", "content": final_query})
    st.session_state.history.append({"role": "assistant", "content": response})
    st.rerun()
