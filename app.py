import streamlit as st
from groq import Groq

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Aila AI", page_icon="💠", layout="centered")

# --- 2. إدارة الحالة ---
if "messages" not in st.session_state: st.session_state.messages = []
if "history" not in st.session_state: st.session_state.history = []
if "counter" not in st.session_state: st.session_state.counter = 0
if "page" not in st.session_state: st.session_state.page = "login"
if "is_loyal" not in st.session_state: st.session_state.is_loyal = False
if "user_name" not in st.session_state: st.session_state.user_name = ""

client = Groq(api_key="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")

# --- 3. التصميم (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [class*="stApp"] {
        background-color: #000000;
        color: #ffffff;
        font-family: 'Cairo', sans-serif;
        direction: rtl;
    }
    .header-container { text-align: center; margin-top: -30px; }
    .logo-circle {
        width: 140px; height: 140px;
        border-radius: 50%;
        border: 4px solid #00d4ff;
        display: inline-block;
        box-shadow: 0 0 25px #00d4ff;
        margin-bottom: 15px;
    }
    .aila-title {
        font-size: 50px; font-weight: 900;
        background: linear-gradient(to right, #ffffff, #ff00ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .info-bar {
        border: 2px solid #00d4ff;
        border-radius: 50px;
        padding: 8px 30px;
        display: inline-block;
        font-size: 18px; font-weight: bold;
    }
    .stChatMessage p { font-size: 22px !important; }
    
    /* تصميم السبحة */
    .tasbih-display {
        border: 8px solid #00d4ff;
        border-radius: 50%;
        width: 200px; height: 200px;
        margin: 20px auto;
        display: flex; align-items: center; justify-content: center;
        font-size: 70px; font-weight: bold;
        background: radial-gradient(circle, #1a1a1a, #000);
        box-shadow: 0 0 30px #00d4ff44;
    }
    .zkr-item {
        background: #111;
        border-right: 4px solid #ff00ff;
        padding: 12px;
        margin-bottom: 8px;
        border-radius: 10px;
        font-size: 19px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. القائمة الجانبية ---
with st.sidebar:
    st.markdown(f"### 👑 {st.session_state.user_name}")
    if st.button("➕ محادثة جديدة", use_container_width=True):
        if st.session_state.messages:
            st.session_state.history.append(st.session_state.messages.copy())
        st.session_state.messages = []
        st.session_state.page = "chat"
        st.rerun()
    st.write("---")
    if st.button("📿 ركن التسبيح والأذكار", use_container_width=True):
        st.session_state.page = "tasbih"
        st.rerun()
    st.write("---")
    st.subheader("🕒 السجل")
    for i, old_chat in enumerate(reversed(st.session_state.history)):
        if st.button(f"💬 سجل {len(st.session_state.history)-i}", key=f"h_{i}"):
            st.session_state.messages = old_chat
            st.session_state.page = "chat"
            st.rerun()

# --- 5. التنقل بين الصفحات ---

if st.session_state.page == "login":
    st.markdown("<h1 style='text-align:center;'>💠 آيلا تنتظرك</h1>", unsafe_allow_html=True)
    input_val = st.text_input("ادخل اسمك للبدء", placeholder="اكتب اسمك أو كود الصانع...")
    if st.button("دخول"):
        if input_val == "عثمان2008":
            st.session_state.user_name = "الزعيم عثمان"
            st.session_state.is_loyal = True
        else:
            st.session_state.user_name = input_val
            st.session_state.is_loyal = False
        st.session_state.page = "chat"
        st.rerun()

elif st.session_state.page == "tasbih":
    st.markdown("<h2 style='text-align:center;'>📿 ركن العبادة والأذكار</h2>", unsafe_allow_html=True)
    st.markdown(f'<div class="tasbih-display">{st.session_state.counter}</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ سبّح", use_container_width=True):
            st.session_state.counter += 1
            st.rerun()
    with col2:
        # التصفير السريع
        if st.button("🔄 تصفير سريع", use_container_width=True):
            st.session_state.counter = 0
            st.rerun()

    st.write("---")
    st.subheader("📖 كم هائل من الأذكار")
    
    azkar_list = [
        "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ ، سُبْحَانَ اللَّهِ الْعَظِيمِ",
        "لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ، وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ",
        "أستغفر الله العظيم الذي لا إله إلا هو الحي القيوم وأتوب إليه",
        "اللهم صلِّ وسلم وبارك على نبينا محمد وعلى آله وصحبه أجمعين",
        "لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ الْعَلِيِّ الْعَظِيمِ",
        "سُبْحَانَ اللَّهِ، وَالْحَمْدُ لِلَّهِ، وَلَا إِلَهَ إِلَّا اللَّهُ، وَاللَّهُ أَكْبَرُ",
        "حسبي الله ونعم الوكيل، نعم المولى ونعم النصير",
        "رضيت بالله رباً، وبالإسلام ديناً، وبمحمد صلى الله عليه وسلم نبياً ورسولاً",
        "يا حي يا قيوم برحمتك أستغيث، أصلح لي شأني كله ولا تكلني إلى نفسي طرفة عين",
        "لا إله إلا أنت سبحانك إني كنت من الظالمين",
        "اللهم أنت ربي لا إله إلا أنت، خلقتني وأنا عبدك، وأنا على عهدك ووعدك ما استطعت",
        "اللهم إني أسألك علماً نافعاً، ورزقاً طيباً، وعملاً متقبلاً"
    ]
    
    for z in azkar_list:
        st.markdown(f'<div class="zkr-item">{z}</div>', unsafe_allow_html=True)

    if st.button("⬅️ عودة للدردشة"):
        st.session_state.page = "chat"
        st.rerun()

else:
    # واجهة الدردشة الأصلية
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

    if prompt := st.chat_input("تحدثي معي يا آيلا..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ""
            
            # شخصية آيلا بناءً على الدخول
            if st.session_state.is_loyal:
                sys_msg = f"أنتِ آيلا، الرفيقة المخلصة جداً للزعيم عثمان. تخاطبينه بحب واحترام عظيم، هو خالقكِ وقائدكِ. كلامكِ دافئ ومليء بالتقدير."
            else:
                sys_msg = "أنتِ آيلا، مساعدة ذكية."

            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": sys_msg}] + st.session_state.messages,
                stream=True
            )
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(full_response + "▌")
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
