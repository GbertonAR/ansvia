import os  
import base64
from openai import AzureOpenAI  
from azure.identity import DefaultAzureCredential, get_bearer_token_provider  
        
endpoint = os.getenv("ENDPOINT_URL", "https://ansv-ai-testeo.openai.azure.com/")  
deployment = os.getenv("DEPLOYMENT_NAME", "ansv2-gpt35")  
      
# Inicialización del cliente del Azure OpenAI Service con autenticación de id. de Entra
token_provider = get_bearer_token_provider(  
    DefaultAzureCredential(),  
    "https://cognitiveservices.azure.com/.default"  
)  
  
client = AzureOpenAI(  
    azure_endpoint=endpoint,  
    azure_ad_token_provider=token_provider,  
    api_version="2025-01-01-preview",  
)  
  

chat_prompt = [
    {
        "role": "user",
        "content": "Buenos dias como estas?"
    },
    {
        "role": "assistant",
        "content": "¡Hola! Estoy aquí para ayudarte. ¿Cómo estás hoy? ¿Hay algo en lo que pueda asistirte?"
    },
    {
        "role": "user",
        "content": "Porque no puedo hacer que funcione?"
    },
    {
        "role": "assistant",
        "content": "Lamento escuchar que estás teniendo dificultades. ¿Podrías ser más específico sobre qué es lo que no puedes hacer funcionar? Estoy aquí para ayudarte a solucionar cualquier problema que puedas tener. ¡Cuéntame más detalles para poder ayudarte mejor!"
    }
] 
  
# Incluir el resultado de voz si la voz está habilitada  
messages = chat_prompt 

completion = client.chat.completions.create(  
    model=deployment,  
    messages=messages,
    max_tokens=800,  
    temperature=0.7,  
    top_p=0.95,  
    frequency_penalty=0,  
    presence_penalty=0,
    stop=None,  
    stream=False  
)  
  
print(completion.to_json())  