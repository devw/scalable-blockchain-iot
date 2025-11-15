const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

// Configuration
const DATA_DIR = process.env.DATA_DIR || "/data";
const CONTRACTS_FILE = path.join(DATA_DIR, "deployed-contracts.json");

/**
 * Ensure data directory exists
 */
const ensureDataDir = () => {
    if (!fs.existsSync(DATA_DIR)) {
        fs.mkdirSync(DATA_DIR, { recursive: true });
    }
};

/**
 * Load existing deployment records
 */
const loadDeployedContracts = () => {
    if (fs.existsSync(CONTRACTS_FILE)) {
        console.log("📋 Found existing deployment records");
        return JSON.parse(fs.readFileSync(CONTRACTS_FILE, "utf8"));
    }
    return {};
};

/**
 * Save deployment info to file
 */
const saveDeploymentInfo = (contractName, info) => {
    const deployedContracts = loadDeployedContracts();
    deployedContracts[contractName] = info;

    fs.writeFileSync(CONTRACTS_FILE, JSON.stringify(deployedContracts, null, 2));
    console.log(`💾 Deployment info saved to: ${CONTRACTS_FILE}`);
};

/**
 * Export contract ABI to data directory
 */
const exportABI = (contractName) => {
    const artifactPath = path.join(__dirname, `../artifacts/contracts/${contractName}.sol/${contractName}.json`);

    if (!fs.existsSync(artifactPath)) {
        console.warn(`⚠️  Artifact not found at: ${artifactPath}`);
        return false;
    }

    const artifact = JSON.parse(fs.readFileSync(artifactPath, "utf8"));
    const abiPath = path.join(DATA_DIR, `${contractName}.abi.json`);

    fs.writeFileSync(abiPath, JSON.stringify(artifact.abi, null, 2));
    console.log(`📄 ABI exported to: ${abiPath}`);

    return true;
};

/**
 * Deploy IoTDataRegistry contract
 */
const deployIoTDataRegistry = async (deployer, network) => {
    console.log("\n🚀 Deploying IoTDataRegistry...");

    const IoTDataRegistry = await hre.ethers.getContractFactory("IoTDataRegistry");
    const contract = await IoTDataRegistry.deploy();
    await contract.waitForDeployment();

    const address = await contract.getAddress();
    console.log(`✅ IoTDataRegistry deployed to: ${address}`);

    // Save deployment info
    const deploymentInfo = {
        address,
        deployer: deployer.address,
        deployedAt: new Date().toISOString(),
        network: network.name,
        chainId: Number(network.chainId),
    };

    saveDeploymentInfo("IoTDataRegistry", deploymentInfo);
    exportABI("IoTDataRegistry");

    return { address, ...deploymentInfo };
};

/**
 * Main deployment function
 */
const main = async () => {
    console.log("📝 Starting contract deployment...");

    // Get network info
    const network = await hre.ethers.provider.getNetwork();
    console.log(`🌐 Network: ${network.name} (Chain ID: ${network.chainId})`);

    // Get deployer account
    const [deployer] = await hre.ethers.getSigners();
    console.log(`👤 Deploying contracts with account: ${deployer.address}`);

    const balance = await hre.ethers.provider.getBalance(deployer.address);
    console.log(`💰 Account balance: ${hre.ethers.formatEther(balance)} ETH`);

    // Ensure data directory exists
    ensureDataDir();

    // Deploy contract
    const deployment = await deployIoTDataRegistry(deployer, network);

    // Summary
    console.log("\n✅ Deployment completed successfully!");
    console.log("📊 Summary:");
    console.log(`   Contract: IoTDataRegistry`);
    console.log(`   Address: ${deployment.address}`);
    console.log(`   Network: ${network.name} (${network.chainId})`);
};

// Execute deployment
main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error("❌ Deployment failed:", error);
        process.exit(1);
    });
