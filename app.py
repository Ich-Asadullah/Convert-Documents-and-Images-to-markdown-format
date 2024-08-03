import streamlit as st
from dotenv import load_dotenv
from document_analyzer import get_pdf_page_count, analyze_document as analyze_document_azure
from openai_analyzer import process_pdf, process_image
import asyncio

load_dotenv()

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
            st.rerun()
        else:
            st.error("Invalid username or password")

async def process_file_openai(file, file_type):
    if file_type == "pdf":
        results, total_cost, inp_tokens, res_tokens = await process_pdf(file)
        st.markdown("\n".join(results))
    else:  # image
        result, total_cost, inp_tokens, res_tokens = await process_image(file)
        st.markdown(result)
    st.write(f"Total cost: ${total_cost:.6f}")

def process_file_azure(file, file_type):
    result = analyze_document_azure(file)
    st.markdown(result)
    if file_type == "pdf":
        # Assuming we can get the number of pages from the result
        num_pages = get_pdf_page_count(file)
        try:
            cost = 0.001 * num_pages
        except:
            cost = num_pages
    else:  # image
        cost = 0.001
    st.write(f"Total cost: {cost}")

def main():
    st.title("Document Analyzer")
    
    analyzer_option = st.radio("Select Analyzer", ("Azure", "OpenAI"))
    
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
        st.write(file_details)
        
        file_type = "pdf" if uploaded_file.type == "application/pdf" else "image"
        
        if st.button("Analyze Document"):
            with st.spinner("Analyzing document..."):
                if analyzer_option == "Azure":
                    process_file_azure(uploaded_file, file_type)
                else:  # OpenAI
                    asyncio.run(process_file_openai(uploaded_file, file_type))

if __name__ == "__main__":
    if not st.session_state.logged_in:
        login()
    else:
        main()