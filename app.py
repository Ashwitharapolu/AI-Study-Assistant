import streamlit as st

# Page config
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
    
    st.divider()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display welcome message if no messages
if len(st.session_state.messages) == 0:
    st.info("👋 Welcome! Upload a PDF in the sidebar and start asking questions!")

# Display all previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input at bottom
if prompt := st.chat_input("Ask a question about your study material..."):
    
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Display AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Placeholder response for now
            response = f"You asked: '{prompt}'. RAG pipeline will be connected on Day 14!"
            st.write(response)
    
    # Add AI response to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })