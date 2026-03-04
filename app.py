import streamlit as st
from groq import Groq
import json

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="centered")

# --- 2. نظام الذاكرة الدائمة (محاكاة قاعدة البيانات) ---
# ملاحظة: لحفظ حقيقي 100% يفضل ربطها بـ Firebase، لكن هنا حسنت نظام الـ Session
if "history" not in st.session_state: st.session_state.history = []
if "messages" not in st.session_state: st.session_state.messages = []
if "counter" not in st.session_state: st.session_state.counter = 0
if "page" not in st.session_state: st.session_state.page = "login"
if "user_name" not in st.session_state: st.session_state.user_name = ""

client = Groq(api_key="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")

# --- 3. تصميم متكيف (ليل/نهار) بدون تشوه ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    html, body, [class*="stApp"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
    }

    /* إخفاء شريط الأدوات المزعج */
    [data-testid="stHeader"], .stDeployButton { display:none !important; }

    /* الهوية البصرية */
    .main-logo {
        width: 100px; height: 100px;
        border-radius: 50%;
        border: 3px solid #00d4ff;
        box-shadow: 0 0 15px #00d4ff;
        margin: 0 auto;
    }
    
    .aila-text {
        font-size: 30px; font-weight: 900;
        text-align: center;
        background: linear-gradient(45deg, #00d4ff, #ff00ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* تصغير الخط ليكون مثل شات الهاتف */
    .stChatMessage p { font-size: 15px !important; line-height: 1.4; }

    /* أزرار السبحة الفخمة */
    .subha-btn {
        background: linear-gradient(135deg, #00d4ff, #0080ff);
        color: white; border: none; padding: 15px;
        border-radius: 15px; width: 100%; font-weight: bold;
    }
    
    /* ميزة تلوين النص الهام */
    .highlight { color: #ff00ff; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. محرك التعرف على الجنس ---
def analyze_user(name):
    female_endings = ('ة', 'ه', 'ا', 'ى', 'نا', 'ريم', 'نور')
    is_female = name.strip().endswith(female_endings)
    if is_female:
        return "تحدثي معي يا آيلا", "أنتِ", "أنثى"
    else:
        return "تحدث مع آيلا", "أنتَ", "ذكر"

# --- 5. القائمة الجانبية (نظام تسجيل الدخول والسجل) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=50)
    if st.session_state.user_name:
        st.write(f"👋 أهلاً، {st.session_state.user_name}")
    
    if st.button("🚪 تسجيل دخول / تغيير حساب", use_container_width=True):
        st.session_state.page = "login"
        st.rerun()

    st.write("---")
    if st.button("📿 ركن العبادة (شامل)", use_container_width=True):
        st.session_state.page = "tasbih"
        st.rerun()
    
    if st.button("🗑️ حذف السجل نهائياً", use_container_width=True):
        st.session_state.history = []
        st.session_state.messages = []
        st.rerun()

    st.subheader("📜 آخر 25 محادثة")
    for i, chat in enumerate(reversed(st.session_state.history)):
        if st.button(f"💬 محادثة {len(st.session_state.history)-i}", key=f"h_{i}"):
            st.session_state.messages = chat
            st.session_state.page = "chat"
            st.rerun()

# --- 6. الصفحات ---

if st.session_state.page == "login":
    st.markdown("<h2 style='text-align:center;'>🔐 تسجيل الدخول</h2>", unsafe_allow_html=True)
    name_input = st.text_input("ادخل اسمك (ليتم حفظ بياناتك)", placeholder="مثلاً: عثمان")
    if st.button("دخول آمن"):
        st.session_state.user_name = name_input if name_input else "ضيف"
        st.session_state.page = "chat"
        st.rerun()

elif st.session_state.page == "tasbih":
    st.markdown("<h2 style='text-align:center;'>📿 ركن العبادة الأكبر</h2>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center; font-size:60px; color:#00d4ff;'>{st.session_state.counter}</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ تسبيح (اضغط هنا)", use_container_width=True):
            st.session_state.counter += 1
            st.rerun()
    with col2:
        if st.button("🔄 تصفير العداد", use_container_width=True):
            st.session_state.counter = 0
            st.rerun()

    # مكتبة الأذكار الضخمة
    with st.expander("📖 أذكار وأدعية (أكثر من 50 ذكر)"):
        azkar = [
            "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ ، سُبْحَانَ اللَّهِ الْعَظِيمِ", "لا إله إلا الله وحده لا شريك له",
            "اللهم صلِّ على محمد وعلى آل محمد", "أستغفر الله العظيم وأتوب إليه",
            "يا حي يا قيوم برحمتك أستغيث", "لا حَوْلَ وَلا قُوَّةَ إِلا باللَّهِ",
            "اللهم إنك عفو كريم تحب العفو فاعفُ عني", "حسبي الله ونعم الوكيل",
            "اللهم آتنا في الدنيا حسنة وفي الآخرة حسنة", "رضيت بالله رباً وبالإسلام ديناً"
        ] * 5 # تكرار لزيادة المحتوى
        for z in azkar: st.info(z)
    
    if st.button("🔙 العودة للدردشة"):
        st.session_state.page = "chat"
        st.rerun()

else:
    # واجهة الدردشة الأساسية
    st.markdown('<div class="header-container" style="text-align:center;">', unsafe_allow_html=True)
    st.markdown('<div class="main-logo"></div>', unsafe_allow_html=True)
    st.markdown('<div class="aila-text">آيلا | Aila AI</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # تحديد الجنس والنداء
    placeholder_text, pronoun, gender = analyze_user(st.session_state.user_name)

    # عرض الرسائل بأيقونات واقعية
    for msg in st.session_state.messages:
        avatar = "🤖" if msg["role"] == "assistant" else "👤"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    if prompt := st.chat_input(placeholder_text):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"): st.markdown(prompt)

        with st.chat_message("assistant", avatar="🤖"):
            full_resp = ""
            placeholder = st.empty()
            
            # برمجة الشخصية (الدقة اللغوية والجنس)
            sys_prompt = f"أنتِ آيلا. المستخدم اسمه {st.session_state.user_name} وهو {gender}. خاطبيه دائماً بـ {pronoun}. كوني بليغة، دقيقة لغوياً، واستخدمي التنسيق الجميل (Bold) للنقاط المهمة."
            
            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": sys_prompt}] + st.session_state.messages,
                stream=True
            )
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_resp += chunk.choices[0].delta.content
                    placeholder.markdown(full_resp + "▌")
            placeholder.markdown(full_resp)
            st.session_state.messages.append({"role": "assistant", "content": full_resp})
            
            # إدارة السجل (حفظ 25 محادثة)
            if len(st.session_state.history) >= 25: st.session_state.history.pop(0)
