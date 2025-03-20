const crypto = require('crypto');
const jwt = require('jsonwebtoken');
const APP_SECRET = crypto.randomBytes(69).toString('hex');

module.exports = {
	sign(data) {
		data = Object.assign(data);
		return (jwt.sign(data, APP_SECRET, { algorithm:'HS256' }))
	},
	decode(token) {
		return (jwt.verify(token, APP_SECRET, { algorithm:'HS256' }));
	}
}