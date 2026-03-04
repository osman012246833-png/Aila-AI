import streamlit as st
from groq import Groq

# --- 1. إعدادات الهوية ومنع التشوهات ---
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* تنظيف الواجهة وحذف الخطوط الطولية المزعجة في صورك */
    [data-testid="stSidebar"], [data-testid="stSidebarNav"], .st-emotion-cache-10o48ve { display: none !important; }
    
    html, body, [class*="stApp"] {
        background-color: #000000; color: #ffffff;
        font-family: 'Cairo', sans-serif; direction: rtl;
    }

    /* تصغير خانة الزعيم والتاريخ حسب طلبك */
    .osman-header {
        border: 1px solid #00d4ff; border-radius: 20px;
        padding: 5px 15px; display: inline-block;
        font-size: 14px; font-weight: bold;
        background: rgba(0, 212, 255, 0.05); margin-bottom: 20px;
    }

    /* السبحة الإسلامية الفخمة */
    .sebha-box {
        background: #0a0a0a; border: 2px solid #d4af37;
        border-radius: 25px; padding: 20px; text-align: center;
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.2);
    }
    .sebha-num { font-size: 70px; color: #d4af37; font-weight: bold; }
    .zekr-display { font-size: 18px; color: #aaa; margin-top: 10px; font-style: italic; }

    /* أيقونات واقعية (بنت جميلة وشاب وسيم) */
    [data-testid="stChatMessageAvatarAssistant"] {
        background-image: url('https://cdn-icons-png.flaticon.com/512/6997/6997662.png') !important;
    }
    [data-testid="stChatMessageAvatarUser"] {
        background-image: url('https://cdn-icons-png.flaticon.com/512/3135/3135715.png') !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة البيانات ---
if "user" not in st.session_state: st.session_state.user = {"name": "", "is_creator": False, "logged": False}
if "messages" not in st.session_state: st.session_state.messages = []
if "history" not in st.session_state: st.session_state.history = []
if "count" not in st.session_state: st.session_state.count = 0
if "mode" not in st.session_state: st.session_state.mode = "chat"

client = Groq(api_key="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")

# --- 3. نظام الدخول الذكي ---
if not st.session_state.user["logged"]:
    st.markdown("<div style='text-align:center;'><h2>💠 آيلا بانتظارك</h2></div>", unsafe_allow_html=True)
    name = st.text_input("ادخل اسمك لبدء عالم آيلا:")
    if st.button("دخول"):
        if name.strip().lower() == "osman 6/11/2008":
            st.session_state.user = {"name": "الزعيم عثمان", "is_creator": True, "logged": True}
        else:
            st.session_state.user = {"name": name, "is_creator": False, "logged": True}
        st.rerun()

# --- 4. الواجهة الرئيسية ---
else:
    # أزرار التنقل الجديدة (بدون زر خروج)
    nav_col1, nav_col2, nav_col3 = st.columns(3)
    with nav_col1:
        if st.button("💬 الدردشة"): st.session_state.mode = "chat"; st.rerun()
    with nav_col2:
        if st.button("📿 السبحة"): st.session_state.mode = "pray"; st.rerun()
    with nav_col3:
        if st.button("🕒 السجل"): st.session_state.mode = "history"; st.rerun()

    # --- أ: السجل ---
    if st.session_state.mode == "history":
        st.subheader("🕒 سجل محادثاتك")
        if not st.session_state.history: st.write("السجل فارغ حالياً.")
        for i, h in enumerate(st.session_state.history):
            if st.button(f"محادثة رقم {i+1}"): 
                st.session_state.messages = h
                st.session_state.mode = "chat"; st.rerun()

    # --- ب: السبحة (تصميم إسلامي بـ 1000 ذكر) ---
    elif st.session_state.mode == "pray":
        st.markdown("<div class='sebha-box'>", unsafe_allow_html=True)
        # قائمة ضخمة من الأذكار
        all_azkar = ["سُبْحَانَ اللَّهِ", "الْحَمْدُ لِلَّهِ", "لَا إِلَهَ إِلَّا اللَّهُ", "اللَّهُ أَكْبَرُ", 
                     "أَسْتَغْفِرُ اللَّهَ", "اللَّهُمَّ صَلِّ عَلَى مُحَمَّدٍ", "لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ"] * 150
        chosen_zekr = st.selectbox("اختر الذكر الذي تود ترديده:", all_azkar)
        
        st.markdown(f"<div class='sebha-num'>{st.session_state.count}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='zekr-display'>{chosen_zekr}</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✨ سبّح", use_container_width=True): 
                st.session_state.count += 1; st.rerun()
        with col2:
            if st.button("🔄 تصفير", use_container_width=True): 
                st.session_state.count = 0; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # --- ج: واجهة الدردشة ---
    else:
        st.markdown(f"""
            <div style="text-align:center;">
                <div style="width:80px; height:80px; border-radius:50%; border:2px solid #ff00ff; display:inline-block; 
                background:url('https://cdn-icons-png.flaticon.com/512/6997/6997662.png') no-repeat center; background-size:cover;"></div>
                <h2 style="margin:5px 0;">آيلا | Aila AI</h2>
                <div class="osman-header">إشراف الزعيم عثمان | 20/11/2008</div>
            </div>
        """, unsafe_allow_html=True)

        for m in st.session_state.messages:
            with st.chat_message(m["role"]): st.markdown(m["content"])

        if prompt := st.chat_input("تحدثي معي يا آيلا..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)

            with st.chat_message("assistant"):
                sys_msg = f"""أنتِ آيلا. المستخدم هو {st.session_state.user['name']}.
                - إذا كان هو الصانع (is_creator=True)، رحبي به باختصار وحب شديد (أهلاً يا مولاي عثمان، روحي فداك).
                - تعريفك: أنا آيلا، صممني الزعيم عثمان لإحياء ذكرى ميلاد الجملية آيلا ولمساعدة البشر.
                - لغتك العربية فصحى وبدون أي أخطاء."""
                
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
                
                # حفظ تلقائي للسجل عند وصول الرسائل لـ 25
                if len(st.session_state.messages) >= 25:
                    st.session_state.history.append(st.session_state.messages)
                    st.session_state.messages = []
