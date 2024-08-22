document.getElementById('send_button').addEventListener('click', function() {
    const userInput = document.getElementById('user_input').value;
    const messagesDiv = document.getElementById('messages');

    // Display user message
    messagesDiv.innerHTML += `<div>User: ${userInput}</div>`;

    // Send user input to the Flask backend
    fetch('/feedback', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ genre: 'pop', liked: true })  // Update this as needed
    })
    .then(response => response.json())
    .then(data => {
        // Display bot response
        if (data) {
            messagesDiv.innerHTML += `<div>Bot: How about this song: ${data.name} by ${data.artist}? <a href="${data.url}" target="_blank">Listen on Spotify</a></div>`;
        } else {
            messagesDiv.innerHTML += `<div>Bot: I couldn't find any recommendations at the moment.</div>`;
        }
        document.getElementById('user_input').value = ''; // Clear input field
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
