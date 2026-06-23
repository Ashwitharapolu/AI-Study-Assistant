# Day 21 - Professional Subtle UI
import streamlit as st
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from rag import RAGPipeline

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Subtle light grey background */
    .stApp {
        background-color: #f1f5f9;
    }

    /* Sidebar subtle indigo */
    section[data-testid="stSidebar"] {
        background-color: #eef2ff;
        border-right: 1px solid #c7d2fe;
    }

    section[data-testid="stSidebar"] * {
        color: #1e1b4b !important;
    }

    /* Buttons */
    .stButton > button {
        background-color: #6366f1;
        color: white !important;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        width: 100%;
        padding: 0.5rem;
        transition: all 0.2s;
    }

    .stButton > button:hover {
        background-color: #4f46e5;
        color: white !important;
    }

    /* Metric cards */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e0e7ff;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }

    /* Chat messages */
    .stChatMessage {
        background-color: #ffffff !important;
        border-radius: 12px !important;
        border: 1px solid #e0e7ff !important;
        padding: 1rem !important;
        margin: 0.5rem 0 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
    }

    /* Chat input */
    div[data-testid="stChatInput"] textarea {
        background-color: #ffffff !important;
        border: 1px solid #c7d2fe !important;
        border-radius: 8px !important;
    }

    /* Divider */
    hr {
        border-color: #e0e7ff !important;
    }

    /* Success/warning/error */
    div[data-testid="stAlert"] {
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

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

# Header
st.markdown("## 📚 AI Powered Smart Study Assistant")
st.markdown("Upload your study material and ask anything using RAG + LLMs")
st.divider()

# Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(
        "📄 PDF Status",
        "Ready ✅" if st.session_state.pdf_processed else "Not Uploaded"
    )
with col2:
    st.metric("🔍 Chunks Created", st.session_state.num_chunks)
with col3:
    st.metric("❓ Questions Asked", st.session_state.questions_asked)
with col4:
    st.metric(
        "📑 PDFs Uploaded",
        len(st.session_state.rag.uploaded_pdfs)
    )

st.divider()

# Sidebar
with st.sidebar:
    st.markdown("## 📚 Study Assistant")
    st.caption("Powered by RAG + Groq LLM")
    st.divider()

    st.markdown("### 📁 Upload Material")
    uploaded_files = st.file_uploader(
        "Upload your PDFs",
        type="pdf",
        accept_multiple_files=True
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
                        st.session_state.num_chunks = len(
                            st.session_state.rag.chunks)
                        st.success(f"✅ {uploaded_file.name} processed!")
                    else:
                        st.error(f"❌ Failed: {uploaded_file.name}")

    if st.session_state.pdf_processed:
        st.success("📄 PDFs Ready!")
        st.info(f"📊 {st.session_state.num_chunks} total chunks")
        if st.session_state.rag.uploaded_pdfs:
            st.markdown("**Uploaded PDFs:**")
            for pdf in st.session_state.rag.uploaded_pdfs:
                st.markdown(f"📄 `{pdf}`")
    else:
        st.warning("⚠️ No PDFs uploaded yet")

    st.divider()

    st.markdown("### ⚙️ Settings")
    num_chunks = st.slider(
        "Chunks to retrieve",
        min_value=3,
        max_value=10,
        value=5
    )

    st.divider()

    st.markdown("### 🛠️ Tools")

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

    st.markdown("### 🔧 Manage")

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

    st.divider()
    st.caption("Built with LangChain + FAISS + Groq")

# Chat area
if len(st.session_state.messages) == 0:
    if st.session_state.pdf_processed:
        st.info("✅ PDFs uploaded! Ask me anything!")
    else:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            ### 👋 Welcome to AI Study Assistant!

            **Get started in 3 simple steps:**

            **1.** 📁 Upload your PDF in the sidebar

            **2.** 📥 Click Process PDFs and wait

            **3.** 💬 Ask any question about your material!

            ---

            **✨ What you can do:**

            ✅ Ask questions from your PDF

            ✅ Generate study summaries

            ✅ Auto generate quizzes

            ✅ Conversation memory

            ✅ Multi PDF support
            """)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

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
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.rag.ask(prompt)
                st.markdown(response)
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })
        st.session_state.questions_asked += 1
        st.rerun()