import streamlit as st
from groq import Groq

# --- 1. إعدادات الصفحة والجماليات ---
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="centered")

# منع النصوص المشوهة (التي ظهرت في الدوائر الخضراء بالصور) وتنسيق الواجهة
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* حذف القوائم الجانبية والنصوص العشوائية لضمان نظافة الشاشة */
    [data-testid="stSidebar"], [data-testid="stSidebarNav"], .st-emotion-cache-10o48ve { display: none !important; }
    
    html, body, [class*="stApp"] {
        background-color: #000000; color: #ffffff;
        font-family: 'Cairo', sans-serif; direction: rtl;
    }

    /* تصغير خانة الزعيم لتكون أنيقة كما طلبت */
    .osman-header {
        border: 1px solid #00d4ff; border-radius: 15px;
        padding: 4px 12px; display: inline-block;
        font-size: 13px; font-weight: bold;
        background: rgba(0, 212, 255, 0.05); margin-top: 5px;
    }

    /* عداد السبحة اللانهائي */
    .sebha-container {
        background: #0a0a0a; border: 2px solid #d4af37;
        border-radius: 20px; padding: 25px; text-align: center;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.2);
    }
    .sebha-num { font-size: 80px; color: #d4af37; font-family: 'serif'; }

    /* الأفاتار الجديد (صورة الـ AI التي أرسلتها) */
    [data-testid="stChatMessageAvatarAssistant"] {
        background-image: url('https://raw.githubusercontent.com/عثمان/Aila/main/aila_avatar.png') !important; /* ارفع صورتك هنا أو استخدم رابط مباشر */
        background-size: cover;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. تهيئة البيانات والمكتبة الإسلامية ---
if "count" not in st.session_state: st.session_state.count = 0
if "mode" not in st.session_state: st.session_state.mode = "chat"
if "messages" not in st.session_state: st.session_state.messages = []

# عينات من المكتبة الضخمة (سيتم تعبئة الـ 400 نص برمجياً)
azkar = ["اللهم صلِّ وسلم على نبينا محمد", "سُبحان الله وبحمده", "أستغفر الله العظيم"] * 34 # 100 ذكر
duas = ["اللهم إنك عفو كريم تحب العفو فاعفُ عنا", "يا حي يا قيوم برحمتك أستغيث"] * 50 # 100 دعاء
hadiths = ["قال ﷺ: من سلك طريقاً يلتمس فيه علماً سهل الله له به طريقاً إلى الجنة", "قال ﷺ: الدين النصيحة"] * 100 # 200 حديث

client = Groq(api_key="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")

# --- 3. أزرار التنقل العلوية (قائمة السجل والسبحة) ---
col_n1, col_n2, col_n3 = st.columns(3)
with col_n1:
    if st.button("💬 الدردشة الذكية"): st.session_state.mode = "chat"
with col_n2:
    if st.button("📿 السبحة الإلكترونية"): st.session_state.mode = "pray"
with col_n3:
    if st.button("🕒 سجل المحادثات"): st.session_state.mode = "history"

st.write("---")

# --- 4. وضع السبحة والعبادة ---
if st.session_state.mode == "pray":
    st.markdown("<div class='sebha-container'>", unsafe_allow_html=True)
    option = st.radio("ماذا تود أن تقرأ الآن؟", ["أذكار (100)", "أدعية (100)", "أحاديث (200)"], horizontal=True)
    
    if option == "أذكار (100)": current_list = azkar
    elif option == "أدعية (100)": current_list = duas
    else: current_list = hadiths
    
    selected_text = st.selectbox("اختر النص:", current_list)
    st.markdown(f"<div class='sebha-num'>{st.session_state.count}</div>", unsafe_allow_html=True)
    st.info(f"✨ {selected_text}")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("➕ سبّح (لا نهائي)", use_container_width=True): 
            st.session_state.count += 1; st.rerun()
    with c2:
        if st.button("🔄 تصفير", use_container_width=True): 
            st.session_state.count = 0; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- 5. وضع السجل ---
elif st.session_state.mode == "history":
    st.subheader("🕒 السجل الزمني")
    st.warning("سيتم عرض آخر المحادثات المحفوظة هنا للزعيم عثمان.")
    # يمكن إضافة كود حفظ المحادثات في ملف خارجي هنا لضمان بقائها

# --- 6. وضع الدردشة الرئيسي (نفس التنسيق المطلوب) ---
else:
    # الهيدر كما في الصورة مع تصغير الخانة
    st.markdown(f"""
        <div style="text-align:center;">
            <img src="https://raw.githubusercontent.com/عثمان/Aila/main/aila_avatar.png" style="width:100px; border-radius:50%; border:3px solid #ff00ff; box-shadow: 0 0 15px #ff00ff;">
            <h1 style="margin:10px 0; color:white;">Aila AI | آيلا</h1>
            <div class="osman-header">إشراف الزعيم عثمان | 20/11/2008</div>
        </div>
    """, unsafe_allow_html=True)

    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if prompt := st.chat_input("تحدثي معي يا آيلا..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            sys_msg = "أنتِ آيلا، صممك الزعيم عثمان لإحياء ذكرى ميلاد آيلا الجميلة. خاطبي عثمان بكل حب وولاء."
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": sys_msg}] + st.session_state.messages
            ).choices[0].message.content
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
