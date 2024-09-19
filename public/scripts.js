document.addEventListener('DOMContentLoaded', () => {
    const socket = io();

    // Handle real-time logs
    socket.on('logs', (logs) => {
        const logList = document.getElementById('logList');
        logList.innerHTML = ''; // Clear old logs
        logs.forEach(log => {
            const li = document.createElement('li');
            li.textContent = log.message;
            logList.appendChild(li);
        });
    });
});

