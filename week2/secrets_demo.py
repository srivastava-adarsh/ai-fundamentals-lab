import os
from dotenv import load_dotenv

load_dotenv()

#read an environment variable
api_key = os.environ.get("MY_API_KEY")

if api_key is None:
    print("No API Key found in environment.")
else:
    print(f"API Key Loaded: (length{len(api_key)} chars)")