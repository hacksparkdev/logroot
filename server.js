const express = require('express');
const { Client } = require('@elastic/elasticsearch');
const app = express();
const port = 3000;

app.use(express.json());

// Initialize Elasticsearch client
const esClient = new Client({ node: 'http://10.10.20.107:9200' });

// Endpoint to queue a Python module execution
app.post('/trigger-python-module', async (req, res) => {
    const { moduleName } = req.body;

    if (!moduleName) {
        return res.status(400).send('Module name is required');
    }

    try {
        // Create task in Elasticsearch
        const result = await esClient.index({
            index: 'python-tasks',
            document: {
                moduleName: moduleName,
                status: 'pending',
                created_at: new Date().toISOString()
            }
        });

        res.send(`Module ${moduleName} queued for execution with task ID: ${result._id}`);
    } catch (error) {
        console.error(`Error adding task to Elasticsearch: ${error.message}`);
        res.status(500).send('Error adding task');
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

