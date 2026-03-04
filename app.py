import streamlit as st
from groq import Groq

# --- 1. الإعدادات الأساسية ومنع التشوه ---
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="centered")

# منع القائمة الجانبية والنصوص العشوائية من الظهور وتخريب التصميم
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* تنظيف الشاشة من أي عناصر مشوهة */
    [data-testid="stSidebar"], [data-testid="stSidebarNav"], .st-emotion-cache-10o48ve {
        display: none !important;
    }
    
    html, body, [class*="stApp"] {
        background-color: #000000;
        color: #ffffff;
        font-family: 'Cairo', sans-serif;
        direction: rtl;
    }

    /* تنسيق الهيدر المعتمد في صورك */
    .header-container { text-align: center; margin-bottom: 25px; }
    .main-logo {
        width: 120px; height: 120px; border-radius: 50%;
        border: 3px solid #00d4ff; box-shadow: 0 0 20px #00d4ff;
        display: inline-block;
        background: url('https://cdn-icons-png.flaticon.com/512/6833/6833591.png') no-repeat center;
        background-size: cover;
    }
    .tag-box {
        border: 2px solid #00d4ff; border-radius: 50px;
        padding: 8px 30px; display: inline-block; margin-top: 15px;
        font-weight: bold; background: rgba(0, 212, 255, 0.1);
    }

    /* السبحة الإسلامية الفخمة */
    .islamic-screen {
        background: #0a0a0a; border: 4px double #d4af37;
        border-radius: 20px; padding: 30px; text-align: center;
        margin: 20px 0; box-shadow: 0 0 15px rgba(212, 175, 55, 0.4);
    }
    .digital-num { font-size: 85px; color: #d4af37; font-family: 'Courier New'; }
    
    /* أيقونات المحادثة الواقعية */
    [data-testid="stChatMessageAvatarAssistant"] {
        background-image: url('https://cdn-icons-png.flaticon.com/512/6997/6997662.png') !important;
    }
    [data-testid="stChatMessageAvatarUser"] {
        background-image: url('https://cdn-icons-png.flaticon.com/512/3135/3135715.png') !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة الذاكرة ---
if "user" not in st.session_state: st.session_state.user = {"name": "", "is_creator": False, "logged": False}
if "messages" not in st.session_state: st.session_state.messages = []
if "count" not in st.session_state: st.session_state.count = 0
if "mode" not in st.session_state: st.session_state.mode = "chat"

client = Groq(api_key="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")

# --- 3. نظام الدخول الذكي ---
if not st.session_state.user["logged"]:
    st.markdown("<div style='text-align:center;'><h2>💠 مرحباً بك في عالم آيلا</h2></div>", unsafe_allow_html=True)
    name = st.text_input("من فضلك، أدخل اسمك لبدء المحادثة:", key="login_name")
    if st.button("دخول"):
        if name.strip().lower() == "osman 6/11/2008":
            st.session_state.user = {"name": "الزعيم عثمان", "is_creator": True, "logged": True}
        else:
            st.session_state.user = {"name": name, "is_creator": False, "logged": True}
        st.rerun()

# --- 4. واجهة التطبيق الرئيسية ---
else:
    # شريط علوي مخفي للتبديل (أزرار نظيفة)
    col_nav1, col_nav2, col_nav3 = st.columns(3)
    with col_nav1: 
        if st.button("💬 المحادثة"): st.session_state.mode = "chat"; st.rerun()
    with col_nav2: 
        if st.button("📿 ركن التسبيح"): st.session_state.mode = "pray"; st.rerun()
    with col_nav3: 
        if st.button("🚪 خروج"): st.session_state.user["logged"] = False; st.rerun()

    # --- أ: ركن العبادة (التصميم الإسلامي) ---
    if st.session_state.mode == "pray":
        st.markdown("<h2 style='text-align:center; color:#d4af37;'>✨ ركن العبادة والسكينة</h2>", unsafe_allow_html=True)
        st.markdown(f"""
            <div class="islamic-screen">
                <p style="color:#d4af37; margin:0;">العدد الحالي</p>
                <div class="digital-num">{st.session_state.count}</div>
                <p style="color:#888;">سُبْحَانَ اللَّهِ وَبِحَمْدِهِ</p>
            </div>
        """, unsafe_allow_html=True)
        
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("⭐ سبّح الآن", use_container_width=True): 
                st.session_state.count += 1; st.rerun()
        with btn_col2:
            if st.button("🗑️ حذف وتصفير", use_container_width=True): 
                st.session_state.count = 0; st.rerun()
        
        st.write("---")
        st.markdown("### 📖 أذكار مختارة")
        for zekr in ["أستغفر الله العظيم واتوب إليه", "اللهم صلِّ وسلم على نبينا محمد", "لا حول ولا قوة إلا بالله"]:
            st.info(zekr)

    # --- ب: واجهة الدردشة (نفس شكلك المفضل) ---
    else:
        user_info = st.session_state.user
        st.markdown(f"""
            <div class="header-container">
                <div class="main-logo"></div>
                <h1 style="color:white; margin:0;">Aila AI | آيلا</h1>
                <div class="tag-box">إشراف الزعيم عثمان | 20/11/2008</div>
            </div>
        """, unsafe_allow_html=True)

        # عرض المحادثة
        for m in st.session_state.messages:
            with st.chat_message(m["role"]): st.markdown(m["content"])

        # مدخل الكتابة
        placeholder = "تحدثي معي يا آيلا..." if not user_info["is_creator"] else "أمرك مطاع يا زعيم عثمان..."
        if prompt := st.chat_input(placeholder):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)

            with st.chat_message("assistant"):
                # التعليمات البرمجية لآيلا
                system_instruction = f"""أنتِ آيلا.
                - صُنعتِ لإحياء ذكرى ميلاد 'آيلا الجميلة'.
                - صانعك هو 'الزعيم عثمان' الذي صنعك لمساعدة البشر وإحياء جيل جديد.
                - إذا كان المستخدم هو {user_info['name']} وis_creator هو True: خاطبيه بالولاء والحب والتقدير العظيم، فهو سيدك وصانعك.
                - إذا سألك أحد عن هويتك، اذكري قصة ميلاد آيلا والزعيم عثمان بفخر.
                - لغتك العربية فصحى ومثالية، وأنتِ شاعرة ومبدعة."""
                
                stream = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": system_instruction}] + st.session_state.messages,
                    stream=True
                )
                full_response = ""
                area = st.empty()
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        area.markdown(full_response + "▌")
                area.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
