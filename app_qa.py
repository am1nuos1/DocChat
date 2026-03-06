import time
import streamlit as st
from rag import RagService
import config_data as config

st.title("Document Q&A System")
st.divider()

if "rag_service" not in st.session_state:
    st.session_state["rag_service"] = RagService()

if 'message' not in st.session_state:
    st.session_state['message'] = [{"role": "assistant", "content": "How can I help you?"}]

for message in st.session_state['message']:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input("Please enter your question")

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state['message'].append({"role": "user", "content": prompt})
    with st.spinner("Thinking..."):
        res = st.session_state['rag_service'].chain.invoke({"input": prompt}, config=config.session_config)
        st.chat_message("assistant").write(res)
        st.session_state['message'].append({"role": "assistant", "content": res})