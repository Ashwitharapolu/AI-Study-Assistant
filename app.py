import streamlit as st
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from rag import RAGPipeline

# Page config
st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="wide"
)

# Initialize session state
if "rag" not in st.session_state:
    st.session_state.rag = RAGPipeline()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False

if "num_chunks" not in st.session_state:
    st.session_state.num_chunks = 0

if "questions_asked" not in st.session_state:
    st.session_state.questions_asked = 0

# Title
st.title("📚 AI Powered Smart Study Assistant")
st.subheader("Upload your study material and ask anything!")

# Metrics row
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📄 PDF Status",
              "Ready ✅" if st.session_state.pdf_processed else "Not uploaded ❌")
with col2:
    st.metric("🔍 Chunks Created", st.session_state.num_chunks)
with col3:
    st.metric("❓ Questions Asked", st.session_state.questions_asked)

st.divider()

# Sidebar
with st.sidebar:
    st.header("📁 Upload Material")

    uploaded_file = st.file_uploader(
        "Upload your PDF",
        type="pdf",
        help="Upload any PDF study material"
    )

    if uploaded_file is not None:
        if st.button("📥 Process PDF"):
            with st.spinner("Processing PDF... This takes 2-3 minutes"):
                temp_path = f"data/{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                success = st.session_state.rag.process_pdf(temp_path)

                if success:
                    st.session_state.pdf_processed = True
                    st.session_state.num_chunks = len(st.session_state.rag.chunks)
                    st.success("✅ PDF processed successfully!")
                    st.session_state.messages = []
                else:
                    st.error("❌ Failed to process PDF.")

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

# Chat area
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

        # Get REAL answer from RAG pipeline
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # THIS IS THE KEY CHANGE - real RAG answer!
                response = st.session_state.rag.ask(prompt)
                st.write(response)

        # Save response and update counter
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })
        st.session_state.questions_asked += 1
        st.rerun()