import os
from dotenv import load_dotenv

# Load environment variables from .env file, if available
load_dotenv()

class Config:
    """Application configuration definitions."""
    
    # API Keys are loaded securely from environment variables
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # File Paths
    DOCUMENTS_DIR = "data"
    FAISS_INDEX_PATH = "data/faiss_index"
    
    # Optional parameters for web search
    SEARCH_NUM_RESULTS = 3
    
    # Model parameters
    TEMPERATURE_CONCISE = 0.3
    TEMPERATURE_DETAILED = 0.7
