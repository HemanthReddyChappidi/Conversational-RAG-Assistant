import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="RAG Knowledge Assistant", page_icon="🤖")

st.title("📚 RAG Knowledge Assistant")

# ========== SIDEBAR UPLOAD ==========
st.sidebar.header("Upload Documents")

uploaded_file = st.sidebar.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)

if uploaded_file is not None:
    with st.sidebar:
        with st.spinner("Uploading & indexing document..."):
            files = {"file": uploaded_file.getvalue()}
            response = requests.post(f"{API_URL}/upload", files={"file": uploaded_file})

            if response.status_code == 200:
                st.success("Document uploaded & indexed!")
            else:
                st.error("Upload failed")

# ========== CHAT HISTORY ==========
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ========== CHAT INPUT ==========
if prompt := st.chat_input("Ask a question about your documents"):
    # show user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # stream assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            response = requests.post(
                f"{API_URL}/ask_stream",
                params={
                    "question": prompt,
                    "session_id": "streamlit_user"
                },
                stream=True,
            )

            if response.status_code != 200:
                st.error("Ask API failed. Upload a document first.")
                st.stop()

            # read streamed tokens
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    text = chunk.decode("utf-8")
                    full_response += text
                    message_placeholder.markdown(full_response + "▌")

            # final message without cursor
            message_placeholder.markdown(full_response)

        except Exception:
            st.error("Cannot connect to backend. Is FastAPI running?")
            st.stop()

    # save chat history
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )