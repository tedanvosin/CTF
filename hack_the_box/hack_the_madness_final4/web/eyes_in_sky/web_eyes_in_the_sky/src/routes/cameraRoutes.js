const express = require('express');
const router = express.Router();
const authMiddleware = require('../middleware/auth');
const { getAllCameras, enableCamera, disableCamera, getFlag } = require('../controllers/cameraController');

// All routes require authentication
router.use(authMiddleware);

// Get all cameras
router.get('/', getAllCameras);

// Enable camera
router.post('/:id/enable', enableCamera);

// Disable camera
router.post('/:id/disable', disableCamera);

// Get flag
router.get('/flag', getFlag);

module.exports = router; 