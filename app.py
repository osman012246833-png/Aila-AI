import streamlit as st
from groq import Groq
import time

# 1. إعدادات الصفحة والأيقونة
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="centered")

# 2. التصميم الجديد (مطابق لصور Gemini & ChatGPT)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;800&display=swap');
    
    html, body, [class*="stApp"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl; text-align: right;
        background-color: #0b0b0b; /* أسود عميق */
        color: #e3e3e3 !important;
    }

    /* تحسين شكل فقاعات الدردشة */
    .stChatMessage {
        background-color: transparent !important;
        padding: 20px 0 !important;
    }

    /* نص المستخدم */
    [data-testid="stChatMessageUser"] {
        background-color: #2f2f2f !important;
        border-radius: 25px !important;
        padding: 15px 25px !important;
        margin-bottom: 15px;
        width: fit-content;
        margin-right: auto; /* لليمين */
    }

    /* نص آيلا */
    [data-testid="stChatMessageAssistant"] {
        margin-bottom: 25px;
    }

    /* حجم الخط وتوضيحه */
    .stChatMessage p, .stMarkdown p {
        font-size: 20px !important;
        line-height: 1.6 !important;
        color: #e3e3e3 !important;
    }

    /* تصميم شريط الإدخال السفلي */
    [data-testid="stChatInputContainer"] {
        border-radius: 30px !important;
        border: 1px solid #444 !important;
        background-color: #1e1e1e !important;
        padding: 5px 15px !important;
    }

    .main-header {
        text-align: center;
        margin-bottom: 50px;
        margin-top: 30px;
    }

    .main-header h1 {
        font-size: 3rem;
        font-weight: 800;
        background: -webkit-linear-gradient(#00ffff, #ff00ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* الأزرار السريعة مثل Gemini */
    .quick-btn {
        display: inline-block;
        padding: 10px 20px;
        margin: 5px;
        background: #1e1e1e;
        border: 1px solid #444;
        border-radius: 15px;
        font-size: 16px;
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. المحرك والتهيئة
client = Groq(api_key="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")
SECRET_CODE = "osman 6/11/2008"

if "messages" not in st.session_state: st.session_state.messages = []
if "is_authenticated" not in st.session_state: st.session_state.is_authenticated = False

# 4. نظام الدخول
if not st.session_state.is_authenticated:
    st.markdown('<div class="main-header"><h1>آيلا | Aila AI</h1></div>', unsafe_allow_html=True)
    st.markdown("<center><h3 style='color:#888;'>مرحباً بك.. ادخل الرمز للبدء</h3></center>", unsafe_allow_html=True)
    user_input = st.text_input("", placeholder="اكتب اسمك أو الرمز السري هنا...", key="login_pass")
    
    if st.button("بدء المحادثة"):
        if user_input == SECRET_CODE:
            st.session_state.is_authenticated = True
            st.session_state.user_display_name = "الزعيم عثمان"
            st.session_state.is_maker = True
            st.rerun()
        elif user_input:
            st.session_state.is_authenticated = True
            st.session_state.user_display_name = user_input
            st.session_state.is_maker = False
            st.rerun()
else:
    # رأس الصفحة بعد الدخول
    st.markdown(f'<div style="text-align:left; color:#888; font-size:14px;">إشراف عثمان | 20/11/2008</div>', unsafe_allow_html=True)
    
    if len(st.session_state.messages) == 0:
        st.markdown(f"<h1 style='text-align:center; margin-top:50px;'>كيف يمكنني مساعدتك اليوم، {st.session_state.user_display_name}؟</h1>", unsafe_allow_html=True)
        # أزرار سريعة
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="quick-btn">💡 اسأل عن تاريخ الإسلام</div>', unsafe_allow_html=True)
            st.markdown('<div class="quick-btn">📖 تفسير آية قرآنية</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="quick-btn">🛠️ مساعدة برمجية</div>', unsafe_allow_html=True)
            st.markdown('<div class="quick-btn">✍️ كتابة مقال إبداعي</div>', unsafe_allow_html=True)

    # عرض الدردشة
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # الإدخال
    if prompt := st.chat_input("طرح سؤالك على آيلا..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # تعليمات المعرفة الدينية والإسلامية
            religion_context = (
                "أنتِ آيلا AI، خبيرة ومثقفة جداً. لديكِ معرفة عميقة بالأديان السماوية، "
                "وبالأخص الدين الإسلامي (القرآن، السنة، الفقه، والتاريخ الإسلامي). "
                "عند الحديث عن الدين، كوني محترمة، دقيقة، واستخدمي لغة فصيحة وجميلة. "
                "إذا كان المستخدم هو 'الزعيم عثمان'، تحدثي معه كصانعك بكل تقدير."
            )
            
            full_response = ""
            placeholder = st.empty()
            
            try:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": religion_context}] + st.session_state.messages[-10:],
                    stream=True
                )
                
                for chunk in completion:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        placeholder.markdown(full_response + "▌")
                
                placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"خطأ: {e}")
