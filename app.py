import streamlit as st
from groq import Groq

# --- 1. إعدادات الصفحة والتنسيق ---
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stSidebar"], [data-testid="stSidebarNav"] { display: none !important; }
    html, body, [class*="stApp"] { background-color: #000000; color: #ffffff; font-family: 'Cairo', sans-serif; direction: rtl; }
    
    .aila-gradient-title {
        font-size: 45px; font-weight: 900;
        background: linear-gradient(to right, #ffffff, #00d4ff, #ff00ff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 5px; text-align: center;
    }
    
    .osman-tag {
        border: 1.5px solid #00d4ff; border-radius: 50px;
        padding: 4px 20px; display: inline-block;
        font-size: 14px; color: #ffffff;
        background: rgba(0, 212, 255, 0.1);
    }
    
    .tribute-text {
        color: #aaaaaa; font-size: 14px; text-align: center; font-style: italic; margin-bottom: 20px;
    }
    
    .support-footer {
        font-size: 13px; color: #ff00ff; font-weight: bold;
        text-align: center; border-top: 1px solid #333;
        padding-top: 10px; margin-top: 15px;
    }

    .sebha-display { font-size: 60px; color: #d4af37; text-align: center; font-weight: bold; }
    
    .prayer-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid #ff00ff; border-radius: 10px;
        padding: 10px; margin: 5px; text-align: center;
    }

    [data-testid="stChatMessageAvatarAssistant"] {
        background-image: url('https://cdn-icons-png.flaticon.com/512/6997/6997662.png') !important;
        background-size: cover;
    }
    [data-testid="stChatMessageAvatarUser"] {
        background-image: url('https://cdn-icons-png.flaticon.com/512/3135/3135715.png') !important;
        background-size: cover;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. البيانات ---
prayers = {"الفجر": "04:51 ص", "الظهر": "12:04 م", "العصر": "03:22 م", "المغرب": "06:01 م", "العشاء": "07:18 م"}
azkar = ["سُبْحَانَ اللَّهِ وَبِحَمْدِهِ", "أَسْتَغْفِرُ اللَّهَ الْعَظِيمَ", "اللَّهُمَّ صَلِّ وَسَلِّمْ عَلَى نَبِيِّنَا مُحَمَّدٍ"] * 34

if "user_data" not in st.session_state: st.session_state.user_data = {"name": "", "is_creator": False, "logged": False}
if "mode" not in st.session_state: st.session_state.mode = "chat"
if "count" not in st.session_state: st.session_state.count = 0
if "messages" not in st.session_state: st.session_state.messages = []

client = Groq(api_key="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")

# --- 3. نظام الدخول ---
if not st.session_state.user_data["logged"]:
    st.markdown("<h2 style='text-align:center;'>💠 مرحباً بك في عالم آيلا</h2>", unsafe_allow_html=True)
    st.markdown("<p class='tribute-text'>هذا العمل إحياء لذكرى ميلاد الجميلة آيلا</p>", unsafe_allow_html=True)
    name_in = st.text_input("فضلاً، أدخل اسمك:")
    if st.button("دخول"):
        if name_in.strip().lower() == "osman 6/11/2008":
            st.session_state.user_data = {"name": "عثمان عصام", "is_creator": True, "logged": True}
        else:
            st.session_state.user_data = {"name": name_in, "is_creator": False, "logged": True}
        st.rerun()

else:
    # الهيدر
    st.markdown(f"""
        <div style="text-align:center; margin-bottom: 20px;">
            <div style="width:100px; height:100px; border-radius:50%; border:3px solid #ff00ff; display:inline-block; 
            background:url('https://cdn-icons-png.flaticon.com/512/6997/6997662.png') no-repeat center; background-size:cover; box-shadow: 0 0 20px #ff00ff;"></div>
            <div class="aila-gradient-title">آيلا | Aila AI</div>
            <div class="osman-tag">إشراف الزعيم عثمان | ابن بني سويف</div>
            <p class='tribute-text' style='margin-top:10px;'>بُني هذا الذكاء تخليداً لذكرى ميلاد "آيلا" الجميلة</p>
        </div>
    """, unsafe_allow_html=True)

    with st.expander("📂 القائمة الرئيسية والمواقيت"):
        tab1, tab2, tab3 = st.tabs(["💬 الأوضاع", "🕌 مواقيت الصلاة", "📜 السجل"])
        with tab1:
            col_a, col_b = st.columns(2)
            if col_a.button("💬 وضع الدردشة", use_container_width=True): st.session_state.mode = "chat"; st.rerun()
            if col_b.button("📿 وضع السبحة", use_container_width=True): st.session_state.mode = "pray"; st.rerun()
        with tab2:
            st.markdown("<p style='text-align:center;'>توقيت القاهرة</p>", unsafe_allow_html=True)
            cols = st.columns(5)
            for i, (p_name, p_time) in enumerate(prayers.items()):
                cols[i].markdown(f"<div class='prayer-card'><b style='color:#00d4ff;'>{p_name}</b><br>{p_time}</div>", unsafe_allow_html=True)
        with tab3:
            if st.button("🗑️ مسح السجل"): st.session_state.messages = []; st.rerun()

    # --- وضع السبحة ---
    if st.session_state.mode == "pray":
        st.markdown(f"<div class='sebha-display'>{st.session_state.count}</div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        if c1.button("➕ سبّح", use_container_width=True): st.session_state.count += 1; st.rerun()
        if c2.button("🔄 تصفير", use_container_width=True): st.session_state.count = 0; st.rerun()
        st.info(azkar[st.session_state.count % len(azkar)])

    # --- وضع الدردشة ---
    elif st.session_state.mode == "chat":
        for m in st.session_state.messages:
            with st.chat_message(m["role"]): st.markdown(m["content"])

        if prompt := st.chat_input("تحدثي مع آيلا الفصيحة..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)

            with st.chat_message("assistant"):
                # تحسين الـ System Prompt ليكون صارماً جداً تجاه اللغة العربية
                sys_msg = (
                    f"أنتِ 'آيلا'. سُميتِ بهذا الاسم إحياءً لذكرى ميلاد طفلة جميلة تحمل نفس الاسم. "
                    f"مطورك هو عثمان عصام. صفتك الأساسية: الفصاحة المطلقة. "
                    f"ممنوع استخدام أي لغة غير العربية. يمنع تماماً الحروف الروسية أو اليابانية أو الإنجليزية. "
                    f"رداً على أي سؤال، استخدمي لغة عربية سليمة 100% وبأسلوب راقٍ."
                )
                if st.session_state.user_data["is_creator"]: sys_msg += " تعاملي مع عثمان بتقدير خاص كونه الأب الروحي لهذا المشروع."

                try:
                    res = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "system", "content": sys_msg}] + st.session_state.messages,
                        temperature=0.7 # خفض درجة الحرارة يجعل الإجابة أكثر دقة لغوياً
                    ).choices[0].message.content
                    
                    st.markdown(res)
                    st.markdown(f"<div class='support-footer'>إحياءً لذكرى ميلاد آيلا - بإشراف عثمان عصام</div>", unsafe_allow_html=True)
                    st.session_state.messages.append({"role": "assistant", "content": res})
                except:
                    st.error("عذراً، حدث خطأ فني.")
