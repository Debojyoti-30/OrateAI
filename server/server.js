// server/server.js
const app = require('./app');
const PORT = process.env.PORT || 5001;

app.listen(PORT, () => {
  console.log(`✅ Server running on port ${PORT}`);
  console.log('GROQ_API_KEY:', process.env.GROQ_API_KEY);
  console.log('Gemini_API_KEY:', process.env.GEMINI_API_KEY);

});
