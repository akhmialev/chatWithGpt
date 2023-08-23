import openai
import uvicorn
from fastapi import Depends, FastAPI
from tools import load_messages, save_messages, messages
from config import API_KEY

openai.api_key = API_KEY
app = FastAPI()


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
