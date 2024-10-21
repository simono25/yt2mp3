document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById('download-form');
    const loader = document.getElementById('loader');
    const messageContainer = document.getElementById('message-container');
    const downloadButton = document.getElementById('download-btn');

    form.addEventListener('submit', (e) => {
        const urlInput = document.getElementById('url').value;

        // Simple URL validation (ensure the input isn't empty or invalid)
        if (!urlInput.trim()) {
            e.preventDefault();
            showMessage("Please enter a valid YouTube URL.", "error");
            return;
        }

        // Show loading spinner and hide the download button
        downloadButton.disabled = true;
        loader.style.display = 'block';
    });

    // Function to display messages dynamically
    function showMessage(message, type) {
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('message', type);
        msgDiv.innerText = message;
        messageContainer.appendChild(msgDiv);

        // Remove the message after 5 seconds
        setTimeout(() => {
            msgDiv.remove();
        }, 5000);
    }
});
