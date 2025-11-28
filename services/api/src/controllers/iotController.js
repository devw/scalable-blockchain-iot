const blockchainClient = require("../blockchain/client");

// 🔹 Get blockchain statistics
const getBlockchainStats = async (req, res) => {
  try {
    const provider = blockchainClient.getProvider(); // deve essere inizializzato da connect()
    console.log("Provider type:", provider.constructor.name);
    console.log(
      "Provider methods:",
      Object.getOwnPropertyNames(Object.getPrototypeOf(provider))
    );
    if (!provider) throw new Error("Blockchain provider not initialized");

    const [blockNumber, gasPrice, network, latestBlock] = await Promise.all([
      provider.getBlockNumber(),
      provider.getFeeData(),
      provider.getNetwork(),
      provider.getBlock("latest"),
    ]);

    res.json({
      success: true,
      stats: {
        chainId: Number(network.chainId), // ✅ BigInt → Number
        networkName: network.name,
        currentBlock: Number(blockNumber), // ✅ BigInt → Number
        gasPrice: gasPrice.toString(),
        blockTimestamp: Number(latestBlock.timestamp), // ✅ BigInt → Number
        miner: latestBlock.miner,
        txCount: latestBlock.transactions.length,
      },
    });
  } catch (err) {
    console.error("Stats error:", err);
    res
      .status(500)
      .json({ success: false, error: "Unable to fetch blockchain stats" });
  }
};

// 🔹 Submit single IoT sensor data
const submitData = async (req, res) => {
  try {
    const { sensorId, data, timestamp } = req.body;
    if (!sensorId || !data) {
      return res
        .status(400)
        .json({ success: false, error: "Missing sensorId or data" });
    }

    const ts = timestamp
      ? Math.floor(new Date(timestamp).getTime() / 1000)
      : Math.floor(Date.now() / 1000);
    const receipt = await blockchainClient.submitData(
      sensorId,
      JSON.stringify(data),
      ts
    );

    res.status(201).json({
      success: true,
      message: "Data submitted successfully",
      data: {
        sensorId,
        transactionHash: receipt.transactionHash,
        blockNumber: receipt.blockNumber,
        gasUsed: receipt.gasUsed,
        timestamp: ts,
      },
    });
  } catch (err) {
    console.error("SubmitData error:", err);
    res.status(500).json({
      success: false,
      error: "Failed to submit data",
      details: err.message,
    });
  }
};

// 🔹 Submit batch of IoT sensor data
const submitBatchData = async (req, res) => {
  try {
    // ⬇️ ⬇️ TEMPORARY LOGGING BLOCK ⬇️ ⬇️ 
    console.log('--- START OF REQUEST DEBUGGING ---');
    console.log('Headers (Content-Type):', req.headers['content-type']);
    console.log('Raw Received Body (as JSON Object):', JSON.stringify(req.body, null, 2));
    console.log('----------------------------------');
    // ⬆️ ⬆️ TEMPORARY LOGGING BLOCK ⬆️ ⬆️
    const { readings } = req.body;
    if (!readings || !Array.isArray(readings) || readings.length === 0) {
      return res
        .status(400)
        .json({ success: false, error: "Readings must be a non-empty array" });
    }

    if (readings.length > 50) {
      return res
        .status(400)
        .json({ success: false, error: "Batch too large (max 50 readings)" });
    }

    const sensorIds = [];
    const dataPoints = [];
    const timestamps = [];

    readings.forEach((r, i) => {
      if (!r.sensorId || !r.data)
        throw new Error(`Invalid reading at index ${i}`);
      sensorIds.push(r.sensorId);
      // CRITICAL LINE: convert object to string
      const dataString = JSON.stringify(r.data); 
      
      // ⬇️ ⬇️ TEMPORARY LOGGING BLOCK ⬇️ ⬇️ 
      console.log(`Reading Index ${i} Data String: ${dataString}`); 
      // ⬆️ ⬆️ TEMPORARY LOGGING BLOCK ⬆️ ⬆️
      dataPoints.push(dataString);
      timestamps.push(
        r.timestamp
          ? Math.floor(new Date(r.timestamp).getTime() / 1000)
          : Math.floor(Date.now() / 1000)
      );
    });

    const receipt = await blockchainClient.submitBatchData(
      sensorIds,
      dataPoints,
      timestamps
    );

    res.status(201).json({
      success: true,
      message: "Batch submitted successfully",
      data: {
        itemsSubmitted: receipt.itemsSubmitted,
        transactionHash: receipt.transactionHash,
        blockNumber: receipt.blockNumber,
        gasUsed: receipt.gasUsed,
      },
    });
  } catch (err) {
    console.error("SubmitBatch error:", err);
    res.status(500).json({
      success: false,
      error: "Failed to submit batch",
      details: err.message,
    });
  }
};

// 🔹 Get contract information
const getContractInfo = async (req, res) => {
  try {
    const info = await blockchainClient.getContractInfo();
    res.json({ success: true, data: info });
  } catch (err) {
    console.error("ContractInfo error:", err);
    res.status(500).json({
      success: false,
      error: "Failed to get contract info",
      details: err.message,
    });
  }
};

// 🔹 Health check
const healthCheck = async (req, res) => {
  try {
    const isHealthy = await blockchainClient.healthCheck();
    if (isHealthy) {
      res.json({ success: true, status: "healthy", blockchain: "connected" });
    } else {
      res.status(503).json({
        success: false,
        status: "unhealthy",
        blockchain: "disconnected",
      });
    }
  } catch (err) {
    console.error("HealthCheck error:", err);
    res
      .status(503)
      .json({ success: false, status: "unhealthy", error: err.message });
  }
};

module.exports = {
  getBlockchainStats,
  submitData,
  submitBatchData,
  getContractInfo,
  healthCheck,
};
