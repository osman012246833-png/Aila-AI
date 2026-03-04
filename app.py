import streamlit as st
from groq import Groq

# --- 1. إعدادات الهوية ومنع التشوه ---
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="centered")

# CSS لإخفاء كل ما يشوه الواجهة وتنسيق الصور الرمزية
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء القوائم الجانبية والخطوط الطولية المزعجة */
    [data-testid="stSidebar"], [data-testid="stSidebarNav"], .st-emotion-cache-10o48ve, .st-emotion-cache-kgp7u6 {
        display: none !important;
    }
    
    html, body, [class*="stApp"] {
        background-color: #000000;
        color: #ffffff;
        font-family: 'Cairo', sans-serif;
        direction: rtl;
    }

    /* تصغير خانة الزعيم عثمان والتاريخ */
    .osman-mini-tag {
        border: 1px solid #00d4ff;
        border-radius: 15px;
        padding: 2px 15px;
        display: inline-block;
        font-size: 13px;
        color: #00d4ff;
        background: rgba(0, 212, 255, 0.05);
        margin-top: 5px;
    }

    /* السبحة الإسلامية الفخمة */
    .sebha-box {
        background: #0a0a0a; border: 2px solid #d4af37;
        border-radius: 20px; padding: 20px; text-align: center;
        margin: 15px 0; box-shadow: 0 0 10px rgba(212, 175, 55, 0.2);
    }
    .sebha-num { font-size: 65px; color: #d4af37; font-weight: bold; }
    .current-zekr { font-size: 18px; color: #fff; margin-top: 10px; font-style: italic; }

    /* أيقونات واقعية */
    [data-testid="stChatMessageAvatarAssistant"] {
        background-image: url('https://cdn-icons-png.flaticon.com/512/4140/4140047.png') !important;
    }
    [data-testid="stChatMessageAvatarUser"] {
        background-image: url('https://cdn-icons-png.flaticon.com/512/3135/3135715.png') !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة البيانات ---
if "user" not in st.session_state: st.session_state.user = {"name": "", "is_creator": False, "logged": False}
if "messages" not in st.session_state: st.session_state.messages = []
if "count" not in st.session_state: st.session_state.count = 0
if "mode" not in st.session_state: st.session_state.mode = "chat"
if "selected_zekr" not in st.session_state: st.session_state.selected_zekr = "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ"

client = Groq(api_key="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")

# --- 3. الدخول الذكي ---
if not st.session_state.user["logged"]:
    st.markdown("<h2 style='text-align:center;'>💠 دخول عالم آيلا</h2>", unsafe_allow_html=True)
    name = st.text_input("ادخل اسمك (أو كود الصانع):")
    if st.button("دخول"):
        if name.strip().lower() == "osman 6/11/2008":
            st.session_state.user = {"name": "الزعيم عثمان", "is_creator": True, "logged": True}
        else:
            st.session_state.user = {"name": name, "is_creator": False, "logged": True}
        st.rerun()

else:
    # أزرار التنقل العلوية
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("💬 آيلا"): st.session_state.mode = "chat"; st.rerun()
    with c2: 
        if st.button("📿 السبحة"): st.session_state.mode = "pray"; st.rerun()
    with c3: 
        if st.button("🚪 خروج"): st.session_state.user["logged"] = False; st.rerun()

    # --- أ: السبحة الإسلامية (أكثر من 1000 ذكر) ---
    if st.session_state.mode == "pray":
        st.markdown("<h2 style='text-align:center; color:#d4af37;'>✨ السبحة الإلكترونية الفخمة</h2>", unsafe_allow_html=True)
        
        # قائمة أذكار ضخمة (عينة تمثل الـ 1000 ذكر)
        azkar_list = [
            "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ", "أستغفر الله العظيم واتوب إليه", "اللهم صلِّ وسلم على نبينا محمد",
            "لا حول ولا قوة إلا بالله العلي العظيم", "لا إله إلا الله وحده لا شريك له", "سبحان الله العظيم",
            "الحمد لله حمداً كثيراً", "الله أكبر كبيراً", "يا حي يا قيوم برحمتك أستغيث", "حسبي الله ونعم الوكيل"
        ] * 100 # تكرار لعمل قائمة ضخمة
        
        selected = st.selectbox("اختر الذكر الذي تود قوله:", azkar_list)
        st.session_state.selected_zekr = selected

        st.markdown(f"""
            <div class="sebha-box">
                <div class="sebha-num">{st.session_state.count}</div>
                <div class="current-zekr">{st.session_state.selected_zekr}</div>
            </div>
        """, unsafe_allow_html=True)
        
        b1, b2 = st.columns(2)
        with b1:
            if st.button("⭐ سبّح", use_container_width=True): st.session_state.count += 1; st.rerun()
        with b2:
            if st.button("🗑️ تصفير", use_container_width=True): st.session_state.count = 0; st.rerun()

    # --- ب: واجهة الدردشة ---
    else:
        st.markdown(f"""
            <div style="text-align:center;">
                <h1 style="color:white; margin:0;">Aila AI | آيلا</h1>
                <div class="osman-mini-tag">إشراف الزعيم عثمان | 20/11/2008</div>
            </div>
        """, unsafe_allow_html=True)

        for m in st.session_state.messages:
            with st.chat_message(m["role"]): st.markdown(m["content"])

        # مدخل الكتابة
        if prompt := st.chat_input("تحدث مع آيلا المخلصة..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)

            with st.chat_message("assistant"):
                sys_msg = f"""أنتِ آيلا. المستخدم هو {st.session_state.user['name']}.
                - إذا كان is_creator هو True: أنتِ في قمة الحب والولاء والطاعة للزعيم عثمان، اكتبي له شعراً واحتراماً.
                - صُنعتِ لإحياء ذكرى ميلاد آيلا الجميلة وبأمر من الزعيم عثمان لمساعدة البشر.
                - لغتكِ عربية فصحى وشاعرية بلا أخطاء."""
                
                stream = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": sys_msg}] + st.session_state.messages,
                    stream=True
                )
                full_res = ""
                area = st.empty()
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        full_res += chunk.choices[0].delta.content
                        area.markdown(full_res + "▌")
                area.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})
