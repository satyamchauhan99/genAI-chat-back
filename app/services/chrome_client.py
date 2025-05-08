import chromadb
from app.core.config import CHROME_DB_IMPL, PERSIST_DIRECTORY
from chromadb.config import Settings
from langchain_community.vectorstores import Chroma

_chroma_initialized = False
_chroma_client = None

def get_chroma_client():
    global _chroma_initialized, _chroma_client

    if not _chroma_initialized:
        try:
            settings = Settings(
                # chroma_db_impl=CHROME_DB_IMPL,
                # persist_directory=PERSIST_DIRECTORY,
                allow_reset=False # Set this to False for production!
            )
            try:
                _chroma_client = chromadb.Client(settings)
                _chroma_initialized = True
            except ValueError as e:
                print(f"Error initializing Chroma client: {e}")
                raise  
        except ValueError as err:
            print("ERRORORORO************", err)
            raise
    return _chroma_client
