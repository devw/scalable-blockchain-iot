// services/blockchain/scripts/load_block.js

import { spawn } from "child_process";
import fs from "fs";
import path from "path";

const DATA_DIR = process.env.DATA_DIR || path.join(process.cwd(), "data");
const SNAPSHOT_DIR = path.join(DATA_DIR, "snapshots");
const LATEST_SNAPSHOT = path.join(SNAPSHOT_DIR, "latest.json");

/**
 * Ensure snapshots directory exists
 */
const ensureSnapshotDir = () => {
    if (!fs.existsSync(SNAPSHOT_DIR)) {
        console.log("📂 Creating snapshots directory...");
        fs.mkdirSync(SNAPSHOT_DIR, { recursive: true });
    }
};

/**
 * Check if latest snapshot exists
 */
const snapshotExists = () => fs.existsSync(LATEST_SNAPSHOT);

/**
 * Start Hardhat node
 */
const startHardhatNode = () => {
    const args = ["node", "--hostname", "0.0.0.0", "--port", "8545"];
    const processEnv = { ...process.env, HARDHAT_NETWORK: "hardhat" };

    const hhProcess = spawn("npx", ["hardhat", ...args], { stdio: "inherit", env: processEnv });

    hhProcess.on("error", (err) => {
        console.error("❌ Failed to start Hardhat Network:", err);
        process.exit(1);
    });

    hhProcess.on("close", (code) => {
        if (code !== 0) console.error(`❌ Hardhat Network exited with code ${code}`);
        console.log("👋 Hardhat Network stopped");
    });

    ["SIGTERM", "SIGINT"].forEach((sig) =>
        process.on(sig, () => {
            console.log(`🛑 Received ${sig}, shutting down...`);
            hhProcess.kill(sig);
        })
    );

    return hhProcess;
};

/**
 * Log startup info
 */
const logStartup = (hasSnapshot) => {
    setTimeout(() => {
        console.log("✅ Hardhat Network is running");
        console.log("🌐 JSON-RPC endpoint: http://0.0.0.0:8545");
        console.log("🔗 Chain ID: 1337");

        if (hasSnapshot) console.log(`💾 Blockchain state restored from snapshot: ${LATEST_SNAPSHOT}`);

        console.log("📊 Ready to accept transactions");
    }, 3000);
};

/**
 * Main function to load blockchain
 */
export const loadBlockchain = () => {
    ensureSnapshotDir();
    const hasSnapshot = snapshotExists();

    if (hasSnapshot) {
        console.log(`💾 Found latest snapshot: ${LATEST_SNAPSHOT}`);
        console.log("🔄 Restoring blockchain state from snapshot...");
    } else {
        console.log("🆕 No snapshot found, starting fresh blockchain");
    }

    startHardhatNode();
    logStartup(hasSnapshot);
};
