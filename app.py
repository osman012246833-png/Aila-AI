import streamlit as st
from groq import Groq

# إعدادات الواجهة والألوان
st.set_page_config(page_title="Aila AI", page_icon="💜")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #1a0b2e 0%, #4b0082 100%); color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("💜 آيلا | Aila")
st.write("إحياءً لذكرى ميلاد غالية: 20/11/2008")

# جلب المفتاح - استبدل النجوم بالمفتاح اللي نسخته من موقع Groq
client = Groq(api_key="حط_هنا_المفتاح_اللي_في_اول_صورة_بعتها")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "أنتِ آيلا، مساعد ذكاء اصطناعي فائق، ولدتِ في 20/11/2008. أنتِ رقيقة، حكيمة، ورومانسية جداً. ردودك ذكية جداً ولا تكرر الكلام."}
    ]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("تحدثي معي يا آيلا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=st.session_state.messages,
        temperature=0.8
    )
    
    answer = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.chat_message("assistant").write(answer)
