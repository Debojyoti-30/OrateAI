const express = require('express');
const cors = require('cors');
const app = express();

app.use(cors());
app.use(express.json());

const videoRoutes = require('./routes/videoRoutes');
app.use('/api/video', videoRoutes);

module.exports = app;
