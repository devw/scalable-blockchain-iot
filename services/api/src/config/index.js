require("dotenv").config();

/**
 * Application Configuration
 * Centralized configuration management using environment variables
 */
const config = {
  // Server Configuration
  server: {
    port: process.env.API_PORT || 3000,
    host: process.env.API_HOST || "0.0.0.0",
    env: process.env.NODE_ENV || "development",
  },

  // Blockchain Configuration
  blockchain: {
    rpcUrl: process.env.BLOCKCHAIN_RPC_URL || "http://blockchain:8545",
    chainId: parseInt(process.env.BLOCKCHAIN_CHAIN_ID || "1337", 10),
    contractAddress: process.env.IOT_CONTRACT_ADDRESS || "",
  },

  // API Configuration
  api: {
    basePath: "/api",
    version: "v1",
  },

  // Logging Configuration
  logging: {
    level: process.env.LOG_LEVEL || "info",
    format: process.env.NODE_ENV === "production" ? "combined" : "dev",
  },

  // Security Configuration
  security: {
    corsOrigin: process.env.CORS_ORIGIN || "*",
    rateLimitWindowMs: 15 * 60 * 1000, // 15 minutes
    rateLimitMax: 100, // Max 100 requests per window
  },
};

/**
 * Validate required configuration
 */
function validateConfig() {
  const required = [
    { key: "blockchain.rpcUrl", value: config.blockchain.rpcUrl },
  ];

  const missing = required.filter(({ value }) => !value);

  if (missing.length > 0) {
    const missingKeys = missing.map(({ key }) => key).join(", ");
    throw new Error(`Missing required configuration: ${missingKeys}`);
  }
}

// Validate on load
try {
  validateConfig();
} catch (error) {
  console.error("❌ Configuration error:", error.message);
  process.exit(1);
}

module.exports = config;
