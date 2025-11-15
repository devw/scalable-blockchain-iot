/**
 * Validation Middleware
 * Input validation using functional approach
 */

/**
 * Validate single sensor data submission
 */
const validateSensorData = (req, res, next) => {
  const { sensorId, data } = req.body;

  if (!sensorId || typeof sensorId !== "string") {
    return res.status(400).json({
      success: false,
      error: "Invalid or missing sensorId (must be string)",
    });
  }

  if (!data) {
    return res.status(400).json({
      success: false,
      error: "Missing required field: data",
    });
  }

  next();
};

/**
 * Validate batch data submission
 */
const validateBatchData = (req, res, next) => {
  const { readings } = req.body;

  if (!readings || !Array.isArray(readings)) {
    return res.status(400).json({
      success: false,
      error: "Invalid input: readings must be an array",
    });
  }

  if (readings.length === 0) {
    return res.status(400).json({
      success: false,
      error: "Batch cannot be empty",
    });
  }

  if (readings.length > 50) {
    return res.status(400).json({
      success: false,
      error: "Batch size exceeds maximum (50 readings)",
    });
  }

  // Validate each reading
  const invalidIndex = readings.findIndex((r) => !r.sensorId || !r.data);

  if (invalidIndex !== -1) {
    return res.status(400).json({
      success: false,
      error: `Invalid reading at index ${invalidIndex}: missing sensorId or data`,
    });
  }

  next();
};

/**
 * Validate timestamp (optional field)
 */
const validateTimestamp = (req, res, next) => {
  const { timestamp } = req.body;

  if (timestamp !== undefined) {
    const ts = Number(timestamp);

    if (isNaN(ts) || ts <= 0) {
      return res.status(400).json({
        success: false,
        error: "Invalid timestamp: must be positive number",
      });
    }

    // Check if timestamp is not too far in future (1 hour tolerance)
    const now = Math.floor(Date.now() / 1000);
    const maxFuture = now + 3600;

    if (ts > maxFuture) {
      return res.status(400).json({
        success: false,
        error: "Timestamp cannot be more than 1 hour in the future",
      });
    }
  }

  next();
};

module.exports = {
  validateSensorData,
  validateBatchData,
  validateTimestamp,
};
