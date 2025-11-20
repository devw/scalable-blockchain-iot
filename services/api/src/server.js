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
    app.use(morgan("dev"));
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

  if (!fs.existsSync(contractsFile)) {
    throw new Error(
      `Contract deployment file not found: ${contractsFile}\nPlease deploy the contract first using: docker-compose exec blockchain yarn deploy`
    );
  }

  if (!fs.existsSync(abiFile)) {
    throw new Error(`Contract ABI file not found: ${abiFile}`);
  }

  const deployedContracts = JSON.parse(fs.readFileSync(contractsFile, "utf8"));
  const contractAddress = deployedContracts.IoTDataRegistry?.address;

  if (!contractAddress) {
    throw new Error(
      "IoTDataRegistry address not found in deployed-contracts.json"
    );
  }

  const abi = JSON.parse(fs.readFileSync(abiFile, "utf8"));
  return { contractAddress, abi };
};

/**

* Initialize blockchain connection and contract
  */
const initializeBlockchain = async () => {
  try {
    console.log("🔗 Initializing blockchain connection...");
    await blockchainClient.connect();

    const { contractAddress, abi } = await loadContractConfig();
    console.log(`📜 Contract address: ${contractAddress}`);

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
    console.log(`📡 Blockchain RPC: ${config.blockchain.rpcUrl}`);

    await initializeBlockchain();

    const app = createApp();

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

    const shutdown = async (signal) => {
      console.log(`\n⚠️  Received ${signal}, shutting down gracefully...`);
      server.close(() => {
        console.log("🛑 HTTP server closed");
        blockchainClient.disconnect();
        process.exit(0);
      });
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

if (require.main === module) {
  startServer();
}

module.exports = { createApp, startServer, initializeBlockchain };
