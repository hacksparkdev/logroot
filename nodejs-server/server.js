const express = require('express');
const bodyParser = require('body-parser');
const { Client } = require('@elastic/elasticsearch');

const app = express();
app.set('view engine', 'ejs');
app.use(bodyParser.urlencoded({ extended: true }));

// Set up Elasticsearch client
const client = new Client({ node: 'http://localhost:9200' });

app.get('/logs', async (req, res) => {
    try {
        // Query Elasticsearch for logs
        const result = await client.search({
            index: 'logs_index',  // Replace with your Elasticsearch index
            size: 100,            // Number of logs to display
            body: {
                query: {
                    match_all: {}  // Fetch all logs, you can customize this to match specific queries
                }
            }
        });

        // Pass logs to the EJS view
        res.render('logs', { logs: result.hits.hits });
    } catch (err) {
        console.error(err);
        res.status(500).send('Error fetching logs');
    }
});

app.listen(3000, () => {
    console.log('Server started on http://localhost:3000');
});

