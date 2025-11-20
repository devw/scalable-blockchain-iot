const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

/**
 * Saves deployment information
 * @param {string} contractAddress
 * @param {number} blockNumber
 */
const saveDeploymentInfo = (contractAddress, blockNumber) => {
    const deploymentInfo = {
        address: contractAddress,
        blockNumber,
        network: hre.network.name,
        chainId: hre.network.config.chainId,
        deployedAt: new Date().toISOString(),
    };

    const deploymentPath = path.join(__dirname, "..", "deployment.json");
    fs.writeFileSync(deploymentPath, JSON.stringify(deploymentInfo, null, 2));

    console.log(`✓ Deployment info saved to deployment.json`);
};

/**
 * Main deployment function
 */
const main = async () => {
    console.log("\n🚀 Starting deployment...\n");

    // Get deployer account
    const [deployer] = await hre.ethers.getSigners();
    console.log(`Deploying contracts with account: ${deployer.address}`);

    const balance = await hre.ethers.provider.getBalance(deployer.address);
    console.log(`Account balance: ${hre.ethers.formatEther(balance)} ETH\n`);

    // Deploy IoTDataRegistry
    console.log("📝 Deploying IoTDataRegistry...");
    const IoTDataRegistry = await hre.ethers.getContractFactory("IoTDataRegistry");
    const registry = await IoTDataRegistry.deploy();

    await registry.waitForDeployment();

    const address = await registry.getAddress();
    const deploymentTx = registry.deploymentTransaction();
    const blockNumber = deploymentTx?.blockNumber || 0;

    console.log(`✓ IoTDataRegistry deployed to: ${address}`);
    console.log(`✓ Deployment block: ${blockNumber}\n`);

    // Save deployment info
    saveDeploymentInfo(address, blockNumber);

    console.log("✅ Deployment completed successfully!\n");
};

// Execute deployment
main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error("\n❌ Deployment failed:", error);
        process.exit(1);
    });
