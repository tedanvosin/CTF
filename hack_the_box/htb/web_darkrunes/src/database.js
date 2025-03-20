const Database = require('better-sqlite3');
const { createHash } = require('./utils/crypto');

const db = new Database('db.sqlite');
db.exec('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)');
db.exec('CREATE TABLE IF NOT EXISTS documents (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, content TEXT, integrity VARCHAR(256))');

const findUser = (username) => db.prepare('SELECT * FROM users WHERE username = ?').get(username);

const addUser = (username, password) => {
	try {
		const hash = createHash(password);

		db.prepare('INSERT INTO users (username, password) VALUES (?, ?)').run(username, hash);

		return true
	}
	catch (error) {
		return false
	}
}

const findUserDocuments = (userId) => {
	const stmt = db.prepare('SELECT * FROM documents WHERE user_id = ?');
	return stmt.all(userId);
}

const findDocument = (userId, id) => {
	const stmt = db.prepare('SELECT * FROM documents WHERE id = ? AND user_id = ?');
	return stmt.get(id, userId);
}

const deleteDocument = (id) => db.prepare('DELETE FROM documents WHERE id = ?').run(id);

const addDocument = (id, content, integrity) => {
	const stmt = db.prepare('INSERT INTO documents (user_id, content, integrity) VALUES (?, ?, ?)');
	const { lastInsertRowid } = stmt.run(id, content, integrity)
	return lastInsertRowid;
}


module.exports = { findUser, addUser, findUserDocuments, findDocument, deleteDocument, addDocument };

