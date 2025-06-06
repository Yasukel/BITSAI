from dotenv import load_dotenv
import os

load_dotenv()  # This loads the .env file into environment variables

token = os.getenv("GITHUB_TOKEN")
if not token:
    raise ValueError("GITHUB_TOKEN environment variable not set.")

print("Token loaded successfully!")
print(token)
