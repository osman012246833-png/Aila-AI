import streamlit as st
from groq import Groq

# --- 1. إعدادات الصفحة والتنسيق الفخم ---
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stSidebar"], [data-testid="stSidebarNav"] { display: none !important; }
    html, body, [class*="stApp"] { background-color: #000000; color: #ffffff; font-family: 'Cairo', sans-serif; direction: rtl; }
    
    .aila-gradient-title {
        font-size: 45px; font-weight: 900;
        background: linear-gradient(to right, #ffffff, #ff00ff, #ffffff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 5px; text-align: center;
    }
    
    .osman-tag {
        border: 1.5px solid #00d4ff; border-radius: 50px;
        padding: 4px 20px; display: inline-block;
        font-size: 14px; color: #ffffff;
        background: rgba(0, 212, 255, 0.1);
    }
    
    .support-footer {
        font-size: 13px; color: #ff00ff; font-weight: bold;
        text-align: center; border-top: 1px solid #333;
        padding-top: 10px; margin-top: 15px;
    }

    /* تحسين شكل الأفاتار - صور واقعية وبدون أخطاء */
    [data-testid="stChatMessageAvatarAssistant"] {
        background-image: url('https://img.freepik.com/free-photo/view-3d-beautiful-woman_23-2150707471.jpg') !important;
        background-size: cover; border: 1px solid #ff00ff;
    }
    [data-testid="stChatMessageAvatarUser"] {
        background-image: url('https://img.freepik.com/free-photo/view-3d-handsome-man_23-2150707158.jpg') !important;
        background-size: cover; border: 1px solid #00d4ff;
    }

    .prayer-table { width: 100%; border-collapse: collapse; margin: 10px 0; background: #111; border-radius: 10px; overflow: hidden; }
    .prayer-table td { padding: 10px; border: 1px solid #222; text-align: center; color: #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. دالة ذكاء تحديد الجنس من الاسم ---
def get_gender_label(name):
    # قائمة عينة لأسماء الإناث الشائعة لضبط الخطاب
    female_names = ["آية", "مريم", "سارة", "فاطمة", "نور", "ليلى", "آيلا", "هنا", "جنا", "ياسمين"]
    name = name.strip()
    if any(fn in name for fn in female_names) or name.endswith("ة") or name.endswith("ه"):
        return "تحدثي مع آيلا"
    return "تحدث مع آيلا"

# --- 3. البيانات الأساسية ---
azkar = ["سُبْحَانَ اللَّهِ وَبِحَمْدِهِ", "أَسْتَغْفِرُ اللَّهَ الْعَظِيمَ", "اللَّهُمَّ صَلِّ وَسَلِّمْ عَلَى نَبِيِّنَا مُحَمَّدٍ"] * 34
prayer_times = {"الفجر": "04:45", "الظهر": "12:05", "العصر": "15:25", "المغرب": "18:05", "العشاء": "19:25"}

if "user_data" not in st.session_state: st.session_state.user_data = {"name": "", "is_creator": False, "logged": False}
if "mode" not in st.session_state: st.session_state.mode = "chat"
if "count" not in st.session_state: st.session_state.count = 0
if "messages" not in st.session_state: st.session_state.messages = []

client = Groq(api_key="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")

# --- 4. واجهة الدخول ---
if not st.session_state.user_data["logged"]:
    st.markdown("<h2 style='text-align:center;'>💠 مرحباً بك في عالم آيلا</h2>", unsafe_allow_html=True)
    name_in = st.text_input("فضلاً، أدخل اسمك:")
    if st.button("دخول"):
        if "osman" in name_in.lower() or "عثمان" in name_in:
            st.session_state.user_data = {"name": name_in, "is_creator": True, "logged": True}
        else:
            st.session_state.user_data = {"name": name_in, "is_creator": False, "logged": True}
        st.rerun()

else:
    # الهيدر الفخم بالأفاتار الجديد
    st.markdown(f"""
        <div style="text-align:center; margin-bottom: 20px;">
            <div style="width:110px; height:110px; border-radius:50%; border:3px solid #ff00ff; display:inline-block; 
            background:url('https://img.freepik.com/free-photo/view-3d-beautiful-woman_23-2150707471.jpg') no-repeat center; background-size:cover; box-shadow: 0 0 20px #ff00ff;"></div>
            <div class="aila-gradient-title">آيلا | Aila AI</div>
            <div class="osman-tag">إشراف عثمان عصام | ابن بني سويف</div>
        </div>
    """, unsafe_allow_html=True)

    # القائمة ومواقيت الصلاة
    with st.expander("📂 القائمة الرئيسية ومواقيت الصلاة"):
        c1, c2, c3 = st.columns(3)
        if c1.button("💬 الدردشة"): st.session_state.mode = "chat"; st.rerun()
        if c2.button("📿 السبحة"): st.session_state.mode = "pray"; st.rerun()
        if c3.button("🕒 السجل"): st.session_state.mode = "history"; st.rerun()
        
        st.markdown("---")
        st.write("🕋 مواقيت الصلاة (بتوقيت القاهرة)")
        html_table = "<table class='prayer-table'><tr>"
        for p, t in prayer_times.items():
            html_table += f"<td>{p}<br>{t}</td>"
        html_table += "</tr></table>"
        st.markdown(html_table, unsafe_allow_html=True)

    # --- وضع الدردشة الذكية ---
    if st.session_state.mode == "chat":
        for m in st.session_state.messages:
            with st.chat_message(m["role"]): st.markdown(m["content"])

        # ميزة تحديد الجنس في خانة الإدخال
        input_label = get_gender_label(st.session_state.user_data["name"])
        if prompt := st.chat_input(input_label):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)

            with st.chat_message("assistant"):
                sys_msg = f"أنتِ آيلا. المستخدم هو {st.session_state.user_data['name']}. لغتك عربية فصحى بليغة جداً."
                if st.session_state.user_data["is_creator"]: sys_msg += " خاطبي عثمان عصام صانعك بكل محبة وتبجيل."

                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": sys_msg}] + st.session_state.messages
                ).choices[0].message.content
                
                footer = "\n\n<div class='support-footer'>إذا أعجبك المشروع، فلا تنسَ صانعه عثمان عصام ابن محافظة بني سويف من دعائك.</div>"
                st.markdown(res + footer, unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": res})

    # --- وضع السبحة ---
    elif st.session_state.mode == "pray":
        st.markdown(f"<h1 style='text-align:center; color:#d4af37;'>{st.session_state.count}</h1>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        if col1.button("➕ سبّح"): st.session_state.count += 1; st.rerun()
        if col2.button("🔄 تصفير"): st.session_state.count = 0; st.rerun()
        text = st.selectbox("اختر ذكراً:", azkar)
        st.info(text)
