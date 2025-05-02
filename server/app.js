// server/app.js
const express = require('express');
const cors = require('cors');
require('dotenv').config();
const multer = require('multer');
const upload = multer({ dest: 'uploads/' });

const chatbotRoutes = require('./routes/chatbot');
// const summarizerRoutes = require('./routes/summarizerRoutes');

const app = express();
app.use(cors());
app.use(express.json());

// your other routes here...
// app.use('/api/summarizer/summarize', upload.single('file'));
app.use('/api/chatbot', chatbotRoutes);


module.exports = app;


