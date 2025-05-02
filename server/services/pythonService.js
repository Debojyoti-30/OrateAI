const { spawn } = require('child_process');
const path = require('path');

exports.runPythonAnalysis = (videoPath) => {
  return new Promise((resolve, reject) => {
    const script = path.join(__dirname, '../python-models/evaluate_all.py');
    const process = spawn('python3', [script, videoPath]);

    let output = '';

    process.stdout.on('data', (data) => {
      output += data.toString();
    });

    process.stderr.on('data', (data) => {
      console.error(`Python error: ${data}`);
    });

    process.on('close', () => {
      try {
        const parsedOutput = JSON.parse(output);
        resolve(parsedOutput);
      } catch (e) {
        reject('Failed to parse Python output');
      }
    });
  });
};
