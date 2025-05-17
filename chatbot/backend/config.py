# import os
# from dotenv import load_dotenv

# load_dotenv()

# class Settings:
#     GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
#     GEMINI_MODEL = os.getenv("GEMINI_MODEL", "models/gemini-2.0-flash")
#     DATA_PATH = os.getenv("DATA_PATH", "./backend/data/data_20250515.json")
#     CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR", "./chroma_db")
#     EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "BAAI/bge-large-en-v1.5") # model oke nhất trong 3 model t test nha
#     CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000)) # thử 300 nhma kh oke lắm
#     CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 100))
#     API_HOST = os.getenv("API_HOST", "0.0.0.0")
#     API_PORT = int(os.getenv("API_PORT", 8000))
#     LOGFIRE_TOKEN = os.getenv("LOGFIRE_TOKEN")
#     LOG_LEVEL = os.getenv("LOG_LEVEL", "info")

# settings = Settings()