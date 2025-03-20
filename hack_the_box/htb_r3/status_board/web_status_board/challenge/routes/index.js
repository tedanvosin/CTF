const express        = require('express');
const router         = express.Router();
const User           = require('../models/User');
const JWTHelper      = require('../helpers/JWTHelper');
const AuthMiddleware = require('../middleware/AuthMiddleware');

router.get('/', (req, res) => {
	return res.render('index.html');
});

router.get('/login', (req, res) => {
	return res.render('login.html');
});

router.post('/api/login', (req, res) => {
	let { username, password } = req.body;

	if (username && password) {
		return User.find({ 
			username,
			password
		})
			.then((user) => {
				if (user.length == 1) {
					let token = JWTHelper.sign({ username: user[0].username });
					res.cookie('session', token, { maxAge: 3600000 });
					return res.json({logged: 1, message: 'User authenticated successfully!' });
				} else {
					return res.json({logged: 0, message: 'Invalid username or password!'});
				}
			})
			.catch(() => res.json({ message: 'Something went wrong'}));
	}
	return res.json({ message: 'No username or password supplied!'});
});

router.get('/dashboard', AuthMiddleware, async (req, res, next) => {
	return res.render('dashboard.html');
});

router.get('/logout', (req, res) => {
	res.clearCookie('session');
	return res.redirect('/');
});

module.exports = router;