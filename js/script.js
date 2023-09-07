const chatLog = document.getElementById('chat-log');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const loadingIndicator = document.getElementById('loading-indicator');
const authButtonContainer = document.getElementById('auth-button-container');
const loginButton = document.getElementById('login-button');
const registerButton = document.getElementById('register-button');
const messageOverlay = document.getElementById('message-overlay');
const closeButton = document.getElementById('close-button');
const registrationButton = document.getElementById('register-button');
const registrationOverlay = document.getElementById('registration-overlay');
const registerSubmitButton = document.getElementById('register-submit-button');
const registrationEmailInput = document.getElementById('registration-email');
const registrationPasswordInput = document.getElementById('registration-password');
const closeRegistrationButton = document.getElementById('close-registration-button');

function sendMessage() {
    const userMessage = messageInput.value;
    if (userMessage.trim() === '') return;

    chatLog.innerHTML += `<div><strong>Вы:</strong> ${userMessage}</div>`;
    messageInput.value = '';

    loadingIndicator.style.display = 'block';

    // Replace the URL with your API URL
    fetch(`http://127.0.0.1:8000/api/v1/?msg=${encodeURIComponent(userMessage)}`)
        .then(response => response.json())
        .then(data => {
            if (data.message === 'Limit exceeded') {
                authButtonContainer.style.display = 'block';
                showMessageOverlay("У вас закончились бесплатные запросы. Зарегистрируйтесь или войдите");
            } else {
                chatLog.innerHTML += `<div><strong>Ассистент:</strong> ${data.message}</div>`;
                chatLog.scrollTop = chatLog.scrollHeight;
            }
        })
        .catch(error => console.error('Ошибка при запросе:', error))
        .finally(() => {
            loadingIndicator.style.display = 'none';
        });
}

function showMessageOverlay(message) {
    messageOverlay.style.display = 'flex';
    const messageText = document.querySelector('.message-text');
    messageText.textContent = message;
    closeButton.focus();
}

function hideMessageOverlay() {
    messageOverlay.style.display = 'none';
}

messageInput.addEventListener('keydown', event => {
    if (event.key === 'Enter') {
        event.preventDefault();
        sendMessage();
    }
});

sendButton.addEventListener('click', sendMessage);

loginButton.addEventListener('click', () => {
    showMessageOverlay();
});

registrationButton.addEventListener('click', () => {
    registrationOverlay.style.display = 'flex';
    registrationEmailInput.value = '';
    registrationPasswordInput.value = '';
    registrationEmailInput.focus();

    const messageText = document.querySelector('.message-text');
    messageText.textContent = '';
    registerSubmitButton.disabled = true;
    registerSubmitButton.style.opacity = 0.5;
});

registrationEmailInput.addEventListener('input', () => {
    checkFormValidity();
});

registrationPasswordInput.addEventListener('input', () => {
    checkFormValidity();
});

function checkFormValidity() {
    const email = registrationEmailInput.value;
    const password = registrationPasswordInput.value;
    const isValid = email.trim() !== '' && password.trim() !== '';

    registerSubmitButton.disabled = !isValid;
    registerSubmitButton.style.opacity = isValid ? 1 : 0.5;
}

registerSubmitButton.addEventListener('click', () => {
    const email = registrationEmailInput.value;
    const password = registrationPasswordInput.value;

    const formData = new URLSearchParams();
    formData.append('email', email);
    formData.append('password', password);

    fetch('http://127.0.0.1:8000/api/v1/register/', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        const message = data.message;
        showMessageOverlay(message);
        handleSuccessfulRegistration(); // Добавляем этот вызов
    })
    .catch(error => console.error('Ошибка при регистрации:', error))
    .finally(() => {
        registrationOverlay.style.display = 'none';
    });
});

function closeRegistrationOverlay() {
    registrationOverlay.style.display = 'none';
}
closeRegistrationButton.addEventListener('click', () => {
    closeRegistrationOverlay();
});
closeButton.addEventListener('click', hideMessageOverlay);

closeButton.addEventListener('keydown', event => {
    if (event.key === 'Enter') {
        hideMessageOverlay();
    }
});

function handleSuccessfulRegistration() {
    const loginButton = document.getElementById('login-button');
    const registerButton = document.getElementById('register-button');
    const logoutButton = document.getElementById('logout-button');

    loginButton.style.display = 'none';
    registerButton.style.display = 'none';
    logoutButton.style.display = 'block';
}
