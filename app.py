import streamlit as st

# Page config - always first line
st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="wide"
)

# Title
st.title("📚 AI Powered Smart Study Assistant")
st.subheader("Upload your study material and ask anything!")

# Sidebar
with st.sidebar:
    st.header("📁 Upload Material")
    st.write("PDF upload coming on Day 13!")
    
    st.divider()
    
    st.header("⚙️ Settings")
    num_chunks = st.slider(
        "Chunks to retrieve",
        min_value=3,
        max_value=10,
        value=5
    )
    st.write(f"Will retrieve top {num_chunks} chunks")

# Main area - 3 columns
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📄 Pages Processed", "0")

with col2:
    st.metric("🔍 Chunks Created", "0")

with col3:
    st.metric("❓ Questions Asked", "0")

st.divider()

# Simple input test
st.subheader("💬 Ask a Question")
question = st.text_input("Type your question here...")

if st.button("Ask"):
    if question:
        st.info(f"You asked: {question}")
        st.warning("RAG pipeline will be connected on Day 14!")
    else:
        st.error("Please type a question first!")

# Footer
st.divider()
st.caption("AI Powered Smart Study Assistant using RAG and LLMs")