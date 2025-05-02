require('dotenv').config();

const axios = require('axios');

const GROQ_ENDPOINT = 'https://api.groq.com/openai/v1/chat/completions';  // Updated endpoint

exports.chatWithGroq = async (req, res) => {
  const userMessage = req.body.message;
  if (!userMessage) {
    return res.status(400).json({ error: 'No message provided' });
  }

  try {
    const payload = {
      model: 'llama-3.3-70b-versatile', // Match model to what you're using in the curl request
      messages: [
        { role: 'system', content: 'You are Orate AI, an expert ppt presentation and public speaking coach. Keep your responses short and precise.' },
        { role: 'user', content: userMessage }
      ]
    };

    const response = await axios.post(GROQ_ENDPOINT, payload, {
      headers: {
        'Authorization': `Bearer ${process.env.GROQ_API_KEY}`,
        'Content-Type': 'application/json'
      }
    });

    const reply = response.data.choices?.[0]?.message?.content
      || 'Sorry, I didn’t get a response.';

    return res.json({ reply });
  } catch (err) {
    console.error('🛑 Groq API error:', err.response?.data || err.message);
    return res.status(500).json({ error: 'Failed to get reply from Groq API.' });
  }
};
