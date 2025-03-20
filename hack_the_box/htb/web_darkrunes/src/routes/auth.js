const { generateCookie, createHash } = require('../utils/crypto');
const { addUser, findUser } = require('../database');

const router = require('express').Router();

router.get("/login", (req, res) => {
    res.render("login");
});

router.get("/register", (req, res) => {
    res.render("register");
});

router.post('/login', (req, res) => {
    const { username, password } = req.body;

    if (typeof username !== "string" || typeof password !== "string" || username.length === 0 || password.length === 0) {
        return res.render("login", { error: "Wrong username and password format,they should not be empty" })
    }

    const user = findUser(username)

    if (!user) {
        return res.status(401).send('Invalid username or password');
    }

    const hash = createHash(password);

    if (hash !== user.password) {
        return res.render("login", { error: 'Invalid username or password' })
    }

    const token = generateCookie(user.username, user.id);
    res.cookie('user', token);
    res.redirect('/documents');
});


router.post('/register', (req, res) => {
    const { username, password } = req.body;

    if (typeof username !== "string" || typeof password !== "string" || username.length === 0 || password.length === 0) {
        return res.render("login", { error: "Wrong username and password format,they should not be empty" })
    }

    const existingUser = findUser(username);

    if (existingUser) {
        return res.status(401).render("register", {
            error: "Username already exists"
        })
    }

    addUser(username, password)

    res.redirect('/login');
});

module.exports = router;