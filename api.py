import openai
import uvicorn
from fastapi import FastAPI, Request, Depends, Form, Header

from chat import load_messages, save_messages, register
from tools import add_middleware, get_user_ip
from config import API_KEY

openai.api_key = API_KEY
app = FastAPI()
add_middleware(app)


@app.get('/api/v1/')
def get_request(msg: str, request: Request, message_count: int = Depends(get_user_ip)):
    """
        Апи для чата с ИИ
    :param msg: сообщение пользователя.
    :param request: для получения IP пользователя.
    :param message_count: делает проверку на кол-во сообщений, что бы не авторизованный пользователь не мог
                            пользоваться ИИ больше 3 раз в сутки
    """
    messages = load_messages(request)
    if message_count:
        return {'message': 'Limit exceeded'}

    messages.append({'role': 'user', 'content': msg})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    answer = response.choices[0]['message']['content']
    save_messages(request, msg, answer)

    return {'message': answer}


@app.post('/api/v1/register/')
def registration(email: str = Form(...), password: str = Form(...)):
    """
        Апи для регистрации новых пользователей
    :param email: почта
    :param password: пароль
    """
    response = register(email, password)
    return response


@app.get('/api/v1/auth_chat')
def auth_chat(msg: str, Authorization: str = Header(...)):
    print(Authorization)


if __name__ == '__main__':
    uvicorn.run(app, port=8000)
