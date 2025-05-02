const { execFile } = require("child_process");
const path = require("path");
const fs = require("fs");

exports.summarizeText = async (req, res) => {
  try {
    const filePath = req.file.path;  // Get file path from multer
    const fileType = path.extname(filePath).toLowerCase().replace(".", "");  // "pptx" or "pdf"
    const pythonScript = path.join(__dirname, "summarizer.py");

    execFile("python", [pythonScript, filePath, fileType], (error, stdout, stderr) => {
      if (error) {
        console.error("Exec Error:", error);
        console.error("stderr:", stderr);
        return res.status(500).json({ error: "Summarization failed" });
      }
      console.log("stdout:", stdout);  // You can log stdout here to check the result
      fs.unlinkSync(filePath);  // Clean up uploaded file after processing
      return res.json({ summary: stdout.trim() });
    });
    
    
  } catch (err) {
    console.error("Controller error:", err);
    res.status(500).json({ error: "Internal Server Error" });
  }
};
