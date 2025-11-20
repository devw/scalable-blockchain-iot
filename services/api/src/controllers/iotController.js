const blockchainClient = require("../blockchain/client");

/**
 * IoT Data Controller
 * Handles business logic for IoT data submission endpoints
 */
class IotController {
  /**
   * Submit single IoT sensor data
   * @param {Object} req - Express request
   * @param {Object} res - Express response
   */
  // Submit single IoT sensor data
  async submitData(req, res) {
    try {
      const { sensorId, data, timestamp } = req.body;

      if (!sensorId || !data) {
        return res.status(400).json({
          success: false,
          error: "Missing required fields: sensorId, data",
        });
      }

      // Convert timestamp to uint256 (seconds)
      const dataTimestamp = timestamp
        ? Math.floor(new Date(timestamp).getTime() / 1000)
        : Math.floor(Date.now() / 1000);

      console.log(
        `📥 Received data from sensor: ${sensorId}, timestamp: ${dataTimestamp}`
      );

      const receipt = await blockchainClient.submitData(
        sensorId,
        JSON.stringify(data),
        dataTimestamp
      );

      console.log(`✅ Data submitted successfully: ${receipt.transactionHash}`);

      return res.status(201).json({
        success: true,
        message: "Data submitted successfully",
        data: {
          sensorId,
          transactionHash: receipt.transactionHash,
          blockNumber: receipt.blockNumber,
          gasUsed: receipt.gasUsed,
          timestamp: dataTimestamp,
        },
      });
    } catch (error) {
      console.error("❌ Error submitting data:", error.message);
      return res.status(500).json({
        success: false,
        error: "Failed to submit data to blockchain",
        details: error.message,
      });
    }
  }

  /**
   * Submit batch of IoT sensor data
   * @param {Object} req - Express request
   * @param {Object} res - Express response
   */
  // Submit batch of IoT sensor data
  async submitBatchData(req, res) {
    try {
      const { readings } = req.body;

      if (!readings || !Array.isArray(readings) || readings.length === 0) {
        return res.status(400).json({
          success: false,
          error: "Invalid input: readings must be a non-empty array",
        });
      }

      if (readings.length > 50) {
        return res.status(400).json({
          success: false,
          error: "Batch size too large: maximum 50 readings per batch",
        });
      }

      const sensorIds = [];
      const dataPoints = [];
      const timestamps = [];

      readings.forEach((r, i) => {
        if (!r.sensorId || !r.data) {
          throw new Error(
            `Invalid reading at index ${i}: missing sensorId or data`
          );
        }

        sensorIds.push(r.sensorId);
        dataPoints.push(JSON.stringify(r.data));
        timestamps.push(
          r.timestamp
            ? Math.floor(new Date(r.timestamp).getTime() / 1000)
            : Math.floor(Date.now() / 1000)
        );
      });

      console.log(`📥 Received batch of ${readings.length} readings`);

      const receipt = await blockchainClient.submitBatchData(
        sensorIds,
        dataPoints,
        timestamps
      );

      console.log(
        `✅ Batch submitted successfully: ${receipt.transactionHash}`
      );

      return res.status(201).json({
        success: true,
        message: "Batch data submitted successfully",
        data: {
          itemsSubmitted: receipt.itemsSubmitted,
          transactionHash: receipt.transactionHash,
          blockNumber: receipt.blockNumber,
          gasUsed: receipt.gasUsed,
        },
      });
    } catch (error) {
      console.error("❌ Error submitting batch:", error.message);
      return res.status(500).json({
        success: false,
        error: "Failed to submit batch data to blockchain",
        details: error.message,
      });
    }
  }

  /**
   * Get contract statistics
   * @param {Object} req - Express request
   * @param {Object} res - Express response
   */
  async getContractInfo(req, res) {
    try {
      const info = await blockchainClient.getContractInfo();

      return res.status(200).json({
        success: true,
        data: info,
      });
    } catch (error) {
      console.error("❌ Error getting contract info:", error.message);

      return res.status(500).json({
        success: false,
        error: "Failed to retrieve contract information",
        details: error.message,
      });
    }
  }

  /**
   * Health check endpoint
   * @param {Object} req - Express request
   * @param {Object} res - Express response
   */
  async healthCheck(req, res) {
    try {
      const isHealthy = await blockchainClient.healthCheck();

      if (isHealthy) {
        return res.status(200).json({
          success: true,
          status: "healthy",
          blockchain: "connected",
        });
      } else {
        return res.status(503).json({
          success: false,
          status: "unhealthy",
          blockchain: "disconnected",
        });
      }
    } catch (error) {
      return res.status(503).json({
        success: false,
        status: "unhealthy",
        error: error.message,
      });
    }
  }
}

module.exports = new IotController();
