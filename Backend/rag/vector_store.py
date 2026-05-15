from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter


# -----------------------------
# LOAD + SPLIT DOCS
# -----------------------------
def load_documents():

    import os

    file_path = os.path.join(
        os.path.dirname(__file__),
        "knowledge_base",
        "risk_policy.txt"
    )

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50
    )

    chunks = splitter.create_documents([text])

    return chunks


# -----------------------------
# CREATE VECTOR STORE
# -----------------------------
def create_vector_store():

    docs = load_documents()

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(
        docs,
        embeddings
    )

    return vectorstore


# -----------------------------
# GLOBAL VECTOR STORE
# -----------------------------
vectorstore = create_vector_store()


# -----------------------------
# SEARCH FUNCTION
# -----------------------------
def search_docs(query, k=2):

    results = vectorstore.similarity_search(
        query,
        k=k
    )

    print(f"[VECTOR SEARCH] Query: {query}")
    print(f"[VECTOR SEARCH] Results: {len(results)}")

    return results