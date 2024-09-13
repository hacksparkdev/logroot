const express = require('express');
const {client} = require {'@elastic/elasticsearch'};
const app = express();
const port = 3000;

app.use(express.json());

//Initialize Elasticsearch client
const esClient = new Client({node: 'http://10.10.20.107:9200'});

//Endpoint to queue a Python module execution
app.post('/trigger-python-module', async (req, res) => {
	const {moduleName} = req.body;

	if (!moduleName){
		return res.status(400).send('Module name is required')

	}

	
})
