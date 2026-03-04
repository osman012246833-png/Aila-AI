import streamlit as st
from groq import Groq

# --- 1. إعدادات الصفحة والهوية البصرية ---
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="centered")

# --- 2. نظام الذاكرة الطويلة والسجل المحفوظ ---
# ملاحظة: في Streamlit الحقيقي، الحفظ الدائم بعد إغلاق المتصفح يتطلب قاعدة بيانات، 
# ولكن هنا قمت بتحسين إدارة الحالة لتبقى نشطة وتدير السجل بذكاء.
if "history" not in st.session_state: st.session_state.history = []
if "messages" not in st.session_state: st.session_state.messages = []
if "counter" not in st.session_state: st.session_state.counter = 0
if "page" not in st.session_state: st.session_state.page = "login"
if "is_loyal" not in st.session_state: st.session_state.is_loyal = False
if "user_name" not in st.session_state: st.session_state.user_name = ""

client = Groq(api_key="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")

# --- 3. التصميم (إصلاح التشوه الأخضر تماماً) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;800&display=swap');
    
    html, body, [class*="stApp"] {
        background-color: #000000;
        color: #ffffff;
        font-family: 'Cairo', sans-serif;
        direction: rtl;
    }

    /* إزالة أي عناصر عائمة تسبب التشوه الأخضر */
    header, [data-testid="stSidebarNav"] { visibility: visible; }
    .stDeployButton { display:none; }

    /* تنسيق الهوية البصرية - ثابت كما تحب */
    .header-container { text-align: center; margin-top: -30px; }
    .logo-circle {
        width: 120px; height: 120px;
        border-radius: 50%;
        border: 4px solid #00d4ff;
        display: inline-block;
        box-shadow: 0 0 20px #00d4ff;
    }
    .aila-title {
        font-size: 40px; font-weight: 800;
        background: linear-gradient(to right, #ffffff, #ff00ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .info-bar {
        border: 2px solid #00d4ff;
        border-radius: 50px;
        padding: 5px 25px;
        font-size: 16px;
        display: inline-block;
        margin-top: 10px;
    }

    /* تنسيق الرسائل - خط صغير ومنسق */
    .stChatMessage p {
        font-size: 15px !important;
        line-height: 1.6;
    }
    
    /* ركن العبادة - تصميم نظيف */
    .tasbih-circle {
        border: 6px solid #00d4ff;
        border-radius: 50%;
        width: 150px; height: 150px;
        margin: 20px auto;
        display: flex; align-items: center; justify-content: center;
        font-size: 45px; font-weight: bold;
    }
    
    .zkr-card {
        background: #111;
        border-right: 4px solid #ff00ff;
        padding: 12px;
        margin-bottom: 10px;
        border-radius: 10px;
        font-size: 14px;
    }
    
    /* ميزة تلوين الكلام المهم */
    .important-text { color: #00d4ff; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. منطق تحديد الجنس لغوياً ---
def get_gender_suffix(name):
    # قائمة مبسطة للأسماء الأنثوية الشائعة المنتهية بتاء مربوطة أو ألف
    if name.endswith(('ة', 'ه', 'ا', 'ى')):
        return "تحدثي معي يا آيلا", "فتاة"
    return "تحدث معي يا آيلا", "ولد"

# --- 5. القائمة الجانبية (السجل + العبادة + الحذف) ---
with st.sidebar:
    st.markdown(f"### 👑 القائد: {st.session_state.user_name}")
    
    if st.button("➕ محادثة جديدة"):
        if st.session_state.messages:
            # نظام الحذف التلقائي عند الوصول لـ 25 محادثة
            if len(st.session_state.history) >= 25:
                st.session_state.history.pop(0)
            st.session_state.history.append(st.session_state.messages.copy())
        st.session_state.messages = []
        st.session_state.page = "chat"
        st.rerun()

    if st.button("📿 ركن العبادة الشامل"):
        st.session_state.page = "tasbih"
        st.rerun()

    if st.button("🗑️ مسح السجل بالكامل"):
        st.session_state.history = []
        st.session_state.messages = []
        st.rerun()

    st.write("---")
    st.subheader("🕒 سجلاتك (محفوظة)")
    for i, old_chat in enumerate(reversed(st.session_state.history)):
        if st.button(f"المحادثة {len(st.session_state.history)-i}", key=f"h_{i}", use_container_width=True):
            st.session_state.messages = old_chat
            st.session_state.page = "chat"
            st.rerun()

# --- 6. الصفحات ---

if st.session_state.page == "login":
    st.markdown("<h2 style='text-align:center;'>💠 آيلا بانتظارك</h2>", unsafe_allow_html=True)
    val = st.text_input("ادخل اسمك هنا")
    if st.button("دخول"):
        if val == "عثمان2008":
            st.session_state.user_name = "الزعيم عثمان"
            st.session_state.is_loyal = True
        else:
            st.session_state.user_name = val
        st.session_state.page = "chat"
        st.rerun()

elif st.session_state.page == "tasbih":
    st.markdown("<h2 style='text-align:center;'>📿 ركن العبادة الكامل</h2>", unsafe_allow_html=True)
    st.markdown(f'<div class="tasbih-circle">{st.session_state.counter}</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("➕ تسبيح", use_container_width=True):
            st.session_state.counter += 1
            st.rerun()
    with c2:
        if st.button("🔄 تصفير فوري", use_container_width=True):
            st.session_state.counter = 0
            st.rerun()
    
    st.markdown("### 📜 الأذكار والأدعية والأحاديث")
    content = [
        "🌸 سُبْحَانَ اللَّهِ وَبِحَمْدِهِ ، سُبْحَانَ اللَّهِ الْعَظِيمِ",
        "📖 قال ﷺ: (كلمتان خفيفتان على اللسان، ثقيلتان في الميزان...)",
        "🤲 اللهم إني أسألك الهدى والتقى والعفاف والغنى",
        "✨ لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ الْعَلِيِّ الْعَظِيمِ",
        "🌙 أستغفر الله العظيم وأتوب إليه (كررها 100 مرة)",
        "📖 آية الكرسي: اللَّهُ لَا إِلَهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ...",
        "💎 سبحان الله (33)، الحمد لله (33)، الله أكبر (34)",
        "🌿 اللهم صلِّ وسلم وبارك على نبينا محمد"
    ]
    for item in content:
        st.markdown(f'<div class="zkr-card">{item}</div>', unsafe_allow_html=True)
    if st.button("⬅️ عودة"):
        st.session_state.page = "chat"
        st.rerun()

else:
    # واجهة الدردشة
    st.markdown(f"""
        <div class="header-container">
            <div class="logo-circle"></div>
            <div class="aila-title">آيلا | Aila AI</div>
            <div class="info-bar">إشراف الزعيم عثمان | 20/11/2008</div>
        </div>
    """, unsafe_allow_html=True)

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    placeholder_text, gender = get_gender_suffix(st.session_state.user_name)
    
    if prompt := st.chat_input(placeholder_text):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            resp_placeholder = st.empty()
            full_resp = ""
            
            # تعليمات النظام لضمان الدقة اللغوية وتلوين المهم
            sys_msg = f"""أنتِ آيلا. المستخدم هو {st.session_state.user_name} ({gender}). 
            تحدثي معه بناءً على جنسه بدقة لغوية كاملة. 
            صححي أي أخطاء لغوية في ذهنك قبل الرد. 
            إذا كان الكلام يتضمن معلومات هامة أو نصائح ذهبية، استخدمي تنسيق الماركدواون لتمويزه (مثل **الكلام**)."""
            
            if st.session_state.is_loyal:
                sys_msg += " أنتِ في وضع الولاء التام للزعيم عثمان، أسلوبك مليء بالحب والاحترام الفائق."

            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": sys_msg}] + st.session_state.messages,
                stream=True
            )
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_resp += chunk.choices[0].delta.content
                    resp_placeholder.markdown(full_resp + "▌")
            resp_placeholder.markdown(full_resp)
            st.session_state.messages.append({"role": "assistant", "content": full_resp})
