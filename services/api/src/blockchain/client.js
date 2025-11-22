const { ethers } = require("ethers");
const config = require("../config");

/**
 * Functional Blockchain Client
 */
const blockchainClient = (() => {
  let provider = null;
  let signer = null;
  let contract = null;
  let isConnected = false;

  return {
    // Connect to blockchain
    // Connect to blockchain
    async connect() {
      try {
        console.log("🔗 Connecting to blockchain...");
        console.log(`   RPC URL: ${config.blockchain.rpcUrl}`);

        provider = new ethers.JsonRpcProvider(config.blockchain.rpcUrl);

        // Use PRIVATE_KEY if provided, otherwise use default signer
        if (process.env.PRIVATE_KEY) {
          console.log("🔑 Using private key from environment");
          signer = new ethers.Wallet(process.env.PRIVATE_KEY, provider);
        } else {
          console.log("🔑 Using default provider signer");
          signer = await provider.getSigner(0);
        }

        const address = await signer.getAddress();
        const network = await provider.getNetwork();

        console.log(
          `✅ Connected to network: ${network.name} (Chain ID: ${network.chainId})`
        );
        console.log(`👤 Using signer: ${address}`);

        isConnected = true;
        return true;
      } catch (error) {
        console.error("❌ Failed to connect to blockchain:", error.message);
        throw error;
      }
    },

    // Get provider safely
    getProvider() {
      if (!provider) throw new Error("Blockchain provider not initialized");
      return provider;
    },

    // Load a contract
    async loadContract(contractAddress, abi) {
      if (!isConnected) throw new Error("Not connected to blockchain");
      if (!contractAddress) throw new Error("Contract address required");
      if (!abi || !abi.length) throw new Error("Contract ABI required");

      contract = new ethers.Contract(contractAddress, abi, signer);

      const code = await provider.getCode(contractAddress);
      if (code === "0x")
        throw new Error("No contract deployed at this address");

      console.log(`📜 Contract loaded at: ${contractAddress}`);
      return contract;
    },

    // Submit single data
    async submitData(sensorId, data, timestamp) {
      if (!contract) throw new Error("Contract not loaded");
      const tx = await contract.submitData(sensorId, data, timestamp);
      const receipt = await tx.wait();
      return {
        transactionHash: receipt.hash,
        blockNumber: receipt.blockNumber,
        gasUsed: receipt.gasUsed.toString(),
      };
    },

    // Submit batch data
    async submitBatchData(sensorIds, dataPoints, timestamps) {
      if (!contract) throw new Error("Contract not loaded");
      if (
        sensorIds.length !== dataPoints.length ||
        dataPoints.length !== timestamps.length
      )
        throw new Error("Arrays length mismatch");

      const tx = await contract.submitBatchData(
        sensorIds,
        dataPoints,
        timestamps
      );
      const receipt = await tx.wait();
      return {
        transactionHash: receipt.hash,
        blockNumber: receipt.blockNumber,
        gasUsed: receipt.gasUsed.toString(),
        itemsSubmitted: sensorIds.length,
      };
    },

    // Get contract info
    async getContractInfo() {
      if (!contract) throw new Error("Contract not loaded");
      const info = await contract.getContractInfo();
      return {
        totalSubmissions: info.totalSubs.toString(),
        contractAddress: info.contractAddr,
      };
    },

    // Health check
    async healthCheck() {
      if (!provider) return false;
      try {
        await provider.getBlockNumber();
        return true;
      } catch {
        return false;
      }
    },

    // Disconnect
    disconnect() {
      provider = null;
      signer = null;
      contract = null;
      isConnected = false;
      console.log("🔌 Disconnected from blockchain");
    },
  };
})();

module.exports = blockchainClient;
