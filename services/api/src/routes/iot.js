const express = require('express');
const iotController = require('../controllers/iotController');

const router = express.Router();

router.post('/data', iotController.submitData);
router.post('/batch', iotController.submitBatchData);
router.get('/info', iotController.getContractInfo);

// 👉 NEW: Blockchain statistics
router.get('/stats', iotController.getBlockchainStats);

module.exports = router;
