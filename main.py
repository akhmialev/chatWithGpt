import openai
import uvicorn
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware

from tools import load_messages, save_messages, messages, get_user_ip, ip_message_count
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
def get_request(msg: str, request: Request, message_count: int = Depends(get_user_ip)):
    load_messages()
    client_ip = request.client.host

    if message_count >= 3:
        return {'message': 'Limit exceeded'}

    messages.append({'role': 'user', 'content': msg})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    answer = response.choices[0]['message']['content']
    messages.append({'role': 'assistant', 'content': answer})
    save_messages()

    ip_message_count[client_ip] = message_count + 1
    print(ip_message_count)
    return answer


if __name__ == '__main__':
    uvicorn.run(app, port=8000)
