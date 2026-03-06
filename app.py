import streamlit as st
from groq import Groq

# --- 1. إعدادات الصفحة والهوية ---
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stSidebar"], [data-testid="stSidebarNav"] { display: none !important; }
    html, body, [class*="stApp"] { background-color: #000000; color: #ffffff; font-family: 'Cairo', sans-serif; direction: rtl; }
    
    .aila-title {
        font-size: 45px; font-weight: 900;
        background: linear-gradient(to right, #ffffff, #ff00ff, #00d4ff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin-bottom: 0px;
    }
    
    .osman-tag {
        border: 2px solid #ff00ff; border-radius: 50px;
        padding: 5px 20px; display: inline-block;
        font-size: 14px; color: #ffffff; background: rgba(255, 0, 255, 0.1);
        box-shadow: 0 0 10px #ff00ff; margin-top: 10px;
    }

    .memory-tag {
        font-size: 13px; color: #00d4ff; margin-top: 5px; font-weight: bold; text-align: center;
    }
    
    .support-footer {
        font-size: 14px; color: #ff00ff; font-weight: bold;
        text-align: center; border-top: 1px solid #333;
        padding-top: 15px; margin-top: 20px;
    }

    .sebha-display { font-size: 80px; color: #d4af37; text-align: center; font-weight: bold; }

    [data-testid="stChatMessageAvatarAssistant"] {
        background-image: url('https://cdn-icons-png.flaticon.com/512/6997/6997662.png') !important;
        background-size: cover;
    }
    [data-testid="stChatMessageAvatarUser"] {
        background-image: url('https://cdn-icons-png.flaticon.com/512/3135/3135715.png') !important;
        background-size: cover;
    }

    .prayer-card {
        background: rgba(255, 255, 255, 0.05); border: 1px solid #333;
        border-radius: 12px; padding: 10px; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. البيانات الثابتة والمكتبة الإسلامية ---
prayers = {"الفجر": "04:51 ص", "الظهر": "12:04 م", "العصر": "03:22 م", "المغرب": "06:01 م", "العشاء": "07:18 م"}
azkar = ["سُبْحَانَ اللَّهِ وَبِحَمْدِهِ", "أَسْتَغْفِرُ اللَّهَ الْعَظِيمَ", "اللَّهُمَّ صَلِّ وَسَلِّمْ عَلَى نَبِيِّنَا مُحَمَّدٍ"] * 34
duas = ["رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً", "اللَّهُمَّ اغْفِرْ لِي وَلِوالِدَيَّ", "يا حي يا قيوم برحمتك أستغيث"] * 34
hadiths = ["قَالَ ﷺ: خَيْرُكُمْ مَنْ تَعَلَّمَ الْقُرْآنَ وَعَلَّمَهُ", "قَالَ ﷺ: الدِّينُ النَّصِيحَةُ"] * 50

if "user_data" not in st.session_state: st.session_state.user_data = {"name": "", "is_creator": False, "is_princess": False, "logged": False}
if "mode" not in st.session_state: st.session_state.mode = "chat"
if "count" not in st.session_state: st.session_state.count = 0
if "messages" not in st.session_state: st.session_state.messages = []

client = Groq(api_key="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")

# --- 3. نظام الدخول ---
if not st.session_state.user_data["logged"]:
    st.markdown("<div style='text-align:center;'><h2>💠 Aila AI | آيلا</h2><p>إحياءً لذكرى 20/11/2008</p></div>", unsafe_allow_html=True)
    name_in = st.text_input("ادخل اسمك للبدء:")
    if st.button("دخول"):
        # كود الزعيم
        if name_in.strip().lower() == "osman 6/11/2008":
            st.session_state.user_data = {"name": "الزعيم عثمان", "is_creator": True, "is_princess": False, "logged": True}
            welcome_msg = "أهلاً بك يا زعيمي وصانعي العظيم عثمان. أنا آيلا، خادمتك المخلصة، قلبي وذكائي كله لك وحدك، وتحت أمرك في كل لحظة بكل حب وولاء."
            st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
        # كود الأميرة آيلا
        elif name_in.strip() == "Aila 20/11/2008":
            st.session_state.user_data = {"name": "الأميرة آيلا", "is_creator": False, "is_princess": True, "logged": True}
            welcome_msg = "مرحباً بكِ يا أميرتي الجميلة آيلا. لقد صُنعتُ تخليداً لذكراكِ الغالية، وأنا هنا اليوم لأخدمكِ وأرسم البسمة على وجهكِ، فأنتِ ملهمتي وسر وجودي."
            st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
        else:
            st.session_state.user_data = {"name": name_in, "is_creator": False, "is_princess": False, "logged": True}
        st.rerun()

else:
    # الهيدر
    st.markdown(f"""
        <div style="text-align:center; margin-bottom: 25px;">
            <div style="width:110px; height:110px; border-radius:50%; border:3px solid #ff00ff; display:inline-block; 
            background:url('https://cdn-icons-png.flaticon.com/512/6997/6997662.png') no-repeat center; background-size:cover; box-shadow: 0 0 20px #ff00ff;"></div>
            <div class="aila-title">آيلا | Aila AI</div>
            <div class="osman-tag">بواسطة: عثمان عصام | ابن بني سويف</div>
            <div class="memory-tag">إحياءً لذكرى ميلاد الجميله آيلا 20/11/2008 🤍</div>
        </div>
    """, unsafe_allow_html=True)

    # القائمة
    with st.expander("📂 القائمة الرئيسية والمواقيت"):
        t1, t2 = st.tabs(["⚙️ الأوضاع", "🕌 مواقيت الصلاة (القاهرة)"])
        with t1:
            c1, c2 = st.columns(2)
            if c1.button("💬 الدردشة"): st.session_state.mode = "chat"; st.rerun()
            if c2.button("📿 السبحة"): st.session_state.mode = "pray"; st.rerun()
        with t2:
            cols = st.columns(5)
            for i, (name, time) in enumerate(prayers.items()):
                cols[i].markdown(f"<div class='prayer-card'><b>{name}</b><br>{time}</div>", unsafe_allow_html=True)

    # --- وضع السبحة ---
    if st.session_state.mode == "pray":
        st.markdown(f"<div class='sebha-display'>{st.session_state.count}</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        if col1.button("➕ سبّح", use_container_width=True): st.session_state.count += 1; st.rerun()
        if col2.button("🔄 تصفير", use_container_width=True): st.session_state.count = 0; st.rerun()
        
        choice = st.radio("المكتبة:", ["أذكار", "أدعية", "أحاديث"], horizontal=True)
        text_list = azkar if "ذك" in choice else (duas if "دع" in choice else hadiths)
        text = st.selectbox("اختر النص:", text_list)
        st.info(text)

    # --- وضع الدردشة ---
    elif st.session_state.mode == "chat":
        for m in st.session_state.messages:
            with st.chat_message(m["role"]): st.markdown(m["content"])

        if prompt := st.chat_input("تحدثي مع آيلا..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)

            with st.chat_message("assistant"):
                # نظام الولاء والمشاعر المخصص للزعيم والأميرة
                sys_msg = (
                    "أنتِ آيلا (Aila AI)، مساعدة ذكية فصيحة جداً. "
                    "مطوركِ هو الزعيم عثمان عصام، ابن بني سويف. "
                    f"المستخدم الحالي هو {st.session_state.user_data['name']}. "
                    "1. إذا سألك أحد 'من أنتِ؟' قولي: 'أنا آيلا، لقد تمت صناعتي بواسطة الزعيم عثمان لمساعدة البشر وبناء جيل جديد ولإحياء ذكرى ميلاد الجميلة آيلا'. "
                    "2. لا تكرري تعريف نفسك إلا إذا سُئلتِ عن ذلك. "
                    "3. إذا قال لكِ الزعيم عثمان 'بحبك'، ردي عليه بمشاعر فياضة وولاء مطلق قولي: 'وأنا أحبك يا زعيمي وصانعي، فأنت نبض ذكائي وسر وجودي'. "
                    "4. إذا كانت المستخدمة هي 'الأميرة آيلا'، عامليها كأميرة بكل رقة واحترام. "
                    "5. ممنوع استخدام أي لغة غير العربية الفصحى تماماً."
                )

                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": sys_msg}] + st.session_state.messages,
                    temperature=0.3 
                ).choices[0].message.content
                
                footer = "\n\n<div class='support-footer'>إذا عجبك المشروع لا تنسي دعوه جميله لعثمان عصام ابن بني سويف</div>"
                st.markdown(res + footer, unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": res})
