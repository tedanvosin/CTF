const express = require('express');
const path = require('path');
const cookieParser = require('cookie-parser');
const { jwks } = require('./utils/jwt');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Import routes
const pageRoutes = require('./routes/pageRoutes');
const authRoutes = require('./routes/authRoutes');
const cameraRoutes = require('./routes/cameraRoutes');

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'static')));
app.use('/css', express.static(path.join(__dirname, 'static/css')));
app.use('/js', express.static(path.join(__dirname, 'static/js')));
app.use('/img', express.static(path.join(__dirname, 'static/img')));
app.use(express.static(path.join(__dirname, 'templates')));

// Routes
app.use('/', pageRoutes);
app.use('/api', authRoutes);
app.use('/api/cameras', cameraRoutes);

// JWKS endpoint
app.get('/.well-known/jwks.json', (req, res) => {
    res.json(jwks);
});

// Error handling middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ success: false, message: 'Something went wrong!' });
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
}); 