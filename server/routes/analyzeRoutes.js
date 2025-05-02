const express = require('express');
const multer = require('multer');
const { handleUploadAndAnalyze } = require('../controllers/analyzeController');

const router = express.Router();
const upload = multer({ dest: 'uploads/' });

router.post('/video/upload', upload.single('video'), handleUploadAndAnalyze);

module.exports = router;
