const api = require('./api');
const express = require('express');
const app = express();
const port = 5000;

app.get('/Stops/', api.getAllStops);
app.get('/Stops/:id', api.getStopById);
app.post('/Stops/', api.addStop);
app.put('/Stops/:id', api.updateStop);
app.delete('/Stops/:id', api.deleteStop);

app.use(express.json());

app.listen(port, () => {
    console.log(`At Stop app running on port ${port}.`);
});