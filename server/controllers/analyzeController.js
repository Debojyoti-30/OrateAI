const { runPythonAnalysis } = require('../services/pythonService');

exports.handleUploadAndAnalyze = async (req, res) => {
  try {
    const videoPath = req.file.path;
    const result = await runPythonAnalysis(videoPath);
    res.json(result);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Analysis failed' });
  }
};
