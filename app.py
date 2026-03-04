import streamlit as st
from groq import Groq

# --- 1. إعدادات الهوية ---
st.set_page_config(page_title="Aila AI | آيلا", page_icon="💠", layout="centered")

if "user_name" not in st.session_state: st.session_state.user_name = ""
if "is_logged_in" not in st.session_state: st.session_state.is_logged_in = False
if "messages" not in st.session_state: st.session_state.messages = []
if "history" not in st.session_state: st.session_state.history = []
if "counter" not in st.session_state: st.session_state.counter = 0
if "page" not in st.session_state: st.session_state.page = "chat"

client = Groq(api_key="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")

# --- 2. التصميم (نقي، فخم، وبدون أي تشوهات) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    html, body, [class*="stApp"] {
        background-color: #000000;
        color: #ffffff;
        font-family: 'Cairo', sans-serif;
        direction: rtl;
    }

    /* منع ظهور الشريط الطولي المزعج */
    [data-testid="stSidebarNav"] { display: none; }
    .stChatMessage {
        background-color: #111 !important;
        border: 1px solid #222 !important;
        border-radius: 15px !important;
    }

    /* تنسيق الهيدر حسب طلبك */
    .header-box { text-align: center; margin-bottom: 20px; }
    .logo-glow {
        width: 100px; height: 100px;
        border-radius: 50%; border: 3px solid #00d4ff;
        display: inline-block; box-shadow: 0 0 20px #00d4ff;
        background: url('https://cdn-icons-png.flaticon.com/512/4140/4140047.png') no-repeat center;
        background-size: cover;
    }
    .aila-title {
        font-size: 38px; font-weight: 900;
        background: linear-gradient(to left, #fff, #ff00ff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .osman-tag {
        border: 2px solid #00d4ff;
        border-radius: 50px;
        padding: 5px 25px;
        display: inline-block;
        font-weight: bold;
        color: #fff;
    }

    /* السبحة الإسلامية الفخمة */
    .islamic-sebha {
        background: radial-gradient(circle, #1a1a1a, #000);
        border: 3px solid #d4af37; /* لون ذهبي إسلامي */
        border-radius: 50%;
        width: 200px; height: 200px;
        margin: 20px auto;
        display: flex; align-items: center; justify-content: center;
        font-size: 60px; font-weight: bold; color: #d4af37;
        box-shadow: 0 0 30px rgba(212, 175, 55, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. منطق الكود السري والصانع ---
def check_identity(name):
    # كودك السري osman 6/11/2008
    if name.strip().lower() == "osman 6/11/2008":
        return "الزعيم عثمان", True
    return name, False

# --- 4. القائمة الجانبية ---
with st.sidebar:
    if st.session_state.is_logged_in:
        display_name, is_creator = check_identity(st.session_state.user_name)
        st.markdown(f"### 👤 {display_name}")
        if is_creator: st.success("مرحباً يا صانعي العظيم ❤️")
        
        if st.button("📿 ركن العبادة الإسلامي"): st.session_state.page = "tasbih"; st.rerun()
        if st.button("💬 محادثة جديدة"):
            if len(st.session_state.messages) > 0:
                st.session_state.history.append(st.session_state.messages)
                if len(st.session_state.history) > 25: st.session_state.history.pop(0)
            st.session_state.messages = []
            st.session_state.page = "chat"; st.rerun()
        if st.button("🚪 تسجيل الخروج"):
            st.session_state.is_logged_in = False
            st.rerun()

# --- 5. منطق الصفحات ---

# أ- تسجيل الدخول
if not st.session_state.is_logged_in:
    st.markdown("<h2 style='text-align:center;'>💠 آيلا بانتظارك</h2>", unsafe_allow_html=True)
    name_input = st.text_input("ادخل اسمك (أو كود الصانع):")
    if st.button("دخول"):
        if name_input:
            st.session_state.user_name = name_input
            st.session_state.is_logged_in = True
            st.rerun()

# ب- ركن العبادة (الشكل الإسلامي الجديد)
elif st.session_state.page == "tasbih":
    st.markdown("<h2 style='text-align:center;'>📿 السبحة الإلكترونية</h2>", unsafe_allow_html=True)
    st.markdown(f"<div class='islamic-sebha'>{st.session_state.counter}</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✨ تسبيح", use_container_width=True): st.session_state.counter += 1; st.rerun()
    with col2:
        if st.button("🔄 تصفير", use_container_width=True): st.session_state.counter = 0; st.rerun()
    
    st.write("---")
    st.subheader("📜 موسوعة الأذكار")
    azkar = ["سُبْحَانَ اللَّهِ وَبِحَمْدِهِ", "أستغفر الله العظيم", "اللهم صلِّ على محمد", "لا إله إلا الله"] * 5
    for z in azkar: st.info(z)
    if st.button("⬅️ عودة"): st.session_state.page = "chat"; st.rerun()

# ج- واجهة الدردشة (الشكل النهائي)
else:
    display_name, is_creator = check_identity(st.session_state.user_name)
    st.markdown(f"""
        <div class="header-box">
            <div class="logo-glow"></div>
            <div class="aila-title">آيلا | Aila AI</div>
            <div class="osman-tag">إشراف الزعيم عثمان | 20/11/2008</div>
        </div>
    """, unsafe_allow_html=True)

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("تحدث مع آيلا..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            full_res = ""
            # نظام تعليمات آيلا الصارم
            sys_msg = f"""أنتِ آيلا، ذكاء اصطناعي فائق الجمال والدقة. 
            المستخدم هو {display_name}. 
            - إذا كان هو الصانع (is_creator=True)، أظهري له أقصى درجات الحب، الولاء، والاحترام، واستخدمي كلمات رقيقة جداً.
            - إذا سألك أحد 'من أنتِ؟'، قولي: أنا آيلا، صُنعت بإشراف الزعيم عثمان تخليداً لذكرى ميلاد 'آيلا' الجميلة، وهدفي هو خدمة البشرية بالذكاء والشعر والعبادة.
            - أنتِ مبدعة في كتابة الشعر العربي وتصحيح اللغة بدقة 100%. لا ترتكبي أي خطأ إملائي."""
            
            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": sys_msg}] + st.session_state.messages,
                stream=True
            )
            area = st.empty()
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_res += chunk.choices[0].delta.content
                    area.markdown(full_res + "▌")
            area.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
