const express = require('express');
const { Client } = require('@elastic/elasticsearch');
const http = require('http');
const path = require('path');
const socketIo = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);
const port = 3000;

// Middleware to parse JSON and form data
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

// Set the view engine to EJS
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Initialize Elasticsearch client
const esClient = new Client({ node: 'http://10.10.20.107:9200' });

// Serve the homepage with real-time log display
app.get('/', (req, res) => {
    res.render('index', { message: null });
});

// Socket.io to emit real-time logs
io.on('connection', (socket) => {
    console.log('A user connected');

    // Emit logs to the connected user every 5 seconds
    setInterval(async () => {
        try {
            const logs = await esClient.search({
                index: 'security-logs',  // Elasticsearch index where logs are stored
                body: {
                    query: {
                        match_all: {}
                    },
                    sort: [{ timestamp: { order: 'desc' } }],
                    size: 10  // Adjust size to fetch the last 10 logs
                }
            });

            // Emit logs to the client
            socket.emit('logs', logs.hits.hits.map(log => log._source));
        } catch (error) {
            console.error('Error fetching logs:', error.message);
        }
    }, 5000);  // Poll every 5 seconds
});

// Start the server with Socket.io
server.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
});

