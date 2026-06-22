import streamlit as st
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from rag import RAGPipeline

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

    # Multiple file uploader
    uploaded_files = st.file_uploader(
        "Upload your PDFs",
        type="pdf",
        accept_multiple_files=True,
        help="Upload one or more PDF study materials"
    )

    if uploaded_files:
        if st.button("📥 Process PDFs"):
            for uploaded_file in uploaded_files:
                with st.spinner(f"Processing {uploaded_file.name}..."):
                    temp_path = f"data/{uploaded_file.name}"
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    success = st.session_state.rag.process_pdf(temp_path)

                    if success:
                        st.session_state.pdf_processed = True
                        st.session_state.num_chunks = len(st.session_state.rag.chunks)
                        st.success(f"✅ {uploaded_file.name} processed!")
                    else:
                        st.error(f"❌ Failed to process {uploaded_file.name}")

    # Show uploaded PDFs
    if st.session_state.pdf_processed:
        st.success("📄 PDFs Ready!")
        st.info(f"📊 {st.session_state.num_chunks} total chunks")

        # Show list of uploaded PDFs
        if st.session_state.rag.uploaded_pdfs:
            st.write("**Uploaded PDFs:**")
            for pdf in st.session_state.rag.uploaded_pdfs:
                st.write(f"📄 {pdf}")
    else:
        st.warning("⚠️ No PDFs uploaded yet")

    st.divider()

    st.header("⚙️ Settings")
    num_chunks = st.slider(
        "Chunks to retrieve",
        min_value=3,
        max_value=10,
        value=5
    )

    st.divider()

    st.header("🛠️ Tools")

    if st.button("📝 Summarize PDF"):
        if not st.session_state.pdf_processed:
            st.warning("⚠️ Please upload a PDF first!")
        else:
            with st.spinner("Generating summary..."):
                summary = st.session_state.rag.summarize()
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"📝 **Document Summary:**\n\n{summary}"
                })
            st.rerun()

    if st.button("🎯 Generate Quiz"):
        if not st.session_state.pdf_processed:
            st.warning("⚠️ Please upload a PDF first!")
        else:
            with st.spinner("Generating quiz..."):
                quiz = st.session_state.rag.generate_quiz()
                if quiz:
                    quiz_text = "🎯 **Quiz Time!**\n\n"
                    for i, q in enumerate(quiz):
                        quiz_text += f"**Q{i+1}: {q['question']}**\n\n"
                        for option in q['options']:
                            quiz_text += f"{option}\n"
                        quiz_text += f"\n✅ **Answer: {q['answer']}**\n\n"
                        quiz_text += "---\n\n"
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": quiz_text
                    })
                else:
                    st.error("❌ Failed to generate quiz.")
            st.rerun()

    st.divider()

    # Reset button
    if st.button("🔄 Reset All"):
        st.session_state.rag.reset()
        st.session_state.pdf_processed = False
        st.session_state.num_chunks = 0
        st.session_state.messages = []
        st.session_state.questions_asked = 0
        st.rerun()

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.rag.clear_history()
        st.rerun()

# Chat area
if len(st.session_state.messages) == 0:
    if st.session_state.pdf_processed:
        st.info("✅ PDFs uploaded! Ask me anything about your study material!")
    else:
        st.info("👋 Welcome! Upload PDFs in the sidebar to get started!")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question about your study material..."):
    if not st.session_state.pdf_processed:
        st.warning("⚠️ Please upload a PDF first!")
    else:
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.rag.ask(prompt)
                st.write(response)
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })
        st.session_state.questions_asked += 1
        st.rerun()