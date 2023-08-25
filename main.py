import openai
import uvicorn
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware

from tools import load_messages, save_messages, messages, get_user_ip
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
def get_request(msg: str, message_count: int = Depends(get_user_ip)):
    load_messages()

    if message_count:
        return {'message': 'Limit exceeded'}

    messages.append({'role': 'user', 'content': msg})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    answer = response.choices[0]['message']['content']
    messages.append({'role': 'assistant', 'content': answer})
    save_messages()

    return {'message': answer}


if __name__ == '__main__':
    uvicorn.run(app, port=8000)
