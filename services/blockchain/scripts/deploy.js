const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

// Configuration
const DATA_DIR = process.env.DATA_DIR || "/data";
const CONTRACTS_FILE = path.join(DATA_DIR, "deployed-contracts.json");

async function main() {
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
    if (!fs.existsSync(DATA_DIR)) {
        fs.mkdirSync(DATA_DIR, { recursive: true });
    }

    // Check if contracts are already deployed
    let deployedContracts = {};
    if (fs.existsSync(CONTRACTS_FILE)) {
        deployedContracts = JSON.parse(fs.readFileSync(CONTRACTS_FILE, "utf8"));
        console.log("📋 Found existing deployment records");
    }

    // Deploy IoTDataRegistry contract (we'll create this next)
    console.log("\n🚀 Deploying IoTDataRegistry...");

    try {
        const IoTDataRegistry = await hre.ethers.getContractFactory("IoTDataRegistry");
        const iotRegistry = await IoTDataRegistry.deploy();
        await iotRegistry.waitForDeployment();

        const contractAddress = await iotRegistry.getAddress();
        console.log(`✅ IoTDataRegistry deployed to: ${contractAddress}`);

        // Save deployment info
        deployedContracts.IoTDataRegistry = {
            address: contractAddress,
            deployer: deployer.address,
            deployedAt: new Date().toISOString(),
            network: network.name,
            chainId: Number(network.chainId),
        };

        // Write to file
        fs.writeFileSync(CONTRACTS_FILE, JSON.stringify(deployedContracts, null, 2));
        console.log(`💾 Deployment info saved to: ${CONTRACTS_FILE}`);

        // Export ABI for API service
        const artifactPath = path.join(__dirname, "../artifacts/contracts/IoTDataRegistry.sol/IoTDataRegistry.json");
        if (fs.existsSync(artifactPath)) {
            const artifact = JSON.parse(fs.readFileSync(artifactPath, "utf8"));
            const abiPath = path.join(DATA_DIR, "IoTDataRegistry.abi.json");
            fs.writeFileSync(abiPath, JSON.stringify(artifact.abi, null, 2));
            console.log(`📄 ABI exported to: ${abiPath}`);
        }

        console.log("\n✅ Deployment completed successfully!");
        console.log("📊 Summary:");
        console.log(`   Contract: IoTDataRegistry`);
        console.log(`   Address: ${contractAddress}`);
        console.log(`   Network: ${network.name} (${network.chainId})`);
    } catch (error) {
        console.error("❌ Deployment failed:", error);
        process.exit(1);
    }
}

// Execute deployment
main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });
