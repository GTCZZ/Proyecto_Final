// catalogo/static/catalogo/js/chatbot.js

function toggleChat() {
    const body = document.getElementById('chat-body');
    body.style.display = body.style.display === 'none' ? 'block' : 'none';
}

function enviarMensaje() {
    const input = document.getElementById('chat-input');
    const messages = document.getElementById('chat-messages');
    const userText = input.value;
    
    if (userText.trim() === '') return;

    // 1. Mostrar mensaje del usuario
    messages.innerHTML += `<p style="text-align: right; color: blue;"><b>Tú:</b> ${userText}</p>`;
    input.value = '';
    messages.scrollTop = messages.scrollHeight;

    // 2. Consultar al Motor Lógico de Django vía FETCH
    fetch(`/api/chat/?mensaje=${encodeURIComponent(userText)}`)
        .then(response => response.json())
        .then(data => {
            messages.innerHTML += `<p style="text-align: left; color: #333;"><b>Bot:</b> ${data.respuesta}</p>`;
            messages.scrollTop = messages.scrollHeight;
        })
        .catch(error => console.error('Error:', error));
}

// Asegurarnos de que el DOM cargue antes de agregar el evento del 'Enter'
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("chat-input").addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            enviarMensaje();
        }
    });
});