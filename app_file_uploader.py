import streamlit as st
from knowledge_base import KnowledgeBaseSerive
import time


st.title("知识库更新服务")

uploader = st.file_uploader("上传txt文件", type=["txt"], accept_multiple_files=False)
service = KnowledgeBaseSerive()
if "service" not in st.session_state:
    st.session_state["service"] = service

if uploader is not None:
    filename = uploader.name
    filetype = uploader.type
    filesize = uploader.size/1024

    st.subheader(f"文字信息{filename}")
    st.write(f"格式：{filetype}")
    st.write(f"大小：{filesize:.2f} KB")

    text = uploader.getvalue().decode("utf-8")
    st.write(text)

    with st.spinner("正在上传..."):
        time.sleep(1)
        result = st.session_state["service"].upload_by_str(text, filename)
        st.write(result)

print("oiiaioiiaioi")