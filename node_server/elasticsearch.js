// elasticsearch.js

const { Client } = require('@elastic/elasticsearch');
const client = new Client({ node: 'http://10.10.20.107:9200' });

async function indexLog(log) {
    try {
        await client.index({
            index: 'windows-logs',
            body: log
        });
    } catch (error) {
        console.error('Error indexing log:', error);
    }
}

async function searchLogs(query) {
    try {
        const { body } = await client.search({
            index: 'windows-logs',
            body: {
                query: {
                    match: query
                }
            }
        });
        return body.hits.hits;
    } catch (error) {
        console.error('Error searching logs:', error);
        return [];
    }
}

module.exports = { indexLog, searchLogs };

