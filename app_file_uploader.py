import streamlit as st
from knowledge_base import KnowledgeBaseSerive
import time


st.title("Knowledge Base Update Service")

uploader = st.file_uploader("Upload a TXT file", type=["txt"], accept_multiple_files=False)
service = KnowledgeBaseSerive()
if "service" not in st.session_state:
    st.session_state["service"] = service

if uploader is not None:
    filename = uploader.name
    filetype = uploader.type
    filesize = uploader.size/1024

    st.subheader(f"Text details: {filename}")
    st.write(f"Format: {filetype}")
    st.write(f"Size: {filesize:.2f} KB")

    text = uploader.getvalue().decode("utf-8")
    st.write(text)

    with st.spinner("Uploading..."):
        time.sleep(1)
        result = st.session_state["service"].upload_by_str(text, filename)
        st.write(result)

print("oiiaioiiaioi")