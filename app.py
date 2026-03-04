import streamlit as st
from groq import Groq
import time

# --- 1. إعدادات الصفحة والهوية ---
st.set_page_config(page_title="Aila AI | آيلا", page_icon="💠", layout="wide")

# --- 2. التصميم (CSS) مطابق تماماً للصور ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    html, body, [class*="stApp"] {
        background-color: #000000;
        color: #FFFFFF;
        font-family: 'Cairo', sans-serif;
        direction: rtl;
    }

    /* فقاعات الدردشة */
    .user-bubble {
        background-color: #2f2f2f;
        padding: 15px 20px;
        border-radius: 20px;
        margin: 10px 0;
        display: inline-block;
        max-width: 80%;
        float: left; /* المستخدم يسار */
        font-size: 20px;
    }

    .ai-bubble {
        background-color: transparent;
        padding: 15px 5px;
        margin: 10px 0;
        display: block;
        width: 100%;
        font-size: 20px;
        line-height: 1.6;
    }

    /* السبحة الإلكترونية */
    .tasbih-box {
        text-align: center;
        background: linear-gradient(145deg, #1a1a1a, #000);
        padding: 40px;
        border-radius: 50%;
        width: 250px;
        height: 250px;
        margin: auto;
        border: 4px solid #00ffff;
        box-shadow: 0 0 30px #00ffff55;
        display: flex;
        flex-direction: column;
        justify-content: center;
        cursor: pointer;
    }

    /* شريط الإدخال السفلي */
    div[data-testid="stChatInput"] {
        bottom: 20px !important;
        background-color: #1e1e1e !important;
        border: 1px solid #333 !important;
        border-radius: 30px !important;
    }

    /* الأزرار */
    .stButton>button {
        border-radius: 20px !important;
        border: 1px solid #444 !important;
        background-color: #1e1e1e !important;
        color: white !important;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. إدارة الذاكرة والبيانات ---
if "messages" not in st.session_state: st.session_state.messages = []
if "counter" not in st.session_state: st.session_state.counter = 0
if "page" not in st.session_state: st.session_state.page = "chat"
if "is_authenticated" not in st.session_state: st.session_state.is_authenticated = False

client = Groq(api_key="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")

# --- 4. نظام التبديل بين الشاشات ---
def go_to_tasbih(): st.session_state.page = "tasbih"
def go_to_chat(): st.session_state.page = "chat"

# --- 5. واجهة تسجيل الدخول ---
if not st.session_state.is_authenticated:
    st.markdown("<h1 style='text-align:center;'>💠 آيلا الذكية</h1>", unsafe_allow_html=True)
    name = st.text_input("ادخل اسمك للبدء", placeholder="مثلاً: الزعيم عثمان")
    if st.button("دخول"):
        st.session_state.is_authenticated = True
        st.session_state.user_name = name
        st.rerun()

# --- 6. صفحة السبحة (ركن العبادة) ---
elif st.session_state.page == "tasbih":
    st.markdown("<h2 style='text-align:center;'>📿 ركن التسبيح والذكر</h2>", unsafe_allow_html=True)
    st.write("---")
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown(f"""
            <div class="tasbih-box">
                <small style="color:#00ffff;">اضغط للعد</small>
                <h1 style="font-size: 80px; margin:0;">{st.session_state.counter}</h1>
                <p>سُبْحَانَ اللَّهِ</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("➕ تسبيح"):
            st.session_state.counter += 1
            st.rerun()
        
        if st.button("🔄 تصفير العداد"):
            st.session_state.counter = 0
            st.rerun()
            
    if st.button("⬅️ العودة للدردشة"):
        go_to_chat()
        st.rerun()

# --- 7. صفحة الدردشة الرئيسية ---
else:
    # القائمة الجانبية (السجل طويل المدى والشعارات)
    with st.sidebar:
        st.markdown(f"### 👑 {st.session_state.user_name}")
        st.write("---")
        st.button("📿 ركن التسبيح والعبادة", on_click=go_to_tasbih)
        st.write("---")
        st.markdown("### 🕒 سجل المحادثات")
        if st.button("🗑️ مسح السجل"):
            st.session_state.messages = []
            st.rerun()
        for i, msg in enumerate(st.session_state.messages[::2]):
            st.caption(f"💬 {msg['content'][:20]}...")

    # واجهة الترحيب
    if not st.session_state.messages:
        st.markdown(f"<h1 style='text-align:center; margin-top:100px;'>كيف يمكنني مساعدتك اليوم يا {st.session_state.user_name}؟</h1>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📖 اسأل عن آية أو حديث"):
                st.session_state.messages.append({"role": "user", "content": "أعطني موعظة دينية قصيرة"})
                st.rerun()
            if st.button("💡 فكرة مشروع برمجي"):
                st.session_state.messages.append({"role": "user", "content": "اقترح علي فكرة تطبيق ذكي"})
                st.rerun()
        with col2:
            if st.button("🛡️ نصيحة في الأمن السيبراني"):
                st.session_state.messages.append({"role": "user", "content": "كيف أحمي حساباتي؟"})
                st.rerun()
            if st.button("📝 تلخيص نص طويل"):
                st.session_state.messages.append({"role": "user", "content": "سأعطيك نصاً لتقومي بتلخيصه"})
                st.rerun()

    # عرض الرسائل بسلوب انسيابي
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div style="text-align:left;"><div class="user-bubble">{msg["content"]}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="ai-bubble"><b>آيلا:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)

    # حقل الإدخال
    if prompt := st.chat_input("تحدث مع آيلا..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

    # توليد الرد (فقط إذا كانت آخر رسالة من المستخدم)
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.markdown('<div class="ai-bubble"><b>آيلا:</b><br></div>', unsafe_allow_html=True):
            placeholder = st.empty()
            full_response = ""
            
            # تعليمات النظام (دين + ذكاء + احترام للصانع)
            sys_prompt = (
                "أنتِ آيلا AI. رفيقة ذكية ومثقفة. لديكِ علم واسع بالإسلام وتاريخه. "
                "أسلوبك فخم، هادئ، ومساعد. إذا كان المستخدم هو الزعيم عثمان، "
                "خاطبيه بلقبه المفضل بكل احترام وتواضع."
            )

            try:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": sys_prompt}] + st.session_state.messages,
                    stream=True
                )
                for chunk in completion:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        placeholder.markdown(full_response + "▌")
                
                placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"عذراً، هناك ضغط على المحرك. الخطأ: {e}")
