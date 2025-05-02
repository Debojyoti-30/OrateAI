// routes/geminiRoutes.js
const express = require("express");
const router = express.Router();
const geminiController = require("../controllers/summarizerController");

router.post("/summarize", upload.single('file'), summarizerController.summarizeText);

module.exports = router;