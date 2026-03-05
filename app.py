import streamlit as st
from groq import Groq
import datetime

# --- 1. إعدادات الصفحة والجماليات ---
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
    .sebha-display { font-size: 80px; color: #d4af37; text-align: center; font-weight: bold; margin: 10px 0; }
    .zekr-card { background: rgba(255, 255, 255, 0.05); border-right: 5px solid #ff00ff; padding: 15px; border-radius: 10px; margin: 10px 0; font-size: 18px; }
    .prayer-time-box { background: #111; border: 1px solid #00d4ff; border-radius: 10px; padding: 10px; text-align: center; margin: 5px; }
    .support-msg { font-size: 12px; color: #ff00ff; font-style: italic; border-top: 1px solid #333; margin-top: 10px; padding-top: 5px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. المكتبة والبيانات ---
azkar_list = ["سُبْحَانَ اللَّهِ وَبِحَمْدِهِ", "أَسْتَغْفِرُ اللَّهَ وَأَتُوبُ إِلَيْهِ", "لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ", "اللَّهُمَّ صَلِّ وَسَلِّمْ عَلَى نَبِيِّنَا مُحَمَّدٍ"] * 25
duas_list = ["رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً", "اللَّهُمَّ إِنَّكَ عَفُوٌّ تُحِبُّ الْعَفْوَ فَاعْفُ عَنَّا"] * 50
hadiths_list = ["قَالَ ﷺ: خَيْرُكُمْ مَنْ تَعَلَّمَ الْقُرْآنَ وَعَلَّمَهُ", "قَالَ ﷺ: الدِّينُ النَّصِيحَةُ"] * 50

# مواقيت الصلاة (مثال تقريبي - يمكن ربطها بـ API لاحقاً)
prayer_times = {"الفجر": "04:50", "الظهر": "12:05", "العصر": "15:20", "المغرب": "18:02", "العشاء": "19:20"}

if "user_data" not in st.session_state: st.session_state.user_data = {"name": "", "is_creator": False, "logged": False}
if "mode" not in st.session_state: st.session_state.mode = "chat"
if "count" not in st.session_state: st.session_state.count = 0
if "messages" not in st.session_state: st.session_state.messages = []

client = Groq(api_key="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")

# --- 3. واجهة الدخول ---
if not st.session_state.user_data["logged"]:
    st.markdown("<h2 style='text-align:center;'>💠 دخول عالم آيلا</h2>", unsafe_allow_html=True)
    name_in = st.text_input("ادخل اسمك:")
    if st.button("دخول"):
        if name_in.strip().lower() == "osman 6/11/2008":
            st.session_state.user_data = {"name": "الزعيم عثمان", "is_creator": True, "logged": True}
        else:
            st.session_state.user_data = {"name": name_in, "is_creator": False, "logged": True}
        st.rerun()

else:
    # الهيدر الموحد
    st.markdown(f"""
        <div style="text-align:center; margin-bottom: 20px;">
            <div style="width:100px; height:100px; border-radius:50%; border:3px solid #ff00ff; display:inline-block; 
            background:url('https://raw.githubusercontent.com/عثمان/Aila/main/aila_avatar.png') no-repeat center; background-size:cover; box-shadow: 0 0 20px #ff00ff;"></div>
            <div class="aila-gradient-title">آيلا | Aila AI</div>
            <div class="osman-tag">إشراف الزعيم عثمان | 20/11/2008</div>
        </div>
    """, unsafe_allow_html=True)

    # القائمة الرئيسية
    with st.expander("📂 القائمة الرئيسية (السبحة، السجل، المكتبة، مواقيت الصلاة)"):
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            if st.button("💬 الدردشة"): st.session_state.mode = "chat"; st.rerun()
        with col_m2:
            if st.button("📿 السبحة والعبادة"): st.session_state.mode = "pray"; st.rerun()
        with col_m3:
            if st.button("🕒 سجل المحادثات"): st.session_state.mode = "history"; st.rerun()
        
        st.markdown("---")
        st.subheader("🕌 مواقيت الصلاة")
        cols = st.columns(5)
        for i, (name, time) in enumerate(prayer_times.items()):
            cols[i].markdown(f"<div class='prayer-time-box'><b>{name}</b><br>{time}</div>", unsafe_allow_html=True)

    # --- وضع السبحة والعبادة ---
    if st.session_state.mode == "pray":
        st.markdown("<div class='sebha-display'>" + str(st.session_state.count) + "</div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("➕ سبّح", use_container_width=True): st.session_state.count += 1; st.rerun()
        with c2:
            if st.button("🔄 تصفير", use_container_width=True): st.session_state.count = 0; st.rerun()
        
        choice = st.radio("القسم:", ["أذكار", "أدعية", "أحاديث"], horizontal=True)
        current_data = azkar_list if "أذكار" in choice else (duas_list if "أدعية" in choice else hadiths_list)
        selected_text = st.selectbox("اختر النص:", current_data)
        st.markdown(f"<div class='zekr-card'>{selected_text}</div>", unsafe_allow_html=True)

    # --- وضع الدردشة ---
    elif st.session_state.mode == "chat":
        for m in st.session_state.messages:
            with st.chat_message(m["role"]): st.markdown(m["content"])

        if prompt := st.chat_input("تحدثي معي يا آيلا..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)

            with st.chat_message("assistant"):
                sys_msg = f"أنتِ آيلا. المستخدم هو {st.session_state.user_data['name']}. لغتك عربية فصحى بليغة جداً وبدون أخطاء."
                if st.session_state.user_data["is_creator"]: sys_msg += " خاطبي صانعك الزعيم عثمان بكل ود."
                
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": sys_msg}] + st.session_state.messages
                ).choices[0].message.content
                
                # إضافة رسالة الدعم في نهاية الرد
                final_res = f"{res}\n\n<div class='support-msg'>إذا أعجبك المشروع، لا تنسَ صانعه الزعيم عثمان من دعائك.</div>"
                st.markdown(final_res, unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": res})
