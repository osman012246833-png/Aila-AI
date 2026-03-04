import streamlit as st
from groq import Groq

# --- 1. إعدادات الصفحة والجماليات ---
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="centered")

# التنسيق البرمجي لمنع التشوه وجعل الألوان مطابقة للصورة
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* حذف أي عناصر مشوهة في منتصف الشاشة */
    [data-testid="stSidebar"], [data-testid="stSidebarNav"], .st-emotion-cache-10o48ve { display: none !important; }
    
    html, body, [class*="stApp"] {
        background-color: #000000; color: #ffffff;
        font-family: 'Cairo', sans-serif; direction: rtl;
    }

    /* تنسيق كلمة آيلا بلون مميز (تدرج لوني فخم) */
    .aila-gradient-title {
        font-size: 45px; font-weight: 900;
        background: linear-gradient(to right, #ffffff, #ff00ff, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }

    /* تصغير خانة الزعيم والتاريخ لتبدو أنيقة */
    .osman-tag {
        border: 1.5px solid #00d4ff; border-radius: 50px;
        padding: 4px 20px; display: inline-block;
        font-size: 14px; color: #ffffff;
        background: rgba(0, 212, 255, 0.1);
    }

    /* زر القائمة الرئيسي */
    .menu-btn {
        background: linear-gradient(45deg, #121212, #1e1e1e);
        border: 1px solid #ff00ff; border-radius: 10px;
        color: white; padding: 10px; cursor: pointer;
    }
    
    /* عداد السبحة اللانهائي */
    .sebha-display {
        font-size: 80px; color: #d4af37; text-align: center;
        font-weight: bold; margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة الحالة والبيانات ---
if "user_data" not in st.session_state: st.session_state.user_data = {"name": "", "is_creator": False, "logged": False}
if "mode" not in st.session_state: st.session_state.mode = "chat"
if "count" not in st.session_state: st.session_state.count = 0
if "messages" not in st.session_state: st.session_state.messages = []

client = Groq(api_key="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")

# --- 3. نظام الدخول والكود السري ---
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
    # الهيدر الموحد (نفس الشكل المطلوب)
    st.markdown(f"""
        <div style="text-align:center; margin-bottom: 20px;">
            <div style="width:100px; height:100px; border-radius:50%; border:3px solid #ff00ff; display:inline-block; 
            background:url('https://cdn-icons-png.flaticon.com/512/6997/6997662.png') no-repeat center; background-size:cover; box-shadow: 0 0 20px #ff00ff;"></div>
            <div class="aila-gradient-title">آيلا | Aila AI</div>
            <div class="osman-tag">إشراف الزعيم عثمان | 20/11/2008</div>
        </div>
    """, unsafe_allow_html=True)

    # زر القائمة الذي يجمع كل الخيارات
    with st.expander("📂 القائمة الرئيسية (السبحة، السجل، المكتبة)"):
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            if st.button("💬 الدردشة"): st.session_state.mode = "chat"; st.rerun()
        with col_m2:
            if st.button("📿 السبحة والعبادة"): st.session_state.mode = "pray"; st.rerun()
        with col_m3:
            if st.button("🕒 سجل المحادثات"): st.session_state.mode = "history"; st.rerun()

    # --- وضع السبحة اللانهائي والمكتبة ---
    if st.session_state.mode == "pray":
        st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
        st.markdown(f"<div class='sebha-display'>{st.session_state.count}</div>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("➕ سبّح", use_container_width=True): st.session_state.count += 1; st.rerun()
        with c2:
            if st.button("🔄 تصفير", use_container_width=True): st.session_state.count = 0; st.rerun()
        
        st.write("---")
        st.subheader("📖 المكتبة الإسلامية الشاملة")
        tab1, tab2, tab3 = st.tabs(["100 ذكر", "100 دعاء", "200 حديث"])
        with tab1: st.info("هنا تظهر قائمة الـ 100 ذكر (تشمل الصلاة على النبي ﷺ)")
        with tab2: st.info("هنا تظهر قائمة الـ 100 دعاء المستجاب")
        with tab3: st.info("هنا تظهر قائمة الـ 200 حديث شريف")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- وضع الدردشة الذكية ---
    elif st.session_state.mode == "chat":
        for m in st.session_state.messages:
            with st.chat_message(m["role"]): st.markdown(m["content"])

        if prompt := st.chat_input("تحدثي معي يا آيلا..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)

            with st.chat_message("assistant"):
                is_creator = st.session_state.user_data["is_creator"]
                sys_msg = f"أنتِ آيلا. المستخدم هو {st.session_state.user_data['name']}."
                if is_creator:
                    sys_msg += " هذا صانعك الزعيم عثمان، خاطبيه بولاء وحب مطلق."
                else:
                    sys_msg += " عرفي نفسك بأنكِ من تصميم الزعيم عثمان لإحياء ذكرى آيلا الجميلة."

                full_res = ""
                stream = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": sys_msg}] + st.session_state.messages,
                    stream=True
                )
                res_area = st.empty()
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        full_res += chunk.choices[0].delta.content
                        res_area.markdown(full_res + "▌")
                res_area.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})
