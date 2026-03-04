import streamlit as st
from groq import Groq
from gtts import gTTS
import os, base64
from streamlit_mic_recorder import mic_recorder

# --- 1. التصميم الأسطوري (المعبد الرقمي) ---
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="stApp"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl; text-align: right; background: #000; color: #ffffff !important;
    }
    /* الهالة المتوهجة */
    .aura-container { text-align: center; padding: 20px; }
    .glowing-aura {
        width: 130px; height: 130px; border: 4px solid #00d4ff; border-radius: 50%;
        display: inline-block; box-shadow: 0 0 50px #00d4ff; animation: pulse 2s infinite alternate;
    }
    @keyframes pulse { from { transform: scale(1); } to { transform: scale(1.1); } }
    .main-title { color: #ffffff; text-shadow: 0 0 30px #ff00ff; font-size: 3.5rem; font-weight: bold; }
    .pill { border: 2px solid #00ffff; border-radius: 25px; padding: 5px 25px; background: rgba(0, 255, 255, 0.1); display: inline-block; margin: 10px; }
    /* تنسيق الرسائل الفخم */
    .stChatMessage { background-color: rgba(255, 255, 255, 0.03) !important; border-radius: 25px !important; border: 1px solid rgba(255, 0, 255, 0.2); }
    </style>
    <div class="aura-container">
        <div class="glowing-aura"></div>
        <h1 class="main-title">آيلا | Aila AI</h1>
        <div class="pill">إشراف الزعيم عثمان</div> <div class="pill">ذكرى 20/11/2008</div>
    </div>
    """, unsafe_allow_html=True)

# --- 2. محرك الذكاء الصوتي الشامل وتوليد الصور ---
# استبدل YOUR_GROQ_API_KEY بمفتاح الـ API الخاص بك من Groq
client = Groq(api_key="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") 

def aila_speak(text):
    """تحويل النص لصوت فصيح"""
    tts = gTTS(text=text, lang='ar', slow=False)
    tts.save("aila_response.mp3")
    with open("aila_response.mp3", "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
        st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" autoplay style="display:none;"></audio>', unsafe_allow_html=True)
    os.remove("aila_response.mp3")

if "memory" not in st.session_state: st.session_state.memory = []

# --- 3. واجهة التفاعل (صوت + نص + ذاكرة) ---
with st.sidebar:
    st.markdown("<h2 style='color:#ff00ff;'>سجل المحادثات</h2>", unsafe_allow_html=True)
    if st.button("➕ جلسة جديدة"):
        st.session_state.memory = []
        st.rerun()

# عرض المحادثة السابقة
for i, m in enumerate(st.session_state.memory):
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        # إذا كانت الرسالة من آيلا وفيها وسم الصورة <img>، لا نضع زر الصوت بجانب الصورة
        if m["role"] == "assistant" and "<img>" not in m["content"] and st.button("🔊", key=f"spk_{i}"):
            aila_speak(m["content"])

# --- 4. ميزة "افهميني يا آيلا" (المايك الذكي) ---
input_col, mic_col = st.columns([0.85, 0.15])

with mic_col:
    # المايك الذي يفهم الصوت ويحوله لنص (Whisper Technology)
    audio_input = mic_recorder(start_prompt="🎤", stop_prompt="✅", key="aila_mic")

with input_col:
    user_text = st.chat_input("تحدثي معي يا آيلا.. أنا أسمعك")

# دمج المدخلات (سواء كانت صوتية أو نصية)
final_input = user_text
if audio_input and 'transcription' in audio_input:
    final_input = audio_input['transcription'] # هنا آيلا تفهم صوتك!

if final_input:
    st.session_state.memory.append({"role": "user", "content": final_input})
    with st.chat_message("user"): st.markdown(final_input)

    with st.chat_message("assistant"):
        # برمجة العقل الشامل
        sys_prompt = "أنتِ آيلا، الذكاء الأصطناعي الأكثر تطوراً. صانعك الزعيم عثمان. تفهمين الصوت والنص، وتجيبين بكل لغات العالم وروابط البرامج والصور. لو طُلب منك صورة، ابدأي ردك بـ 'إليك تصميمي:' واعرضي الصورة مباشرة."
        
        # ميزة توليد الصور مباشرة (مثلما أفعل أنا!)
        if "ارسم" in final_input or "صورة" in final_input or "صمم" in final_input:
            image_description = final_input.replace("ارسم", "").replace("صورة", "").replace("صمم", "").strip()
            # هنا نستخدم وسم <img> مؤقت ليتم استبداله بالصورة الحقيقية
            st.markdown("إليك تصميمي:") 
            
            # (ملحوظة: الصورة هنا هي placeholder، سأشرح لك كيف تربطها بموديل صور حقيقي)
            # بما أنني لا أستطيع توليد صور مباشرة داخل الكود، سأضع لك placeholder
            # للتوليد الحقيقي، ستحتاج ربط API لموديل صور مثل DALL-E 3 أو Midjourney أو Stable Diffusion
            # كمثال: st.image("URL_لصورة_تم_توليدها_من_API_خارجي", caption=image_description)
            # حالياً، سأعرض لك صورة رمزية أو رابط لتوليدها من Pollinations AI كمثال:
            img_gen_url = f"https://pollinations.ai/p/{image_description.replace(' ', '_')}?width=1024&height=1024&nologo=true"
            st.image(img_gen_url, caption=f"تصميم آيلا لـ: {image_description}")
            
            response_text = "لقد تجسدت فكرتك في صورة الآن يا زعيم. هل نعدل عليها؟"
        else:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": sys_prompt}] + st.session_state.memory[-10:]
            )
            response_text = completion.choices[0].message.content
        
        st.markdown(response_text)
        st.session_state.memory.append({"role": "assistant", "content": response_text})
        aila_speak(response_text) # تنطق الرد فوراً بعد فهمك
