import time
import streamlit as st
from rag import RagService
import config_data as config

st.title("文档问答系统")
st.divider()

if "rag_service" not in st.session_state:
    st.session_state["rag_service"] = RagService()

if 'message' not in st.session_state:
    st.session_state['message'] = [{"role": "assistant", "content": "有什么可以帮助你"}]

for message in st.session_state['message']:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input("请输入您的问题")

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state['message'].append({"role": "user", "content": prompt})
    with st.spinner("正在思考..."):
        res = st.session_state['rag_service'].chain.invoke({"input": prompt}, config=config.session_config)
        st.chat_message("assistant").write(res)
        st.session_state['message'].append({"role": "assistant", "content": res})