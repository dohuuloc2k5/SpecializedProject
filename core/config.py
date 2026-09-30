import os
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

class Config:
    # Cấu hình SQL Server
    DB_SERVER = os.getenv("DB_SERVER", "localhost")
    DB_NAME = os.getenv("DB_NAME", "TroLyAo_DB")
    DB_USER = os.getenv("DB_USER", "")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    
    # Cấu hình AI Engine
    OLLAMA_MODEL = "qwen2.5:7b"
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200