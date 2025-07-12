document.addEventListener('DOMContentLoaded', () => {
    const sendBtn = document.getElementById('send-btn');
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');
    const personaType = document.getElementById('persona-type');
    const personaRelation = document.getElementById('persona-relation');
    const personaTone = document.getElementById('persona-tone');
    const personaField = document.getElementById('persona-field');

    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    function sendMessage() {
        const userMessage = userInput.value.trim();
        if (userMessage) {
            appendMessage('user', userMessage);
            userInput.value = '';
            generateBotResponse(userMessage);
        }
    }

    function appendMessage(sender, message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `${sender}-message`);
        messageElement.textContent = message;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function generateBotResponse(userMessage) {
        const type = personaType.value.trim() || 'AI';
        const relation = personaRelation.value.trim() || 'assistant';
        const tone = personaTone.value.trim() || 'helpful';
        const field = personaField.value.trim() || 'general';

        const botMessage = `As a ${type} ${relation} with a ${tone} tone in the field of ${field}, I think... (This is a placeholder response. The actual response logic needs to be implemented based on the persona.)`;
        appendMessage('bot', botMessage);
    }
});
