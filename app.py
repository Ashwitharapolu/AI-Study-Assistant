import streamlit as st
import sys
import os

# Add src to path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from rag import RAGPipeline

# Page config
st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="wide"
)

# Initialize RAG pipeline in session state
if "rag" not in st.session_state:
    st.session_state.rag = RAGPipeline()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False

if "num_chunks" not in st.session_state:
    st.session_state.num_chunks = 0

# Title
st.title("📚 AI Powered Smart Study Assistant")
st.subheader("Upload your study material and ask anything!")

# Sidebar
with st.sidebar:
    st.header("📁 Upload Material")
    
    # PDF uploader
    uploaded_file = st.file_uploader(
        "Upload your PDF",
        type="pdf",
        help="Upload any PDF study material"
    )
    
    # Process uploaded PDF
    if uploaded_file is not None:
        if st.button("📥 Process PDF"):
            with st.spinner("Processing PDF..."):
                # Save uploaded file temporarily
                temp_path = f"data/{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Process with RAG pipeline
                success = st.session_state.rag.process_pdf(temp_path)
                
                if success:
                    st.session_state.pdf_processed = True
                    st.session_state.num_chunks = len(st.session_state.rag.chunks)
                    st.success("✅ PDF processed successfully!")
                    st.session_state.messages = []
                else:
                    st.error("❌ Failed to process PDF. Please try another file.")
    
    # Show PDF status
    if st.session_state.pdf_processed:
        st.success("📄 PDF Ready!")
        st.info(f"📊 {st.session_state.num_chunks} chunks created")
    else:
        st.warning("⚠️ No PDF uploaded yet")
    
    st.divider()
    
    st.header("⚙️ Settings")
    num_chunks = st.slider(
        "Chunks to retrieve",
        min_value=3,
        max_value=10,
        value=5
    )
    
    st.divider()
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Main chat area
if len(st.session_state.messages) == 0:
    if st.session_state.pdf_processed:
        st.info("✅ PDF uploaded! Ask me anything about your study material!")
    else:
        st.info("👋 Welcome! Upload a PDF in the sidebar to get started!")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question about your study material..."):
    if not st.session_state.pdf_processed:
        st.warning("⚠️ Please upload a PDF first!")
    else:
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.write(prompt)

        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = f"You asked: '{prompt}'. RAG pipeline will be connected on Day 14!"
                st.write(response)

        # Save AI response
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })