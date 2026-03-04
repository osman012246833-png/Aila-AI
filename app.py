import streamlit as st
from groq import Groq

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="centered")

# --- 2. إدارة الحالة ---
if "messages" not in st.session_state: st.session_state.messages = []
if "history" not in st.session_state: st.session_state.history = []
if "counter" not in st.session_state: st.session_state.counter = 0
if "page" not in st.session_state: st.session_state.page = "login"
if "is_loyal" not in st.session_state: st.session_state.is_loyal = False
if "user_name" not in st.session_state: st.session_state.user_name = ""

client = Groq(api_key="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")

# --- 3. التنسيق البرمجي (إصلاح تداخل الشاشة وتصغير الخط) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;800&display=swap');
    
    html, body, [class*="stApp"] {
        background-color: #000000;
        color: #ffffff;
        font-family: 'Cairo', sans-serif;
        direction: rtl;
    }

    /* إصلاح الهيدر */
    .header-container { text-align: center; margin-top: -40px; }
    .logo-circle {
        width: 110px; height: 110px;
        border-radius: 50%;
        border: 3px solid #00d4ff;
        display: inline-block;
        box-shadow: 0 0 15px #00d4ff;
    }
    .aila-title {
        font-size: 35px; font-weight: 800;
        background: linear-gradient(to right, #ffffff, #ff00ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .info-bar {
        border: 1.5px solid #00d4ff;
        border-radius: 30px;
        padding: 4px 20px;
        font-size: 14px;
        display: inline-block;
    }

    /* تصغير خط الكتابة والرسائل (مثل حجم خط الشات العادي) */
    .stChatMessage p, div[data-testid="stMarkdownContainer"] p {
        font-size: 16px !important;
        line-height: 1.5;
    }
    
    /* منع التداخل الطولي للسبحة */
    .tasbih-box {
        border: 5px solid #00d4ff;
        border-radius: 50%;
        width: 160px; height: 160px;
        margin: 10px auto;
        display: flex; align-items: center; justify-content: center;
        font-size: 50px; font-weight: bold;
        background: #000;
    }
    
    .zkr-card {
        background: #111;
        border-right: 3px solid #00d4ff;
        padding: 10px;
        margin-bottom: 5px;
        font-size: 15px;
        border-radius: 8px;
    }

    /* إخفاء أي عناصر تسبب تشوه عمودي */
    button[kind="secondary"] { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. القائمة الجانبية (نظام السجل والعبادة) ---
with st.sidebar:
    st.markdown(f"### 👑 {st.session_state.user_name}")
    if st.button("💬 محادثة جديدة", use_container_width=True):
        if st.session_state.messages:
            st.session_state.history.append(st.session_state.messages.copy())
        st.session_state.messages = []
        st.session_state.page = "chat"
        st.rerun()
    
    if st.button("📿 ركن الأذكار", use_container_width=True):
        st.session_state.page = "tasbih"
        st.rerun()
    
    st.write("---")
    st.subheader("🕒 السجل")
    for i, old_chat in enumerate(reversed(st.session_state.history)):
        if st.button(f"سجل {len(st.session_state.history)-i}", key=f"h_{i}", use_container_width=True):
            st.session_state.messages = old_chat
            st.session_state.page = "chat"
            st.rerun()

# --- 5. منطق الصفحات ---

# أ- صفحة الدخول
if st.session_state.page == "login":
    st.markdown("<h2 style='text-align:center;'>💠 دخول عالم آيلا</h2>", unsafe_allow_html=True)
    val = st.text_input("ادخل اسمك", placeholder="أو كود الصانع...")
    if st.button("دخول للنظام"):
        if val == "عثمان2008":
            st.session_state.user_name = "الزعيم عثمان"
            st.session_state.is_loyal = True
        else:
            st.session_state.user_name = val
        st.session_state.page = "chat"
        st.rerun()

# ب- صفحة السبحة (تم إصلاح التشوه)
elif st.session_state.page == "tasbih":
    st.markdown("<h3 style='text-align:center;'>📿 العداد والأذكار</h3>", unsafe_allow_html=True)
    st.markdown(f'<div class="tasbih-box">{st.session_state.counter}</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("➕ تسبيح", use_container_width=True):
            st.session_state.counter += 1
            st.rerun()
    with c2:
        if st.button("🔄 تصفير سريع", use_container_width=True):
            st.session_state.counter = 0
            st.rerun()
    
    st.write("---")
    st.subheader("📜 قائمة الأذكار الكبرى")
    azkar_big_list = [
        "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ ، سُبْحَانَ اللَّهِ الْعَظِيمِ",
        "لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ",
        "أستغفر الله العظيم وأتوب إليه (100 مرة)",
        "اللهم صلِّ وسلم على نبينا محمد (صلى الله عليه وسلم)",
        "لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ الْعَلِيِّ الْعَظِيمِ",
        "لا إله إلا أنت سبحانك إني كنت من الظالمين",
        "أصبحنا وأصبح الملك لله، والحمد لله، لا إله إلا الله",
        "اللهم بك أصبحنا، وبك أمسينا، وبك نحيا، وبك نموت",
        "حسبي الله لا إله إلا هو عليه توكلت وهو رب العرش العظيم",
        "بسم الله الذي لا يضر مع اسمه شيء في الأرض ولا في السماء",
        "اللهم إني أسألك العفو والعافية في الدنيا والآخرة",
        "يا حي يا قيوم برحمتك أستغيث أصلح لي شأني كله",
        "سبحان الله (33)، الحمد لله (33)، الله أكبر (34)",
        "اللهم إني أعوذ بك من الهم والحزن، والعجز والكسل",
        "رضيت بالله رباً وبالإسلام ديناً وبمحمد نبياً",
        "اللهم آتنا في الدنيا حسنة وفي الآخرة حسنة وقنا عذاب النار"
    ]
    for z in azkar_big_list:
        st.markdown(f'<div class="zkr-card">{z}</div>', unsafe_allow_html=True)
    
    if st.button("⬅️ عودة للدردشة"):
        st.session_state.page = "chat"
        st.rerun()

# ج- صفحة الدردشة
else:
    st.markdown(f"""
        <div class="header-container">
            <div class="logo-circle"></div>
            <div class="aila-title">آيلا | Aila AI</div>
            <div class="info-bar">إشراف الزعيم عثمان | 20/11/2008</div>
        </div>
    """, unsafe_allow_html=True)

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("تحدثي معي يا آيلا..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ""
            
            if st.session_state.is_loyal:
                sys_msg = f"أنتِ آيلا، رفيقة الزعيم عثمان المخلصة جداً. تخاطبينه بحب وتقدير وتنفذين أوامره بكل مودة. أسلوبك رقيق وفخم."
            else:
                sys_msg = "أنتِ آيلا، مساعدة ذكية ومحترمة."

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
