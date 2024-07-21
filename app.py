import streamlit as st
import os
from document_analyzer import analyze_document

# Set page config
st.set_page_config(page_title="Document Analyzer", page_icon="📄")

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.title("Document Analyzer - Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "admin":
            st.session_state.logged_in = True
            st.success("Logged in successfully!")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

def main():
    st.title("Document Analyzer")
    
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
        st.write(file_details)
        
        if st.button("Analyze Document"):
            with st.spinner("Analyzing document..."):
                result = analyze_document(uploaded_file)
                st.markdown(result)

if __name__ == "__main__":
    if not st.session_state.logged_in:
        login()
    else:
        main()