#!/usr/bin/env node
import fs from "fs";
import path from "path";
import hre from "hardhat";
import { fileURLToPath } from "url";

// Paths
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const DATA_DIR = path.join(__dirname, "..", "data");
const CONTRACTS_FILE = path.join(DATA_DIR, "deployed-contracts.json");

// Ensure data directory exists
if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });

// Helper to save deployment info
const saveDeployment = (address, blockNumber) => {
    const deploymentInfo = {
        address,
        blockNumber,
        network: hre.network.name,
        chainId: hre.network.config.chainId,
        deployedAt: new Date().toISOString(),
    };
    fs.writeFileSync(CONTRACTS_FILE, JSON.stringify(deploymentInfo, null, 2));
    console.log(`📦 Deployment info saved to: ${CONTRACTS_FILE}`);
};

const main = async () => {
    console.log("🚀 Deploying IoTDataRegistry contract...");

    const [deployer] = await hre.ethers.getSigners();
    console.log(`Deploying with account: ${deployer.address}`);
    const balance = await hre.ethers.provider.getBalance(deployer.address);
    console.log(`Account balance: ${hre.ethers.formatEther(balance)} ETH\n`);

    const IoTDataRegistry = await hre.ethers.getContractFactory("IoTDataRegistry");
    const registry = await IoTDataRegistry.deploy();
    await registry.waitForDeployment();

    const address = await registry.getAddress();
    const blockNumber = registry.deploymentTransaction()?.blockNumber || 0;

    console.log(`✅ Contract deployed at address: ${address}`);
    console.log(`🧱 Deployment block: ${blockNumber}\n`);

    saveDeployment(address, blockNumber);
};

main()
    .then(() => {
        console.log("🎉 Deployment completed successfully!");
        process.exit(0);
    })
    .catch((err) => {
        console.error("❌ Deployment failed:", err);
        process.exit(1);
    });
