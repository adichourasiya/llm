import os
from dotenv import load_dotenv
import openai
import base64

# Load environment variables
load_dotenv()

api_key = os.getenv('AZURE_OPENAI_KEY')
endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
api_version = os.getenv('AZURE_OPENAI_API_VERSION')
deployment_name = os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME')

def get_openai_client():
    return openai.AzureOpenAI(
        api_key=api_key,
        api_version=api_version,
        azure_endpoint=endpoint
    )

def encode_image_to_base64(image_bytes):
    return base64.b64encode(image_bytes).decode('utf-8')

def send_message(messages, deployment_name):
    client = get_openai_client()
    response = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
        max_tokens=300,
        temperature=0.7
    )
    return response.choices[0].message.content
