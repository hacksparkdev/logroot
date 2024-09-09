// server.js

const express = require('express');
const http = require('http');
const socketIO = require('socket.io');
const { indexLog, searchLogs } = require('./elasticsearch');

// Create an Express app
const app = express();
const server = http.createServer(app);
const io = socketIO(server);

// Serve static files (frontend UI)
app.use(express.static('public'));

// Handle incoming WebSocket connections from clients
io.on('connection', (socket) => {
    console.log('A user connected');

    // Listen for incoming log data from Python
    socket.on('log_data', async (data) => {
        console.log('Received log:', data);
        await indexLog(JSON.parse(data));
        io.emit('new_log', data);  // Broadcast log data to all connected clients
    });

    // Handle search requests
    socket.on('search_logs', async (query) => {
        const results = await searchLogs(query);
        socket.emit('search_results', results);
    });

    socket.on('disconnect', () => {
        console.log('A user disconnected');
    });
});

// Start the server
const PORT = process.env.PORT || 5000;
server.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

