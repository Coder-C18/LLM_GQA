import google.generativeai as gemini_client
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(dotenv_path='.env')
gemini_client.configure(api_key=os.getenv("API_KEY_GEMINI"))
