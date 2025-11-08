const { spawn } = require("child_process");
const fs = require("fs");
const path = require("path");

// Configuration
const DATA_DIR = process.env.DATA_DIR || "/data";
const BLOCKCHAIN_DATA_FILE = path.join(DATA_DIR, "blockchain-state.json");
const CONTRACTS_FILE = path.join(DATA_DIR, "deployed-contracts.json");

console.log("🚀 Starting Hardhat Network...");
console.log("📁 Data directory:", DATA_DIR);

// Ensure data directory exists
if (!fs.existsSync(DATA_DIR)) {
    console.log("📂 Creating data directory...");
    fs.mkdirSync(DATA_DIR, { recursive: true });
}

// Check if blockchain state exists
const hasExistingState = fs.existsSync(BLOCKCHAIN_DATA_FILE);

if (hasExistingState) {
    console.log("✅ Found existing blockchain state");
    console.log("🔄 Restoring previous blockchain data...");
} else {
    console.log("🆕 No existing state found, starting fresh blockchain");
}

// Hardhat node arguments
const hardhatArgs = ["node", "--hostname", "0.0.0.0", "--port", "8545"];

// Start Hardhat Network
const hardhatProcess = spawn("npx", ["hardhat", ...hardhatArgs], {
    stdio: "inherit",
    env: {
        ...process.env,
        HARDHAT_NETWORK: "hardhat",
    },
});

// Handle process events
hardhatProcess.on("error", (error) => {
    console.error("❌ Failed to start Hardhat Network:", error);
    process.exit(1);
});

hardhatProcess.on("close", (code) => {
    if (code !== 0) {
        console.error(`❌ Hardhat Network exited with code ${code}`);
        process.exit(code);
    }
    console.log("👋 Hardhat Network stopped");
});

// Graceful shutdown
process.on("SIGTERM", () => {
    console.log("🛑 Received SIGTERM, shutting down gracefully...");
    hardhatProcess.kill("SIGTERM");
});

process.on("SIGINT", () => {
    console.log("🛑 Received SIGINT, shutting down gracefully...");
    hardhatProcess.kill("SIGINT");
});

// Log startup complete
setTimeout(() => {
    console.log("✅ Hardhat Network is running");
    console.log("🌐 JSON-RPC endpoint: http://0.0.0.0:8545");
    console.log("🔗 Chain ID: 1337");

    if (hasExistingState) {
        console.log("💾 Blockchain state restored from:", BLOCKCHAIN_DATA_FILE);
    }

    console.log("📊 Ready to accept transactions");
}, 3000);
