import streamlit as st
from groq import Groq

# --- 1. إعدادات الصفحة والتنسيق الفخم ---
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stSidebar"], [data-testid="stSidebarNav"] { display: none !important; }
    html, body, [class*="stApp"] { background-color: #000000; color: #ffffff; font-family: 'Cairo', sans-serif; direction: rtl; }
    
    /* عنوان آيلا المتدرج */
    .aila-gradient-title {
        font-size: 45px; font-weight: 900;
        background: linear-gradient(to right, #ffffff, #ff00ff, #ffffff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 5px; text-align: center;
    }
    
    /* تاق الزعيم */
    .osman-tag {
        border: 1.5px solid #00d4ff; border-radius: 50px;
        padding: 4px 20px; display: inline-block;
        font-size: 14px; color: #ffffff;
        background: rgba(0, 212, 255, 0.1);
    }
    
    /* رسالة الدعم لابن بني سويف */
    .support-footer {
        font-size: 13px; color: #ff00ff; font-weight: bold;
        text-align: center; border-top: 1px solid #333;
        padding-top: 10px; margin-top: 15px;
    }

    /* عداد السبحة */
    .sebha-display { font-size: 80px; color: #d4af37; text-align: center; font-weight: bold; }
    
    /* تحسين شكل الأفاتار */
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

# --- 2. المكتبة الإسلامية ---
azkar = ["سُبْحَانَ اللَّهِ وَبِحَمْدِهِ", "أَسْتَغْفِرُ اللَّهَ الْعَظِيمَ", "اللَّهُمَّ صَلِّ وَسَلِّمْ عَلَى نَبِيِّنَا مُحَمَّدٍ"] * 34
duas = ["رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً", "اللَّهُمَّ اغْفِرْ لِي وَلِوَالِدَيَّ"] * 50
hadiths = ["قَالَ ﷺ: خَيْرُكُمْ مَنْ تَعَلَّمَ الْقُرْآنَ وَعَلَّمَهُ", "قَالَ ﷺ: الدِّينُ النَّصِيحَةُ"] * 50

if "user_data" not in st.session_state: st.session_state.user_data = {"name": "", "is_creator": False, "logged": False}
if "mode" not in st.session_state: st.session_state.mode = "chat"
if "count" not in st.session_state: st.session_state.count = 0
if "messages" not in st.session_state: st.session_state.messages = []

client = Groq(api_key="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")

# --- 3. نظام الدخول ---
if not st.session_state.user_data["logged"]:
    st.markdown("<h2 style='text-align:center;'>💠 مرحباً بك في عالم آيلا</h2>", unsafe_allow_html=True)
    name_in = st.text_input("فضلاً، أدخل اسمك:")
    if st.button("دخول"):
        if name_in.strip().lower() == "osman 6/11/2008":
            st.session_state.user_data = {"name": "عثمان عصام", "is_creator": True, "logged": True}
        else:
            st.session_state.user_data = {"name": name_in, "is_creator": False, "logged": True}
        st.rerun()

else:
    # الهيدر الفخم
    st.markdown(f"""
        <div style="text-align:center; margin-bottom: 20px;">
            <div style="width:100px; height:100px; border-radius:50%; border:3px solid #ff00ff; display:inline-block; 
            background:url('https://cdn-icons-png.flaticon.com/512/6997/6997662.png') no-repeat center; background-size:cover; box-shadow: 0 0 20px #ff00ff;"></div>
            <div class="aila-gradient-title">آيلا | Aila AI</div>
            <div class="osman-tag">إشراف الزعيم عثمان | 20/11/2008</div>
        </div>
    """, unsafe_allow_html=True)

    # القائمة
    with st.expander("📂 القائمة الرئيسية"):
        c1, c2, c3 = st.columns(3)
        if c1.button("💬 الدردشة"): st.session_state.mode = "chat"; st.rerun()
        if c2.button("📿 السبحة"): st.session_state.mode = "pray"; st.rerun()
        if c3.button("🕒 السجل"): st.session_state.mode = "history"; st.rerun()

    # --- وضع السبحة ---
    if st.session_state.mode == "pray":
        st.markdown(f"<div class='sebha-display'>{st.session_state.count}</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        if col1.button("➕ سبّح"): st.session_state.count += 1; st.rerun()
        if col2.button("🔄 تصفير"): st.session_state.count = 0; st.rerun()
        
        choice = st.radio("المكتبة:", ["أذكار", "أدعية", "أحاديث"], horizontal=True)
        text = st.selectbox("اختر النص:", azkar if "ذك" in choice else (duas if "دع" in choice else hadiths))
        st.info(text)

    # --- وضع الدردشة ---
    elif st.session_state.mode == "chat":
        for m in st.session_state.messages:
            with st.chat_message(m["role"]): st.markdown(m["content"])

        if prompt := st.chat_input("تحدثي مع آيلا الفصيحة..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)

            with st.chat_message("assistant"):
                sys_msg = f"أنتِ آيلا. المستخدم هو {st.session_state.user_data['name']}. يجب أن تكون لغتك العربية بليغة، فصيحة، ودقيقة جداً نحوياً وصرفياً."
                if st.session_state.user_data["is_creator"]: sys_msg += " خاطبي عثمان بكل تبجيل ومحبة."

                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": sys_msg}] + st.session_state.messages
                ).choices[0].message.content
                
                # رسالة الدعم النهائية
                footer = "\n\n<div class='support-footer'>إذا أعجبك المشروع، فلا تنسَ صانعه عثمان عصام ابن محافظة بني سويف من دعائك.</div>"
                st.markdown(res + footer, unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": res})
