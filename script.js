const chatbox = document.getElementById('chatbox');
const input = document.getElementById('input');
const submit = document.getElementById('submit');

// Function to add a new message to the chatbox
function addMessage(message, sender) {
    const msg = document.createElement('div');
    msg.innerHTML = `<strong>${sender}: </strong>${message}`;
    chatbox.appendChild(msg);
    chatbox.scrollTop = chatbox.scrollHeight;
}

// Function to send a message to the server
function sendMessage() {
    const message = input.value;
    if (message.trim() === '') return;

    addMessage(message, 'You');
    input.value = '';

    fetch('https://13.233.161.16:5000/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message }),
        mode: 'cors',
    })
    .then(response => response.json())
    .then(data => {
        const reply = data.reply;
        addMessage(reply, 'Bot');
    })
    .catch(error => {
        console.log('Error:', error);
    });
}

// Event listener for the submit button
submit.addEventListener('click', sendMessage);

// Event listener for the Enter key
input.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});
