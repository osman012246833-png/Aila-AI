import streamlit as st
from groq import Groq

# --- 1. إعدادات النظام العميقة ---
st.set_page_config(page_title="Aila AI | آيلا", page_icon="💠", layout="centered")

# محاكاة حفظ البيانات (للحفظ الدائم الحقيقي يلزم ربط Firebase بس هنا عملت أقصى ثبات)
if "user_data" not in st.session_state: st.session_state.user_data = None
if "history" not in st.session_state: st.session_state.history = []
if "messages" not in st.session_state: st.session_state.messages = []
if "counter" not in st.session_state: st.session_state.counter = 0
if "theme" not in st.session_state: st.session_state.theme = "dark"

client = Groq(api_key="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")

# --- 2. محرك التنسيق (تغيير الألوان حسب الوضع) ---
bg_color = "#000000" if st.session_state.theme == "dark" else "#FFFFFF"
text_color = "#FFFFFF" if st.session_state.theme == "dark" else "#000000"
sidebar_bg = "#111111" if st.session_state.theme == "dark" else "#f0f2f6"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    .stApp {{ background-color: {bg_color}; color: {text_color}; font-family: 'Cairo', sans-serif; transition: 0.3s; }}
    [data-testid="stSidebar"] {{ background-color: {sidebar_bg}; }}
    
    /* أيقونات المحادثة الجديدة */
    .user-avatar {{ width: 45px; height: 45px; border-radius: 50%; border: 2px solid #00d4ff; }}
    .aila-avatar {{ width: 45px; height: 45px; border-radius: 50%; border: 2px solid #ff00ff; }}
    
    /* تنسيق الفقاعات لمنع التداخل (إصلاح الدوائر الخ0راء) */
    .stChatMessage {{ 
        padding: 15px; border-radius: 15px; margin-bottom: 10px;
        background-color: {"#1a1a1a" if st.session_state.theme == "dark" else "#f9f9f9"};
        border: 1px solid #333;
    }}

    .header-logo {{
        text-align: center; border: 4px solid #00d4ff; width: 100px; height: 100px;
        border-radius: 50%; margin: 0 auto; box-shadow: 0 0 20px #00d4ff;
    }}
    
    /* أزرار السبحة المطورة */
    .tasbih-btn {{
        background: linear-gradient(45deg, #00d4ff, #0055ff);
        color: white; border: none; padding: 15px 30px;
        border-radius: 50px; font-weight: bold; cursor: pointer; width: 100%;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. وظائف الذكاء والتعرف على الجنس ---
def analyze_user(name):
    female_names = ["رحمة", "زينب", "فاطمة", "سارة", "مريم", "ليلى", "هناء"]
    is_female = any(n in name for n in female_names) or name.endswith(('ة', 'ا', 'ى'))
    return ("تحدثي معي يا آيلا", "أنثى") if is_female else ("تحدث مع يا آيلا", "ذكر")

# --- 4. القائمة الجانبية (تسجيل الدخول والإعدادات) ---
with st.sidebar:
    if st.session_state.user_data:
        st.write(f"👤 مرحباً، **{st.session_state.user_data['name']}**")
        st.write(f"📧 {st.session_state.user_data['email']}")
        
        st.session_state.theme = st.selectbox("🌓 وضع الإضاءة", ["dark", "light"], index=0 if st.session_state.theme == "dark" else 1)
        
        if st.button("🚪 تسجيل الخروج"):
            st.session_state.user_data = None
            st.rerun()
            
        st.write("---")
        if st.button("📿 ركن العبادة الشامل"): st.session_state.page = "tasbih"; st.rerun()
        if st.button("💬 المحادثة الرئيسية"): st.session_state.page = "chat"; st.rerun()
        if st.button("🗑️ مسح السجل"): st.session_state.history = []; st.rerun()
    else:
        st.subheader("🔐 تسجيل الدخول")

# --- 5. منطق الصفحات ---

# أ- صفحة التسجيل (بالبريد)
if not st.session_state.user_data:
    st.markdown("<h2 style='text-align:center;'>💠 مرحباً بك في عالم آيلا</h2>", unsafe_allow_html=True)
    email = st.text_input("البريد الإلكتروني الأصلي", placeholder="example@mail.com")
    name = st.text_input("الاسم الكريم", placeholder="اكتب اسمك ليتم التعرف عليك")
    if st.button("دخول آمن"):
        if "@" in email and len(name) > 2:
            st.session_state.user_data = {"name": name, "email": email}
            st.rerun()
        else:
            st.error("يرجى إدخال بريد صحيح واسم حقيقي")

# ب- ركن العبادة (تحديث ضخم)
elif st.session_state.page == "tasbih":
    st.title("📿 ركن العبادة والسكينة")
    st.markdown(f"<h1 style='text-align:center; font-size: 80px;'>{st.session_state.counter}</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✨ سبّح الآن", use_container_width=True): st.session_state.counter += 1; st.rerun()
    with col2:
        if st.button("🔄 تصفير سريع", use_container_width=True): st.session_state.counter = 0; st.rerun()
        
    st.write("---")
    st.subheader("📖 أذكار وأدعية مضاعفة")
    azkar = [
        "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ ، سُبْحَانَ اللَّهِ الْعَظِيمِ", "أستغفر الله العظيم وأتوب إليه (100 مرة)",
        "لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ الْعَلِيِّ الْعَظِيمِ", "اللهم صلِّ وسلم على نبينا محمد",
        "رضيت بالله رباً وبالإسلام ديناً وبمحمد ﷺ نبياً", "لا إله إلا أنت سبحانك إني كنت من الظالمين",
        "اللهم إني أسألك علماً نافعاً ورزقاً طيباً", "يا حي يا قيوم برحمتك أستغيث",
        "حسبي الله ونعم الوكيل", "اللهم بك أصبحنا وبك أمسينا",
        "سبحان الله (33)، الحمد لله (33)، الله أكبر (34)", "أعوذ بكلمات الله التامات من شر ما خلق",
        "بسم الله الذي لا يضر مع اسمه شيء", "اللهم إني أعوذ بك من الهم والحزن"
    ] * 5 # تكرار الكمية لزيادة المحتوى
    for z in azkar:
        st.markdown(f"<div style='background:#222; padding:10px; margin:5px; border-right:4px solid #00d4ff;'>{z}</div>", unsafe_allow_html=True)

# ج- الدردشة الذكية
else:
    placeholder, gender = analyze_user(st.session_state.user_data['name'])
    
    st.markdown(f"""
        <div style="text-align:center;">
            <div class="header-logo"></div>
            <h2 style="margin-top:10px;">آيلا | Aila AI</h2>
            <p style="color:#00d4ff;">بإشراف الزعيم عثمان | 20/11/2008</p>
        </div>
    """, unsafe_allow_html=True)

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input(placeholder):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            full_response = ""
            sys_prompt = f"أنتِ آيلا. المستخدم هو {st.session_state.user_data['name']} وهو {gender}. خاطبيه بناءً على ذلك بدقة. أسلوبك فخم ومنسق جداً."
            
            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": sys_prompt}] + st.session_state.messages,
                stream=True
            )
            res_area = st.empty()
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    res_area.markdown(full_response + "▌")
            res_area.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
            # الحذف التلقائي بعد 25
            if len(st.session_state.history) > 25: st.session_state.history.pop(0)
