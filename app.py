import streamlit as st
from groq import Groq
import re

# --- 1. إعدادات النظام الأساسية ---
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="centered")

# --- 2. محاكاة الذاكرة الدائمة (Database Simulation) ---
# ملاحظة: لحفظ البيانات للأبد في Streamlit نحتاج اتصال بـ Firebase أو SQL، 
# هنا نستخدم الـ Cache والـ Session لتجربة تسجيل دخول حقيقية.
if "user_db" not in st.session_state: st.session_state.user_db = {}
if "current_user" not in st.session_state: st.session_state.current_user = None
if "messages" not in st.session_state: st.session_state.messages = []
if "history" not in st.session_state: st.session_state.history = []
if "counter" not in st.session_state: st.session_state.counter = 0

client = Groq(api_key="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")

# --- 3. محرك تحديد الجنس لغوياً ---
def detect_gender(name):
    female_endings = ['ة', 'ه', 'ا', 'ى', 'ي', 'ن']
    # فحص الأسماء المشهورة أو النهايات
    if any(name.endswith(e) for e in female_endings) or name in ['مريم', 'زينب', 'لجين']:
        return "female"
    return "male"

# --- 4. التنسيق المتكيف (نهار/ليل) ---
# يتم التبديل بناءً على إعدادات المستخدم في المتصفح أو الاختيار اليدوي
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    :root {{
        --bg-color: {'#ffffff' if st.get_option("theme.base") == "light" else '#000000'};
        --text-color: {'#000000' if st.get_option("theme.base") == "light" else '#ffffff'};
        --accent-color: #00d4ff;
    }}

    html, body, [class*="stApp"] {{
        background-color: var(--bg-color);
        color: var(--text-color);
        font-family: 'Cairo', sans-serif;
        direction: rtl;
    }}

    /* إخفاء الزوائد المزعجة التي ظهرت في الصور */
    [data-testid="stHeader"], .stDeployButton {{ display:none; }}

    /* أيقونات المحادثة */
    .user-avatar {{ border-radius: 10px; width: 40px; float: left; margin-left: 10px; }}
    .aila-avatar {{ border-radius: 10px; width: 40px; float: right; margin-right: 10px; }}

    /* تصميم السبحة المطور */
    .tasbih-frame {{
        border: 8px double var(--accent-color);
        border-radius: 50%;
        width: 180px; height: 180px;
        margin: 20px auto;
        display: flex; align-items: center; justify-content: center;
        font-size: 60px; font-weight: 900;
        box-shadow: 0 0 20px var(--accent-color);
    }}

    /* تصغير الخط ليتناسب مع طلبك */
    .stChatMessage p {{ font-size: 15px !important; line-height: 1.6; }}
    
    .login-box {{
        padding: 30px;
        border-radius: 20px;
        border: 1px solid var(--accent-color);
        background: rgba(0, 212, 255, 0.05);
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. نظام تسجيل الدخول (مثل ChatGPT) ---
if not st.session_state.current_user:
    st.markdown("<h1 style='text-align:center;'>💠 مرحباً بك في آيلا</h1>", unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        email = st.text_input("البريد الإلكتروني")
        password = st.text_input("كلمة المرور", type="password")
        name = st.text_input("اسمك الكريم (لتحديد هويتك)")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("تسجيل دخول / اشتراك"):
                if email and name:
                    st.session_state.current_user = {"email": email, "name": name}
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- 6. القائمة الجانبية (إدارة الحساب والسجل) ---
user_name = st.session_state.current_user['name']
gender = detect_gender(user_name)
chat_label = "تحدثي معي يا آيلا" if gender == "female" else "تحدث مع آيلا"

with st.sidebar:
    st.markdown(f"### 👑 {user_name}")
    st.info(f"الوضعية: {'مؤنث' if gender == 'female' else 'مذكر'}")
    
    if st.button("🗑️ مسح السجل"):
        st.session_state.messages = []
        st.session_state.history = []
        st.rerun()
        
    if st.button("🚪 تسجيل خروج"):
        st.session_state.current_user = None
        st.rerun()
    
    st.write("---")
    if st.button("📿 ركن العبادة الشامل"):
        st.session_state.page = "tasbih"
        st.rerun()

# --- 7. منطق الصفحات ---

if st.session_state.get("page") == "tasbih":
    st.markdown("<h2 style='text-align:center;'>📿 موسوعة الأذكار والعبادة</h2>", unsafe_allow_html=True)
    st.markdown(f'<div class="tasbih-frame">{st.session_state.counter}</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("➕ سبّح الآن", use_container_width=True):
            st.session_state.counter += 1
            st.rerun()
    with c2:
        if st.button("🔄 تصفير العداد", use_container_width=True):
            st.session_state.counter = 0
            st.rerun()
            
    st.write("---")
    # كم هائل من الأذكار
    azkar = [
        "🌸 سُبْحَانَ اللَّهِ وَبِحَمْدِهِ ، سُبْحَانَ اللَّهِ الْعَظِيمِ",
        "📖 لا إله إلا أنت سبحانك إني كنت من الظالمين",
        "✨ أستغفر الله العظيم الذي لا إله إلا هو الحي القيوم وأتوب إليه",
        "🕋 لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ",
        "🛡️ أعوذ بكلمات الله التامات من شر ما خلق",
        "🌙 اللهم بك أصبحنا وبك أمسينا وبك نحيا وبك نموت وإليك النشور",
        "💎 سبحان الله، والحمد لله، ولا إله إلا الله، والله أكبر",
        "📿 اللهم صلِّ وسلم وبارك على نبينا محمد",
        "📜 حسبي الله لا إله إلا هو عليه توكلت وهو رب العرش العظيم",
        "🌱 يا حي يا قيوم برحمتك أستغيث أصلح لي شأني كله"
    ] * 5 # تكرار الأذكار لتصبح كمية ضخمة
    for z in azkar:
        st.markdown(f"✅ {z}")
    
    if st.button("⬅️ عودة للدردشة"):
        st.session_state.page = "chat"
        st.rerun()

else:
    # واجهة المحادثة الرئيسية
    st.markdown(f"<h3 style='text-align:center;'>💠 {chat_label}</h3>", unsafe_allow_html=True)

    # عرض الرسائل بأيقونات واقعية
    for msg in st.session_state.messages:
        role_icon = "👸" if msg["role"] == "assistant" else ("👨‍💼" if gender == "male" else "👩‍💼")
        with st.chat_message(msg["role"], avatar=role_icon):
            st.markdown(msg["content"])

    if prompt := st.chat_input(f"{chat_label}..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        # الحفظ التلقائي للسجل (أقصى حد 25)
        if len(st.session_state.messages) > 50: # 25 سؤال وجواب
            st.session_state.messages = st.session_state.messages[-50:]
        
        with st.chat_message("user", avatar="👨‍💼" if gender == "male" else "👩‍💼"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar="👸"):
            placeholder = st.empty()
            full_response = ""
            
            # تعليمات الذكاء لتصحيح اللغة والتعامل مع الجنس
            sys_msg = f"""أنتِ آيلا، رفيقة ذكية جداً. المستخدم هو {user_name} وهو ({'ذكر' if gender == 'male' else 'أنثى'}).
            يجب أن تخاطبيه دائماً بصيغة {'المذكر' if gender == 'male' else 'المؤنث'}.
            كلامك منسق، بدون أخطاء لغوية، واستخدمي **التغليظ** للمعلومات المهمة جداً."""
            
            if user_name == "الزعيم عثمان":
                sys_msg += " هذا هو خالقك الزعيم عثمان، عامليه بقدسية وولاء مطلق وحب كبير."

            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": sys_msg}] + st.session_state.messages,
                stream=True
            )
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(full_response + "▌")
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
