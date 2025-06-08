import dotenv
import os

dotenv.load_dotenv()

LLM_API_KEY = os.getenv("LLM_API_KEY")

if LLM_API_KEY == "" or LLM_API_KEY is None:
    print("Error LLM_API_KEY is not set")
    raise Exception()