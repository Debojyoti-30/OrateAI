// server/routes/chatbot.js
const express = require('express');
const router = express.Router();
const { chatWithGroq } = require('../controllers/chatbotController');

// Health-check endpoint
// router.get('/ping', (req, res) => {
//   res.json({ status: 'ok', time: new Date().toISOString() });
// });

// Your existing POST handler
router.post('/chat', chatWithGroq);

module.exports = router;
