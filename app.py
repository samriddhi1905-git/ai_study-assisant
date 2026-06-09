import os
import streamlit as st

from utils.pdf_loader import load_pdf

from utils.embeddings import (
    create_vector_db,
    load_vector_db
)

from utils.retriever import retrieve_chunks

from utils.llm import generate_answer

from utils.pdf_manager import (
    save_uploaded_pdfs,
    get_all_pdfs,
    delete_pdf
)

PDF_FOLDER = "pdfs"

os.makedirs(PDF_FOLDER, exist_ok=True)

st.set_page_config(page_title="AI Study Assistant")

st.title("AI Study Assistant")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "vectordb" not in st.session_state:
    st.session_state.vectordb = None

# Sidebar
with st.sidebar:

    st.header("Upload PDFs")

    uploaded_files = st.file_uploader(
        "Upload PDFs",
        type="pdf",
        accept_multiple_files=True
    )

    if uploaded_files:

        with st.spinner("Processing PDFs..."):

            save_uploaded_pdfs(uploaded_files)

            all_documents = []

            pdf_files = get_all_pdfs()

            for pdf in pdf_files:

                pdf_path = os.path.join(
                    PDF_FOLDER,
                    pdf
                )

                documents = load_pdf(pdf_path)

                all_documents.extend(documents)

            vectordb = create_vector_db(
                all_documents
            )

            st.session_state.vectordb = vectordb

        st.success("PDFs processed successfully!")

    st.subheader("Uploaded PDFs")

    pdf_files = get_all_pdfs()

    selected_pdf = st.selectbox(
        "Filter by PDF",
        ["All"] + pdf_files
    )

    for pdf in pdf_files:

        col1, col2 = st.columns([4, 1])

        with col1:

            st.write(f"📄 {pdf}")

        with col2:

            if st.button(
                "❌",
                key=pdf
            ):

                delete_pdf(pdf)

                st.rerun()

# Load existing DB
if (
    st.session_state.vectordb is None
    and os.path.exists("chroma_db")
):

    st.session_state.vectordb = load_vector_db()

# Chat UI
if st.session_state.vectordb:

    # Show old messages
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    # User input
    query = st.chat_input(
        "Ask a question about your notes"
    )

    if query:

        # Save user message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": query
            }
        )

        with st.chat_message("user"):

            st.markdown(query)

        # AI response
        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                results = retrieve_chunks(
                    st.session_state.vectordb,
                    query,
                    selected_pdf
                )

                answer = generate_answer(
                    query,
                    results
                )

                st.markdown(answer)

        # Save response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

else:

    st.info("Upload PDFs to begin.")