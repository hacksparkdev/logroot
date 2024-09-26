const express = require('express');
const bodyParser = require('body-parser');
const { Client } = require('@elastic/elasticsearch');
const path = require('path')

const app = express();
app.set('view engine', 'ejs');
app.use(express.static(path.join(__dirname, 'public')));
app.use(bodyParser.urlencoded({ extended: true }));

// Set up Elasticsearch client
const client = new Client({ node: 'http://10.10.20.107:9200' });

// Logs route (already in your code)
app.get('/logs', async (req, res) => {
    try {
        // Query Elasticsearch for logs
        const result = await client.search({
		index: 'winlogbeat-*',  // Replace with your Elasticsearch index
            size: 200,            // Number of logs to display
            body: {
                query: {
                    match_all: {}  // Fetch all logs, you can customize this to match specific queries
                }
            }
        });

        // Pass logs to the EJS view
        res.render('logs2', { logs: result.hits.hits });
    } catch (err) {
        console.error(err);
        res.status(500).send('Error fetching logs');
    }
});

app.get('/filter', async (req, res) => {
    const { logLevel, eventType, timeRange } = req.query;
    const query = { bool: { must: [] } };

    // Add log level filter if provided
    if (logLevel) {
        query.bool.must.push({ term: { 'log.level.keyword': logLevel } });
    }

    // Add event type filter if provided
    if (eventType) {
        query.bool.must.push({ match: { 'event.type': eventType } });
    }

    // Add time range filter if provided
    if (timeRange) {
        const now = new Date();
        const pastTime = new Date(now.getTime() - timeRange * 60 * 60 * 1000);
        query.bool.must.push({
            range: {
                '@timestamp': {
                    gte: pastTime.toISOString(),
                    lte: now.toISOString()
                }
            }
        });
    }

    try {
        const result = await client.search({
            index: 'winlogbeat-*',
            body: { query }
        });
        res.render('filter', { logs: result.hits.hits });
    } catch (error) {
        console.error(error);
        res.status(500).send('Error fetching logs');
    }
});


app.get('/dashboard', (req, res) => {
    res.render('dashboard')
})

app.listen(3000, () => {
    console.log('Server started on http://localhost:3000');
});

