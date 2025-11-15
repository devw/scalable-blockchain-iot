const express = require('express');
const iotController = require('../controllers/iotController');

const router = express.Router();

/**
 * POST /api/iot/data
 * Submit single IoT sensor data
 * 
 * Body: {
 *   sensorId: string,
 *   data: object,
 *   timestamp?: number
 * }
 */
router.post('/data', iotController.submitData);

/**
 * POST /api/iot/batch
 * Submit batch of IoT sensor data
 * 
 * Body: {
 *   readings: [{
 *     sensorId: string,
 *     data: object,
 *     timestamp?: number
 *   }]
 * }
 */
router.post('/batch', iotController.submitBatchData);

/**
 * GET /api/iot/info
 * Get contract information and statistics
 */
router.get('/info', iotController.getContractInfo);

module.exports = router;
