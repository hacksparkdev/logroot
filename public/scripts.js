document.addEventListener('DOMContentLoaded', () => {
    const socket = io();

    // Handle real-time logs
    socket.on('logs', (logs) => {
        const logList = document.getElementById('logList');
        logList.innerHTML = ''; // Clear previous logs
        logs.forEach(log => {
            const li = document.createElement('li');
            li.textContent = `${log.timestamp}: ${log.message}`;
            logList.appendChild(li);
        });
    });
});

