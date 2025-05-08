import chromadb
import os

# Set environment variables before creating client
os.environ["CHROMA_DB_IMPL"] = "duckdb+parquet"
os.environ["PERSIST_DIRECTORY"] = "./chroma_store"

client = chromadb.Client()

print("✅ ChromaDB is ready using duckdb+parquet at ./chroma_store")
input("Press Enter to exit...")
