document.addEventListener('DOMContentLoaded', () => {
    const sendBtn = document.getElementById('send-btn');
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');
    const personaType = document.getElementById('persona-type');
    const personaRelation = document.getElementById('persona-relation');
    const personaTone = document.getElementById('persona-tone');
    const personaField = document.getElementById('persona-field');
    const exportJsonBtn = document.getElementById('export-json-btn');

    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    exportJsonBtn.addEventListener('click', exportToJson);

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

    function exportToJson() {
        const persona = {
            role: "system",
            content: `You are a ${personaType.value.trim()} ${personaRelation.value.trim()} with a ${personaTone.value.trim()} tone, specializing in ${personaField.value.trim()}.`
        };

        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify([persona], null, 2));
        const downloadAnchorNode = document.createElement('a');
        downloadAnchorNode.setAttribute("href", dataStr);
        downloadAnchorNode.setAttribute("download", "persona.json");
        document.body.appendChild(downloadAnchorNode); // required for firefox
        downloadAnchorNode.click();
        downloadAnchorNode.remove();
    }
});
