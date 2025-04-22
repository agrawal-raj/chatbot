$(document).ready(function() {
    const chatBox = $('#chat-box');
    const userInput = $('#user-input');
    const sendButton = $('#send-button');
    
    // Scroll to bottom of chat
    function scrollToBottom() {
        chatBox.scrollTop(chatBox[0].scrollHeight);
    }
    
    // Add message to chat
    function addMessage(text, isUser) {
        const messageClass = isUser ? 'user-message' : 'bot-message';
        chatBox.append(`
            <div class="message ${messageClass}">
                ${text}
            </div>
        `);
        scrollToBottom();
    }
    
    // Handle send message
    function sendMessage() {
        const message = userInput.val().trim();
        if (message) {
            addMessage(message, true);
            userInput.val('');
            
            // Send to server
            $.ajax({
                url: '/chat/send/',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({message: message}),
                success: function(data) {
                    addMessage(data.response, false);
                },
                error: function() {
                    addMessage("Sorry, I'm having trouble responding right now.", false);
                }
            });
        }
    }
    
    // Event listeners
    sendButton.click(sendMessage);
    userInput.keypress(function(e) {
        if (e.which === 13) {  // Enter key
            sendMessage();
        }
    });
    
    // Initial scroll to bottom
    scrollToBottom();
});