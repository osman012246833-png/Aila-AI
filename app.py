import streamlit as st
from groq import Groq

# --- 1. إعدادات الصفحة والجماليات ---
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stSidebar"], [data-testid="stSidebarNav"] { display: none !important; }
    html, body, [class*="stApp"] { background-color: #050505; color: #ffffff; font-family: 'Cairo', sans-serif; direction: rtl; }
    
    .aila-title {
        font-size: 50px; font-weight: 900; color: #ff00ff;
        text-shadow: 0 0 15px #ff00ff; text-align: center; margin-bottom: 0px;
    }
    
    .osman-badge {
        border: 2px solid #00d4ff; border-radius: 20px;
        padding: 5px 25px; display: inline-block;
        font-size: 16px; color: #ffffff; background: rgba(0, 212, 255, 0.1);
        box-shadow: 0 0 10px #00d4ff;
    }
    
    .support-txt {
        font-size: 14px; color: #ff00ff; font-weight: bold;
        text-align: center; border-top: 1px dashed #444;
        padding-top: 10px; margin-top: 20px;
    }

    /* تحسين الأفاتار - لوجو AI فخم */
    [data-testid="stChatMessageAvatarAssistant"] {
        background-image: url('https://img.freepik.com/free-vector/ai-technology-brain-background-digital-transformation-concept_53876-117818.jpg') !important;
        background-size: cover; border: 2px solid #ff00ff;
    }
    [data-testid="stChatMessageAvatarUser"] {
        background-image: url('https://img.freepik.com/free-vector/user-blue-gradient-vector-icon-concept_53876-145591.jpg') !important;
        background-size: cover; border: 2px solid #00d4ff;
    }

    .prayer-card { background: #111; border: 1px solid #333; border-radius: 12px; padding: 10px; text-align: center; }
    .prayer-time { color: #00d4ff; font-weight: bold; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. دالة التوقيت والذكاء ---
def get_label(name):
    female_names = ["آية", "مريم", "سارة", "فاطمة", "نور", "ليلى", "آيلا", "هنا", "جنا", "ياسمين", "زينب", "رنا"]
    if any(fn in name for fn in female_names) or name.endswith(("ة", "ه")):
        return "تحدثي مع آيلا..."
    return "تحدث مع آيلا..."

# مواقيت صلاة بنظام 12 ساعة
prayer_times = {"الفجر": "04:45 ص", "الظهر": "12:05 م", "العصر": "03:25 م", "المغرب": "06:05 م", "العشاء": "07:25 م"}

if "user_data" not in st.session_state: st.session_state.user_data = {"name": "", "is_creator": False, "logged": False}
if "messages" not in st.session_state: st.session_state.messages = []

client = Groq(api_key="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")

# --- 3. واجهة الدخول ---
if not st.session_state.user_data["logged"]:
    st.markdown("<h2 style='text-align:center;'>💠 مرحباً بك في عالم آيلا الذكي</h2>", unsafe_allow_html=True)
    name_in = st.text_input("ادخل اسمك هنا:")
    if st.button("انطلق الآن"):
        if "عثمان" in name_in or "osman" in name_in.lower():
            st.session_state.user_data = {"name": "عثمان عصام", "is_creator": True, "logged": True}
        else:
            st.session_state.user_data = {"name": name_in, "is_creator": False, "logged": True}
        st.rerun()

else:
    # الهيدر الجديد الاحترافي
    st.markdown(f"""
        <div style="text-align:center; margin-bottom: 30px;">
            <div style="width:120px; height:120px; border-radius:50%; border:4px solid #ff00ff; display:inline-block; 
            background:url('https://img.freepik.com/free-vector/ai-technology-brain-background-digital-transformation-concept_53876-117818.jpg') no-repeat center; background-size:cover; box-shadow: 0 0 25px #ff00ff;"></div>
            <div class="aila-title">Aila AI | آيلا</div>
            <div class="osman-badge">إشراف: عثمان عصام | ابن بني سويف</div>
        </div>
    """, unsafe_allow_html=True)

    # مواقيت الصلاة (نظام 12 ساعة)
    with st.expander("🕌 مواقيت الصلاة بتوقيت القاهرة"):
        cols = st.columns(5)
        for i, (name, time) in enumerate(prayer_times.items()):
            cols[i].markdown(f"<div class='prayer-card'><b>{name}</b><br><span class='prayer-time'>{time}</span></div>", unsafe_allow_html=True)

    # --- منطقة الدردشة ---
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    input_placeholder = get_label(st.session_state.user_data["name"])
    if prompt := st.chat_input(input_placeholder):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            # تعليمات صارمة للغة العربية الفصحى ومنع اللغات الأخرى
            sys_prompt = (
                f"أنتِ آيلا، مساعد ذكي بليغ. المستخدم هو {st.session_state.user_data['name']}. "
                "تحدثي بالعربية الفصحى فقط. ممنوع استخدام أي كلمات أجنبية أو فيتنامية أو إنجليزية. "
                "اجعلي إجاباتك دقيقة ونقية لغوياً."
            )
            if st.session_state.user_data["is_creator"]: sys_prompt += " خاطبي عثمان بكل تبجيل كونه المطور الأصلي."

            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": sys_prompt}] + st.session_state.messages
            ).choices[0].message.content
            
            # رسالة الدعم بالاسم والمحافظة
            footer = f"\n\n<div class='support-txt'>إذا أعجبك المشروع، فلا تنسَ صانعه عثمان عصام ابن محافظة بني سويف من دعائك.</div>"
            st.markdown(res + footer, unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": res})
