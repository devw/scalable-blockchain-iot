const express = require("express");
const cors = require("cors");
const helmet = require("helmet");
const morgan = require("morgan");
const fs = require("fs");
const path = require("path");

const config = require("./config");
const blockchainClient = require("./blockchain/client");
const healthRoutes = require("./routes/health");
const iotRoutes = require("./routes/iot");
const {
  errorHandler,
  notFoundHandler,
  requestLogger,
} = require("./middleware/errorHandler");

/**
 * Initialize Express application
 */
const createApp = () => {
  const app = express();

  // Security middleware
  app.use(helmet());
  app.use(cors({ origin: config.security.corsOrigin }));

  // Body parsing
  app.use(express.json());
  app.use(express.urlencoded({ extended: true }));

  // Logging
  if (config.server.env === "development") {
    app.use(requestLogger);
  } else {
    app.use(morgan(config.logging.format));
  }

  // Routes
  app.use("/health", healthRoutes);
  app.use("/api/iot", iotRoutes);

  // Root endpoint
  app.get("/", (req, res) => {
    res.json({
      service: "IoT Blockchain API",
      version: "1.0.0",
      status: "running",
      endpoints: {
        health: "/health",
        submitData: "POST /api/iot/data",
        submitBatch: "POST /api/iot/batch",
        contractInfo: "GET /api/iot/info",
      },
    });
  });

  // Error handling
  app.use(notFoundHandler);
  app.use(errorHandler);

  return app;
};

/**
 * Load smart contract ABI and address
 */
const loadContractConfig = async () => {
  const dataDir = "/data";
  const contractsFile = path.join(dataDir, "deployed-contracts.json");
  const abiFile = path.join(dataDir, "IoTDataRegistry.abi.json");

  // Check if files exist
  if (!fs.existsSync(contractsFile)) {
    throw new Error(
      `Contract deployment file not found: ${contractsFile}\n` +
        "Please deploy the contract first using: docker-compose exec blockchain yarn deploy"
    );
  }

  if (!fs.existsSync(abiFile)) {
    throw new Error(`Contract ABI file not found: ${abiFile}`);
  }

  // Load contract address
  const deployedContracts = JSON.parse(fs.readFileSync(contractsFile, "utf8"));
  const contractAddress = deployedContracts.IoTDataRegistry?.address;

  if (!contractAddress) {
    throw new Error(
      "IoTDataRegistry address not found in deployed-contracts.json"
    );
  }

  // Load ABI
  const abi = JSON.parse(fs.readFileSync(abiFile, "utf8"));

  return { contractAddress, abi };
};

/**
 * Initialize blockchain connection and contract
 */
const initializeBlockchain = async () => {
  try {
    console.log("🔗 Initializing blockchain connection...");

    // Connect to blockchain
    await blockchainClient.connect();

    // Load contract configuration
    const { contractAddress, abi } = await loadContractConfig();
    console.log(`📜 Contract address: ${contractAddress}`);

    // Load contract
    await blockchainClient.loadContract(contractAddress, abi);

    console.log("✅ Blockchain initialization complete");
    return true;
  } catch (error) {
    console.error("❌ Blockchain initialization failed:", error.message);
    throw error;
  }
};

/**
 * Start server
 */
const startServer = async () => {
  try {
    console.log("🚀 Starting IoT Blockchain API Server...");
    console.log(`📍 Environment: ${config.server.env}`);
    console.log(`�� Blockchain RPC: ${config.blockchain.rpcUrl}`);

    // Initialize blockchain
    await initializeBlockchain();

    // Create Express app
    const app = createApp();

    // Start listening
    const server = app.listen(config.server.port, config.server.host, () => {
      console.log("");
      console.log("✅ Server is running!");
      console.log(
        `📡 API endpoint: http://${config.server.host}:${config.server.port}`
      );
      console.log(
        `🏥 Health check: http://${config.server.host}:${config.server.port}/health`
      );
      console.log("");
      console.log("📚 Available endpoints:");
      console.log(`   POST /api/iot/data   - Submit single sensor data`);
      console.log(`   POST /api/iot/batch  - Submit batch sensor data`);
      console.log(`   GET  /api/iot/info   - Get contract information`);
      console.log("");
    });

    // Graceful shutdown
    const shutdown = async (signal) => {
      console.log(`\n⚠️  Received ${signal}, shutting down gracefully...`);

      server.close(() => {
        console.log("🛑 HTTP server closed");
        blockchainClient.disconnect();
        process.exit(0);
      });

      // Force shutdown after 10 seconds
      setTimeout(() => {
        console.error("❌ Forced shutdown after timeout");
        process.exit(1);
      }, 10000);
    };

    process.on("SIGTERM", () => shutdown("SIGTERM"));
    process.on("SIGINT", () => shutdown("SIGINT"));
  } catch (error) {
    console.error("❌ Failed to start server:", error.message);
    process.exit(1);
  }
};

// Start server if run directly
if (require.main === module) {
  startServer();
}

module.exports = { createApp, startServer, initializeBlockchain };
