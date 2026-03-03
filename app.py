import streamlit as st
from groq import Groq

# إعدادات الواجهة
st.set_page_config(page_title="Aila AI", page_icon="💜")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #1a0b2e 0%, #4b0082 100%); color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("💜 آيلا | Aila")
st.write("ذكري ميلاد غالية: 20/11/2008")

# المفتاح الصحيح
client = Groq(api_key="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")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "أنتِ آيلا، مساعدة ذكاء اصطناعي فائقة. ردودك ذكية جداً."}
    ]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("تحدثي مع آيلا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=st.session_state.messages,
    )
    answer = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.chat_message("assistant").write(answer)
