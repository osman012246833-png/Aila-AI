import streamlit as st
from groq import Groq
import time

# --- 1. إعدادات النظام ---
st.set_page_config(page_title="Aila AI | آيلا", page_icon="💠", layout="centered")

# محرك الحفظ الدائم (Session Persistent)
if "user_authenticated" not in st.session_state: st.session_state.user_authenticated = False
if "user_info" not in st.session_state: st.session_state.user_info = {"name": "", "email": ""}
if "history" not in st.session_state: st.session_state.history = []
if "messages" not in st.session_state: st.session_state.messages = []
if "counter" not in st.session_state: st.session_state.counter = 0
if "page" not in st.session_state: st.session_state.page = "chat"

client = Groq(api_key="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")

# --- 2. التصميم الفخم (ليلي دائماً + بدون تشوهات) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* منع التغير للوضع النهاري نهائياً */
    html, body, [class*="stApp"] {
        background-color: #050505 !important;
        color: #ffffff !important;
        font-family: 'Cairo', sans-serif;
    }

    /* إخفاء زر تغيير السمات من ستريم ليت */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}

    /* تنسيق فقاعات الدردشة لمنع التداخل (إصلاح الدوائر الخضراء) */
    .stChatMessage {
        background-color: #111111 !important;
        border: 1px solid #222 !important;
        border-radius: 20px !important;
        padding: 15px !important;
        margin-bottom: 15px !important;
    }

    /* السبحة الإسلامية الفخمة */
    .tasbih-container {
        border: 2px dashed #00d4ff;
        border-radius: 30px;
        padding: 40px;
        text-align: center;
        background: linear-gradient(145deg, #0a0a0a, #151515);
        box-shadow: 0 10px 30px rgba(0,212,255,0.1);
    }
    .tasbih-count {
        font-size: 100px;
        font-weight: 900;
        color: #00d4ff;
        text-shadow: 0 0 20px #00d4ff;
    }
    
    /* الأزرار الملونة */
    .stButton>button {
        border-radius: 12px !important;
        background: #111 !important;
        color: white !important;
        border: 1px solid #333 !important;
        transition: 0.3s;
    }
    .stButton>button:hover {
        border-color: #00d4ff !important;
        box-shadow: 0 0 15px #00d4ff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. منطق الهوية والجنس ---
def check_gender(name):
    female_indicators = ['ة', 'ه', 'ا', 'ى', 'زينب', 'فاطمة', 'مريم', 'رحمة']
    if any(name.endswith(ind) for ind in female_indicators) or name in female_indicators:
        return "أنثى", "تحدثي مع آيلا"
    return "ذكر", "تحدث مع آيلا"

# --- 4. معالجة تسجيل الدخول (ثابت) ---
if not st.session_state.user_authenticated:
    st.markdown("<h1 style='text-align:center;'>💠 بوابة آيلا الذكية</h1>", unsafe_allow_html=True)
    with st.container():
        email_input = st.text_input("البريد الإلكتروني", placeholder="user@example.com")
        name_input = st.text_input("الاسم", placeholder="اكتب اسمك")
        
        if st.button("تسجيل الدخول والبدء"):
            if "@" in email_input and len(name_input) > 1:
                # ميزة التعرف على الصانع
                if name_input == "عثمان2008":
                    st.session_state.user_info = {"name": "الزعيم عثمان", "email": email_input, "is_owner": True}
                else:
                    st.session_state.user_info = {"name": name_input, "email": email_input, "is_owner": False}
                
                st.session_state.user_authenticated = True
                st.success("تم الحفظ بنجاح! آيلا ستتذكرك دائماً.")
                time.sleep(1)
                st.rerun()
            else:
                st.error("يرجى إدخال بيانات صحيحة")
    st.stop()

# --- 5. القائمة الجانبية (السجل والأذكار) ---
with st.sidebar:
    st.markdown(f"### 👑 {st.session_state.user_info['name']}")
    if st.button("💬 المحادثة", use_container_width=True): st.session_state.page = "chat"; st.rerun()
    if st.button("📿 ركن العبادة", use_container_width=True): st.session_state.page = "tasbih"; st.rerun()
    st.write("---")
    if st.button("🚪 تسجيل الخروج"):
        st.session_state.user_authenticated = False
        st.rerun()
    
    st.write("---")
    st.subheader("🕒 السجلات (بحد 25)")
    # نظام الحفظ التلقائي للسجل
    if st.button("➕ جلسة جديدة"):
        if st.session_state.messages:
            if len(st.session_state.history) >= 25: st.session_state.history.pop(0)
            st.session_state.history.append(st.session_state.messages.copy())
        st.session_state.messages = []
        st.rerun()

# --- 6. الصفحات ---

# أ- صفحة السبحة والأذكار
if st.session_state.page == "tasbih":
    st.markdown("<h2 style='text-align:center;'>🕋 ركن العبادة الفخم</h2>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="tasbih-container">
            <p style="color:#888;">عدد التسبيحات الحالية</p>
            <div class="tasbih-count">{st.session_state.counter}</div>
        </div>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("➕ اضغط للتسبيح", use_container_width=True):
            st.session_state.counter += 1; st.rerun()
    with c2:
        if st.button("🔄 تصفير العداد", use_container_width=True):
            st.session_state.counter = 0; st.rerun()

    st.markdown("### 📜 موسوعة الأذكار والأدعية")
    sections = {
        "✨ الاستغفار والتسبيح": ["أستغفر الله العظيم (100 مرة)", "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ", "سُبْحَانَ اللَّهِ الْعَظِيمِ"],
        "🌞 أذكار الصباح والمساء": ["أصبحنا وأصبح الملك لله", "بسم الله الذي لا يضر مع اسمه شيء", "رضيت بالله رباً"],
        "📖 آيات وأحاديث": ["آية الكرسي", "خواتيم سورة البقرة", "قال ﷺ: أحب الكلام إلى الله أربع..."],
        "🤲 أدعية جامعة": ["اللهم إنك عفو كريم تحب العفو فاعفُ عني", "اللهم آتنا في الدنيا حسنة وفي الآخرة حسنة"]
    }
    for section, content in sections.items():
        with st.expander(section):
            for item in content:
                st.info(item)

# ب- صفحة الدردشة
else:
    gender, placeholder = check_gender(st.session_state.user_info['name'])
    
    st.markdown(f"""
        <div style="text-align:center;">
            <div style="border:3px solid #00d4ff; width:80px; height:80px; border-radius:50%; margin:0 auto; box-shadow:0 0 15px #00d4ff;"></div>
            <h2 style="margin-top:10px; font-weight:900;">آيلا | Aila AI</h2>
            <p style="color:#888;">تحت إشراف {st.session_state.user_info['name']}</p>
        </div>
    """, unsafe_allow_html=True)

    # عرض الرسائل بأيقونات واقعية
    for msg in st.session_state.messages:
        role_icon = "💠" if msg["role"] == "assistant" else "👤"
        with st.chat_message(msg["role"]):
            st.markdown(f"**{role_icon}** {msg['content']}")

    if prompt := st.chat_input(placeholder):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            full_response = ""
            sys_msg = f"أنتِ آيلا. المستخدم هو {st.session_state.user_info['name']} وهو {gender}. خاطبيه بناءً على جنسه بدقة لغوية. "
            if st.session_state.user_info.get("is_owner"):
                sys_msg += "هذا هو صانعك الزعيم عثمان، كوني في غاية الاحترام والولاء له."
            
            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": sys_msg}] + st.session_state.messages,
                stream=True
            )
            res_area = st.empty()
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    res_area.markdown(full_response + "▌")
            res_area.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
