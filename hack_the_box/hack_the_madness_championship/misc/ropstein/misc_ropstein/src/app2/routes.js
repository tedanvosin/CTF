const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const dotenv = require('dotenv');
const bodyParser = require('body-parser')
const fs = require('fs')
const path = require('path');

dotenv.config();

const app = express();
const DATABASE = 'users.db';
app.use(express.json());
app.use(express.text()); 
app.use(bodyParser.json())
app.use(express.static(path.join(__dirname, 'public')));



const Router = express.Router();


const db = new sqlite3.Database(DATABASE, (err) => {
  if (err) {
    return console.error(err.message);
  }
  console.log('Connected to SQLite database.');
});


Router.post('/login', (req, res) => {
  const { agentid, passkey } = req.body;

  db.get("SELECT * FROM users WHERE agentid = ? AND passkey = ?", [agentid, passkey], (err, user) => {
    if (user) {
      req.session.auth = true;
      req.session.user_id = user.id;
      req.session.agentid = user.agentid;
      res.status(200).json({ redirect: '/dashboard' });
    } else {
      res.status(401).json({ message: "Invalid credentials." });
    }
  });
});


Router.post('/upload', (req, res) => {
  if (!req.session.auth) {
    return res.status(401).json({ message: "Unauthorized" });
  }

  try {
    const { filename, content } = req.body;
    const fileExtension = path.extname(filename).toLowerCase();
    if (fileExtension === '.js' || fileExtension === '.json') {
      return res.status(400).json({ message: "Uploading .js or .json files is not allowed." });
    }

    const isValidBase64 = (str) => {
      const base64Regex = /^(?:[A-Z0-9+\/]{4})*?(?:[A-Z0-9+\/]{2}==|[A-Z0-9+\/]{3}=)?$/i;
      return base64Regex.test(str.replace(/\s/g, ''));
    };

    if (!isValidBase64(content)) {
      return res.status(400).json({ message: "Invalid Base64 content." });
    }

    const buffer = Buffer.from(content, 'base64');
    fs.writeFile(filename, buffer, (err) => {
      if (err) {
        return res.status(500).json({ message: "Error occurred while saving the file." });
      }
      
      // Record backup information in the database.
      const fileSizeInBytes = buffer.length;
      const userId = req.session.user_id;
      db.run(
        "INSERT INTO backups (user_id, filename, file_size) VALUES (?, ?, ?)",
        [userId, filename, fileSizeInBytes],
        (err) => {
          if (err) {
            console.error("Error inserting backup record:", err);
            return res.status(500).json({ message: "File saved, but error recording backup info." });
          }
          res.json({ message: "File uploaded successfully!" });
        }
      );
    });
  } catch (error) {
    console.error("Error during upload:", error);
    res.status(500).json({ message: "Error occurred during the upload process." });
  }
});

Router.get('/download/:id', (req, res) => {
  if (!req.session.auth) {
    return res.status(401).json({ message: "Unauthorized" });
  }
  const backupId = req.params.id;
  db.get("SELECT filename FROM backups WHERE id = ? AND user_id = ?", [backupId, req.session.user_id], (err, row) => {
    if (err || !row) {
      return res.status(404).json({ message: "File not found" });
    }
    // Assuming files are stored in the server's root directory or adjust the path accordingly
    const filepath = require('path').join(process.cwd(), row.filename);
    res.download(filepath, row.filename, (err) => {
      if (err) {
        console.error("Error downloading file:", err);
        res.status(500).json({ message: "Error downloading file." });
      }
    });
  });
});


Router.get('/backups', (req, res) => {
  if (!req.session.auth) {
    return res.status(401).json({ message: "Unauthorized" });
  }
  const userId = req.session.user_id;
  db.all(
    "SELECT id, filename, file_size, timestamp FROM backups WHERE user_id = ? ORDER BY timestamp ASC",
    [userId],
    (err, rows) => {
      if (err) {
        return res.status(500).json({ message: "Error retrieving backups." });
      }
      res.json(rows);
    }
  );
});



module.exports = Router;
