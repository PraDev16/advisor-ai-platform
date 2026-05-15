from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from Backend.rag.vector_store import (
    vectorstore
)

# -----------------------------
# PDF INGESTION
# -----------------------------
def ingest_pdf(pdf_path):

    # -----------------------------
    # READ PDF
    # -----------------------------
    reader = PdfReader(pdf_path)

    full_text = ""

    for page in reader.pages:

        text = page.extract_text()

        if text:
            full_text += text + "\n"

    # -----------------------------
    # SPLIT INTO CHUNKS
    # -----------------------------
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_text(full_text)

    # -----------------------------
    # STORE IN VECTOR DB
    # -----------------------------
    vectorstore.add_texts(chunks)

    return {
        "status": "success",
        "chunks_added": len(chunks)
    }