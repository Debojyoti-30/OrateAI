const { spawn } = require('child_process');
const path = require('path');

exports.handleUpload = (req, res) => {
  const filePath = path.join(__dirname, '../uploads', req.file.filename);

  const python = spawn('python3', [
    './python-models/evaluate_all.py',
    filePath,
  ]);

  python.stdout.on('data', (data) => {
    const result = data.toString();
    res.json({ analysis: JSON.parse(result) });
  });

  python.stderr.on('data', (data) => {
    console.error(`Python error: ${data}`);
  });
};
