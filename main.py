import openai
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from tools import load_messages, save_messages, messages
from config import API_KEY

openai.api_key = API_KEY
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/api/v1/')
def get_request(msg: str):
    load_messages()
    messages.append({'role': 'user', 'content': msg})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    answer = response.choices[0]['message']['content']
    messages.append({'role': 'assistant', 'content': answer})
    save_messages()
    return answer


if __name__ == '__main__':
    uvicorn.run(app, port=8000)
