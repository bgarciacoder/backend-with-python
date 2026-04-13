import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
if MONGO_URI is None:
    raise ValueError("MONGO_URI environment variable not set")

API_AUTH_TOKEN = os.getenv("API_AUTH_TOKEN")
if API_AUTH_TOKEN is None:
    raise ValueError("API_AUTH_TOKEN environment variable not set")