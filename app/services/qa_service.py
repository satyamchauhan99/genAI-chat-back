import chromadb
from langchain_community.llms import OpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
import os
from app.services.chrome_client import get_chroma_client
from app.core.config import OPENAI_API_KEY

embedding_function = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
client = get_chroma_client()
    
def store_document_embedding(doc_id: str, content: str):
    embedding_vector = embedding_function.embed_documents([content])[0]
    collection = client.get_or_create_collection("documents")
    collection.add(
        embeddings=[embedding_vector],
        ids=[doc_id],
        documents=[content],
        metadatas=[{"document_id": doc_id}]
    )


def ask_question(question: str, document_ids: list[str]) -> str:
    collection = client.get_or_create_collection("documents")

    results = collection.query(
        query_texts=[question],
        n_results=5,
        where={"document_id": {"$in": [str(doc_id) for doc_id in document_ids]}}
    )

    if not results["documents"] or not results["documents"][0]:
        return "No relevant documents found."

    context = "\n".join(results["documents"][0])
    llm = OpenAI(openai_api_key=OPENAI_API_KEY)
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=None)
    return qa.run(f"{context}\nQuestion: {question}")
