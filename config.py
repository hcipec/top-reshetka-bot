import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.environ["BOT_TOKEN"]
GEMINI_API_KEY: str = os.environ["GEMINI_API_KEY"]
