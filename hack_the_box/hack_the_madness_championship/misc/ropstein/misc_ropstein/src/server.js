const express = require('express');
const path = require('path');
const app1Routes = require('./app1/routes');
const app2Routes = require('./app2/routes');
const sqlite3 = require('sqlite3').verbose();
const session = require('express-session');


const app = express();


const secretKey = process.env.SECRET_KEY || 'redactedl33tredactedl33t';
const admin_pass = process.env.ADMIN_PASS || 'redactedl33t';
const DATABASE = 'users.db';
const db = new sqlite3.Database(DATABASE, (err) => {
  if (err) {
    return console.error(err.message);
  }
  console.log('Connected to SQLite database (test connection)');
  initDb();
});

function initDb() {
  db.serialize(() => {
    db.run(`
      CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        agentid TEXT NOT NULL UNIQUE,
        passkey TEXT NOT NULL
      )
    `);

    db.run(`
      CREATE TABLE IF NOT EXISTS backups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        filename TEXT NOT NULL,
        file_size INTEGER NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
      )
    `);

    db.get("SELECT COUNT(*) AS count FROM users", (err, row) => {
      if (err) {
        return console.error("Error checking users table:", err);
      }
      if (row.count === 0) {
        db.run("INSERT INTO users (agentid, passkey) VALUES (?, ?)",
          ['admin', admin_pass],
          function (err) {
            if (!err) {
              console.log("Admin user created with default credentials.");
              insertSampleBackups(this.lastID);
            }
          }
        );
      } else {
        db.get("SELECT id FROM users WHERE agentid = ?", ['admin'], (err, user) => {
          if (user) {
            insertSampleBackups(user.id);
          }
        });
      }
    });

    // Function to insert sample backup records
    function insertSampleBackups(adminUserId) {
      db.get("SELECT COUNT(*) AS count FROM backups", (err, row) => {
        if (err) {
          return console.error("Error checking backups table:", err);
        }
        if (row.count === 0) {
          const petabyte = 1e15;
          db.run(
            "INSERT INTO backups (user_id, filename, file_size) VALUES (?, ?, ?)",
            [adminUserId, "aws_backup.zip", petabyte],
            (err) => {
              if (err) console.error("Error inserting sample backup:", err);
              else console.log("Inserted sample backup with 1 petabyte file size.");
            }
          );

          db.run(
            "INSERT INTO backups (user_id, filename, file_size) VALUES (?, ?, ?)",
            [adminUserId, "evil_core_main_server_backup.zip", petabyte * 2],
            (err) => {
              if (err) console.error("Error inserting sample backup:", err);
              else console.log("Inserted sample backup with 2 petabytes file size.");
            }
          );
        }
      });
    }
  });
}



app.use(express.json());

app.use(session({
    secret: secretKey,
    resave: false,
    saveUninitialized: true,
  }));

app.use('/api/v1/static', express.static(path.join(__dirname, './public')));
app.use('/api/v2/static', express.static(path.join(__dirname, './public')));

app.use('/api/v1', app1Routes);
app.use('/api/v2', app2Routes);


app.get('/', (req, res) => {
    if (req.session.auth) {
      res.redirect('/dashboard');
    } else {
      res.sendFile(path.join(__dirname, 'public', 'login.html'));
    }
  });
  
app.get('/login', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'login.html'));
  });

app.get('/dashboard', (req, res) => {
    if (req.session.auth) {
      res.sendFile(path.join(__dirname, 'public', 'dashboard.html'));
    } else {
      res.redirect('/login'); 
    }
  });

  
app.listen(5000, () => {
    console.log(`Server running ...`);
});