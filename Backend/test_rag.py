from rag.rag_engine import load_documents

docs = load_documents()

print("\nFINAL OUTPUT")
print("Number of chunks:", len(docs))

if docs:
    print("\nFirst chunk:\n", docs[0].page_content)