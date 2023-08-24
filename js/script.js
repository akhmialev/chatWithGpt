const chatLog = document.getElementById('chat-log');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const loadingIndicator = document.getElementById('loading-indicator');
const authButtonContainer = document.getElementById('auth-button-container');
const loginButton = document.getElementById('login-button');
const registerButton = document.getElementById('register-button');

// Функция для отправки сообщения
function sendMessage() {
    const userMessage = messageInput.value;
    if (userMessage.trim() === '') return;

    chatLog.innerHTML += `<div><strong>Вы:</strong> ${userMessage}</div>`;
    messageInput.value = '';

    loadingIndicator.style.display = 'block'; // Показать индикатор загрузки

    // Замените URL на свой API URL
    fetch(`http://127.0.0.1:8000/api/v1/?msg=${encodeURIComponent(userMessage)}`)
        .then(response => response.json())
        .then(data => {
            if (data.message === "Limit exceeded") {
                authButtonContainer.style.display = 'block'; // Показать контейнер с кнопками
            } else {
                chatLog.innerHTML += `<div><strong>Ассистент:</strong> ${data.message}</div>`;
                chatLog.scrollTop = chatLog.scrollHeight;
            }
        })
        .catch(error => console.error('Ошибка при запросе:', error))
        .finally(() => {
            loadingIndicator.style.display = 'none'; // Скрыть индикатор загрузки
        });
}

// Обработчик нажатия Enter на поле ввода сообщения
messageInput.addEventListener('keydown', event => {
    if (event.key === 'Enter') {
        event.preventDefault(); // Предотвращаем стандартное поведение (отправку формы)
        sendMessage(); // Вызываем функцию отправки сообщения
    }
});

// Обработчик кнопки "Отправить"
sendButton.addEventListener('click', sendMessage);

// Обработчики для кнопок Вход и Регистрация
loginButton.addEventListener('click', () => {
    // Ваш код для обработки кнопки Вход
});

registerButton.addEventListener('click', () => {
    // Ваш код для обработки кнопки Регистрация
});
