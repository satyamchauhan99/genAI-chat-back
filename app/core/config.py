import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "secret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
CHROME_DB_IMPL = os.getenv("CHROME_DB_IMPL", "duckdb+parquet")
PERSIST_DIRECTORY = os.getenv("PERSIST_DIRECTORY", "./chrome_store")
ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS", [".csv", ".xls", ".xlsx"])
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploaded_docs")
