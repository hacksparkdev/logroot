const express = require('express');
const { Client } = require('@elastic/elasticsearch');
const app = express();
const port = 3000;

app.use(express.json());
app.use(express.urlencoded({ extended: true })); // To handle form data

// Set the view engine to EJS
app.set('view engine', 'ejs');

// Initialize Elasticsearch client
const esClient = new Client({ node: 'http://10.10.20.107:9200' });

// Serve the form on the root route
app.get('/', (req, res) => {
    res.render('index', { errorMessage: null }); // Render form without any errors initially
});

// Endpoint to queue a Python module execution
app.post('/trigger-python-module', async (req, res) => {
    const { moduleName, hostname } = req.body;

    if (!moduleName || !hostname) {
        // If the form submission is incomplete, show an error
        return res.render('index', { errorMessage: 'Module name and hostname are required' });
    }

    try {
        // Create task in Elasticsearch
        const result = await esClient.index({
            index: 'python-tasks',
            document: {
                moduleName: moduleName,
                hostname: hostname, // Include hostname in the task document
                status: 'pending',
                created_at: new Date().toISOString()
            }
        });

        // Redirect to task result page after queuing the module
        res.redirect(`/task/${result._id}`);
    } catch (error) {
        console.error(`Error adding task to Elasticsearch: ${error.message}`);
        res.render('index', { errorMessage: 'Error adding task' });
    }
});

// Endpoint to fetch task result by ID
app.get('/task/:id', async (req, res) => {
    const { id } = req.params;

    try {
        // Fetch the task from Elasticsearch by ID
        const result = await esClient.get({
            index: 'python-tasks',
            id: id
        });

        res.send(result._source);
    } catch (error) {
        console.error(`Error fetching task from Elasticsearch: ${error.message}`);
        res.status(500).send('Error fetching task');
    }
});

app.listen(port, () => {
    console.log(`Node.js server running on http://localhost:${port}`);
});

