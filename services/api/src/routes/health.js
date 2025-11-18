const express = require('express');
const iotController = require('../controllers/iotController');

const router = express.Router();

/**
 * GET /health
 * Health check endpoint
 */
router.get('/', iotController.healthCheck);

module.exports = router;
