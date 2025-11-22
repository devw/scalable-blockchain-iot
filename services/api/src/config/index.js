module.exports = {
  server: {
    port: process.env.PORT || 3000,
    host: process.env.HOST || "0.0.0.0",
    env: process.env.NODE_ENV || "development",
  },
  blockchain: {
    rpcUrl: process.env.BLOCKCHAIN_RPC_URL || "http://localhost:8545",
  },
  security: {
    corsOrigin: process.env.CORS_ORIGIN || "*",
  },
  logging: {
    format: process.env.LOG_FORMAT || "combined",
  },
};
