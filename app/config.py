import os
from dotenv import load_dotenv, find_dotenv

# Loading environment variables from .env file
load_dotenv(find_dotenv(), override=True)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")