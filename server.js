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

// Serve static files (like CSS, JS) from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// Set the view engine to EJS and define the 'views' directory
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Initialize Elasticsearch client
const esClient = new Client({ node: 'http://10.10.20.107:9200' });

// Serve homepage with form to trigger module execution and display real-time logs
app.get('/', (req, res) => {
    res.render('index', { message: null });
});

// Endpoint to queue a Python module execution
app.post('/trigger-python-module', async (req, res) => {
    const { moduleName, hostname } = req.body;

    if (!moduleName) {
        return res.render('index', { message: 'Module name is required' });
    }

    try {
        // Create task in Elasticsearch, include the hostname or use 'all' if none provided
        const result = await esClient.index({
            index: 'python-tasks',
            document: {
                moduleName: moduleName,
                hostname: hostname || 'all',
                status: 'pending',
                created_at: new Date().toISOString()
            }
        });

        res.redirect(`/task/${result._id}`);
    } catch (error) {
        console.error(`Error adding task to Elasticsearch: ${error.message}`);
        res.render('index', { message: 'Error adding task to Elasticsearch' });
    }
});

// Endpoint to fetch task result by ID and render it
app.get('/task/:id', async (req, res) => {
    const { id } = req.params;

    try {
        // Fetch the task from Elasticsearch by ID
        const result = await esClient.get({
            index: 'python-tasks',
            id: id
        });

        // Render the result using EJS
        res.render('task', { task: result._source });
    } catch (error) {
        console.error(`Error fetching task from Elasticsearch: ${error.message}`);
        res.status(500).send('Error fetching task');
    }
});

// Socket.io real-time log updates
io.on('connection', (socket) => {
    console.log('A user connected');

    // Emit logs to the connected user every 5 seconds (replace with real log fetching logic)
    setInterval(async () => {
        try {
            const logs = await esClient.search({
                index: 'machine-logs-*',  // Use appropriate index pattern for your logs
                body: {
                    query: {
                        match_all: {}
                    },
                    sort: [{ timestamp: { order: 'desc' } }],
                    size: 10  // Fetch last 10 logs
                }
            });

            // Send logs to the client
            socket.emit('logs', logs.hits.hits.map(log => log._source));
        } catch (error) {
            console.error('Error fetching logs:', error.message);
        }
    }, 5000);  // Fetch logs every 5 seconds
});

// Start the server with Socket.io
server.listen(port, () => {
    console.log(`Node.js server running on http://localhost:${port}`);
});

