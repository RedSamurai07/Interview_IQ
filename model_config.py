from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
base_url = "https://openrouter.ai/api/v1"
api_key = os.getenv("Open_API_KEY")

client = OpenAI(base_url=base_url, api_key=api_key)

response = client.chat.completions.create(
    model = "nvidia/nemotron-3.5-lightning:free",
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}],
        max_tokens = 500,
        temperature = 0.3
)

print(response.choices[0].message.content)
print(f"Model name: {response.model.name}")

