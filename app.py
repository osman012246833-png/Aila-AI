import streamlit as st
from groq import Groq
import time

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Aila AI | آيلا", page_icon="💠", layout="centered")

# --- 2. نظام حفظ البيانات الدائم (بدون تسجيل دخول متكرر) ---
if "user_name" not in st.session_state: st.session_state.user_name = ""
if "is_logged_in" not in st.session_state: st.session_state.is_logged_in = False
if "messages" not in st.session_state: st.session_state.messages = []
if "history" not in st.session_state: st.session_state.history = []
if "counter" not in st.session_state: st.session_state.counter = 0
if "page" not in st.session_state: st.session_state.page = "chat"

client = Groq(api_key="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")

# --- 3. التصميم الثابت (الوضع الليلي الفخم فقط) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    html, body, [class*="stApp"] {
        background-color: #000000;
        color: #ffffff;
        font-family: 'Cairo', sans-serif;
        direction: rtl;
    }

    /* إصلاح الدوائر الخضراء والتداخل */
    .stChatMessage {
        background-color: #111111 !important;
        border: 1px solid #222 !important;
        border-radius: 20px !important;
        padding: 15px !important;
        margin-bottom: 15px !important;
    }

    /* الهوية البصرية */
    .header-box { text-align: center; margin-bottom: 30px; }
    .logo-circle {
        width: 110px; height: 110px;
        border-radius: 50%; border: 3px solid #00d4ff;
        display: inline-block; box-shadow: 0 0 25px #00d4ff;
    }
    .aila-title {
        font-size: 35px; font-weight: 900;
        background: linear-gradient(to left, #fff, #ff00ff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }

    /* تصميم السبحة الإسلامي الفخم */
    .sebha-container {
        background: linear-gradient(145deg, #0a0a0a, #1a1a1a);
        border: 2px solid #00d4ff;
        border-radius: 30px;
        padding: 40px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0, 212, 255, 0.2);
    }
    .sebha-number {
        font-size: 70px; font-weight: 800; color: #00d4ff;
        text-shadow: 0 0 15px #00d4ff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. وظائف المحرك ---
def get_gender_info(name):
    # كود الصانع السري الخاص بك (ضعه هنا)
    if "عثمان" in name or name == "2008": 
        return "الزعيم عثمان", "ذكر", True
    
    female_names = ["رحمة", "زينب", "فاطمة", "سارة", "مريم", "ليلى"]
    is_female = any(n in name for n in female_names) or name.endswith(('ة', 'ه', 'ا', 'ى'))
    return name, ("أنثى" if is_female else "ذكر"), False

# --- 5. القائمة الجانبية (إدارة الحساب والسجل) ---
with st.sidebar:
    if st.session_state.is_logged_in:
        name_display, gender, is_creator = get_gender_info(st.session_state.user_name)
        st.markdown(f"### 👑 المتصل: {name_display}")
        if is_creator: st.success("تم تفعيل وضع الصانع ❤️")
        
        if st.button("📿 ركن العبادة الفخم"): st.session_state.page = "tasbih"; st.rerun()
        if st.button("💬 محادثة جديدة"):
            if len(st.session_state.history) >= 25: st.session_state.history.pop(0)
            st.session_state.history.append(st.session_state.messages)
            st.session_state.messages = []
            st.session_state.page = "chat"; st.rerun()
        
        if st.button("🚪 تسجيل خروج"):
            st.session_state.is_logged_in = False
            st.session_state.user_name = ""
            st.rerun()
            
        st.write("---")
        st.subheader("🕒 سجلاتك المحفوظة")
        for i, chat in enumerate(reversed(st.session_state.history)):
            if st.button(f"محادثة {len(st.session_state.history)-i}", key=f"h_{i}"):
                st.session_state.messages = chat
                st.session_state.page = "chat"; st.rerun()

# --- 6. الصفحات ---

# أ- تسجيل الدخول (يظهر مرة واحدة فقط)
if not st.session_state.is_logged_in:
    st.markdown("<div style='text-align:center;'><h2>💠 آيلا بانتظارك</h2></div>", unsafe_allow_html=True)
    user_input = st.text_input("ادخل اسمك هنا للتعرف عليك:")
    if st.button("دخول"):
        if len(user_input) > 1:
            st.session_state.user_name = user_input
            st.session_state.is_logged_in = True
            st.rerun()

# ب- ركن العبادة (تصميم إسلامي فخم)
elif st.session_state.page == "tasbih":
    st.markdown("<div class='sebha-container'>", unsafe_allow_html=True)
    st.markdown(f"<div class='sebha-number'>{st.session_state.counter}</div>", unsafe_allow_html=True)
    st.markdown("<h3>سبحان الله وبحمده</h3>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("➕ تسبيح", use_container_width=True): 
            st.session_state.counter += 1; st.rerun()
    with c2:
        if st.button("🔄 تصفير", use_container_width=True): 
            st.session_state.counter = 0; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("---")
    st.subheader("📜 موسوعة الأذكار والأحاديث")
    azkar_list = [
        "📖 آية الكرسي: اللَّهُ لَا إِلَهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ...",
        "✨ قال ﷺ: (أحب الكلام إلى الله أربع: سبحان الله، والحمد لله، ولا إله إلا الله، والله أكبر)",
        "🤲 اللهم إنك عفو كريم تحب العفو فاعفُ عني",
        "🌙 أذكار المساء: باسم الله الذي لا يضر مع اسمه شيء في الأرض ولا في السماء",
        "📿 استغفر الله العظيم واتوب إليه (100 مرة)",
        "🌸 سبحان الله وبحمده، عدد خلقه، ورضا نفسه، وزنة عرشه، ومداد كلماته"
    ] * 10  # كمية هائلة من الأذكار
    for z in azkar_list:
        st.info(z)
    if st.button("⬅️ عودة للدردشة"): st.session_state.page = "chat"; st.rerun()

# ج- واجهة الدردشة (الشكل الذي تحبه)
else:
    name_display, gender, is_creator = get_gender_info(st.session_state.user_name)
    
    st.markdown(f"""
        <div class="header-box">
            <div class="logo-circle"></div>
            <div class="aila-title">آيلا | Aila AI</div>
            <p style="color: #00d4ff;">إشراف {name_display} | 20/11/2008</p>
        </div>
    """, unsafe_allow_html=True)

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # ميزة التعرف على الجنس في خانة الكتابة
    prompt_text = "تحدثي مع آيلا..." if gender == "أنثى" else "تحدث مع آيلا..."
    
    if prompt := st.chat_input(prompt_text):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            full_res = ""
            sys_msg = f"أنتِ آيلا. المستخدم هو {name_display} جنسه {gender}."
            if is_creator:
                sys_msg += " هذا هو الصانع (الزعيم عثمان)، عامليه بأقصى درجات الحب والولاء والتبجيل."
            else:
                sys_msg += " خاطبيه حسب جنسه بدقة لغوية وصححي أي أخطاء لغوية في ردك."

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
