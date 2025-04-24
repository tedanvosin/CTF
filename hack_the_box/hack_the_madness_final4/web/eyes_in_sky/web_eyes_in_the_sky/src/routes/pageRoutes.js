const express = require('express');
const router = express.Router();
const authMiddleware = require('../middleware/auth');
const { getHomePage, getDashboardPage, getUnauthorizedPage, handleNext } = require('../controllers/pageController');

// Public routes
router.get('/', getHomePage);
router.get('/unauthorized', getUnauthorizedPage);
router.get('/next', handleNext);

// Protected routes
router.get('/dashboard', authMiddleware, getDashboardPage);

module.exports = router; 