import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="RAG Knowledge Assistant", page_icon="🤖")

st.title("📚 RAG Knowledge Assistant")

# Chat history storage
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input box
if prompt := st.chat_input("Ask a question about your documents"):
    # Show user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Call FastAPI backend
    with st.spinner("Thinking..."):
        response = requests.post(
            f"{API_URL}/ask",
            params={"question": prompt}
        )

        result = response.json()
        answer = result["answer"]
        sources = ", ".join(result["sources"])

        final_answer = f"{answer}\n\n📄 **Sources:** {sources}"

    # Show assistant response
    with st.chat_message("assistant"):
        st.markdown(final_answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": final_answer}
    )