const { ethers } = require("ethers");
const config = require("../config");

/**
 * Blockchain Client
 * Handles connection and interaction with Hardhat Network
 */
class BlockchainClient {
  constructor() {
    this.provider = null;
    this.contract = null;
    this.signer = null;
    this.isConnected = false;
  }

  /**
   * Initialize connection to blockchain
   */
  async connect() {
    try {
      console.log("🔗 Connecting to blockchain...");
      console.log(`   RPC URL: ${config.blockchain.rpcUrl}`);

      // Create provider
      this.provider = new ethers.JsonRpcProvider(config.blockchain.rpcUrl);

      // Test connection
      const network = await this.provider.getNetwork();
      console.log(
        `✅ Connected to network: ${network.name} (Chain ID: ${network.chainId})`
      );

      // Get default signer (first account from Hardhat)
      this.signer = await this.provider.getSigner(0);
      const address = await this.signer.getAddress();
      console.log(`👤 Using signer: ${address}`);

      this.isConnected = true;
      return true;
    } catch (error) {
      console.error("❌ Failed to connect to blockchain:", error.message);
      this.isConnected = false;
      throw error;
    }
  }

  /**
   * Load IoTDataRegistry contract
   * @param {string} contractAddress - Deployed contract address
   * @param {Array} abi - Contract ABI
   */
  async loadContract(contractAddress, abi) {
    if (!this.isConnected) {
      throw new Error("Not connected to blockchain. Call connect() first.");
    }

    if (!contractAddress) {
      throw new Error("Contract address is required");
    }

    if (!abi || abi.length === 0) {
      throw new Error("Contract ABI is required");
    }

    try {
      console.log(`📜 Loading contract at: ${contractAddress}`);

      this.contract = new ethers.Contract(contractAddress, abi, this.signer);

      // Verify contract exists
      const code = await this.provider.getCode(contractAddress);
      if (code === "0x") {
        throw new Error("No contract deployed at the specified address");
      }

      console.log("✅ Contract loaded successfully");
      return this.contract;
    } catch (error) {
      console.error("❌ Failed to load contract:", error.message);
      throw error;
    }
  }

  /**
   * Submit IoT data to blockchain
   * @param {string} sensorId - Sensor identifier
   * @param {string} data - Sensor data
   * @param {number} timestamp - Data timestamp
   * @returns {Object} Transaction receipt
   */
  async submitData(sensorId, data, timestamp) {
    if (!this.contract) {
      throw new Error("Contract not loaded. Call loadContract() first.");
    }

    try {
      console.log(`📤 Submitting data for sensor: ${sensorId}`);

      // Call smart contract function
      const tx = await this.contract.submitData(sensorId, data, timestamp);
      console.log(`⏳ Transaction sent: ${tx.hash}`);

      // Wait for confirmation
      const receipt = await tx.wait();
      console.log(`✅ Transaction confirmed in block: ${receipt.blockNumber}`);

      return {
        transactionHash: receipt.hash,
        blockNumber: receipt.blockNumber,
        gasUsed: receipt.gasUsed.toString(),
      };
    } catch (error) {
      console.error("❌ Failed to submit data:", error.message);
      throw error;
    }
  }

  /**
   * Submit batch of IoT data
   * @param {Array} sensorIds - Array of sensor identifiers
   * @param {Array} dataPoints - Array of sensor data
   * @param {Array} timestamps - Array of timestamps
   * @returns {Object} Transaction receipt
   */
  async submitBatchData(sensorIds, dataPoints, timestamps) {
    if (!this.contract) {
      throw new Error("Contract not loaded. Call loadContract() first.");
    }

    if (
      sensorIds.length !== dataPoints.length ||
      dataPoints.length !== timestamps.length
    ) {
      throw new Error("Arrays length mismatch");
    }

    try {
      console.log(`📤 Submitting batch of ${sensorIds.length} readings`);

      const tx = await this.contract.submitBatchData(
        sensorIds,
        dataPoints,
        timestamps
      );
      console.log(`⏳ Batch transaction sent: ${tx.hash}`);

      const receipt = await tx.wait();
      console.log(`✅ Batch confirmed in block: ${receipt.blockNumber}`);

      return {
        transactionHash: receipt.hash,
        blockNumber: receipt.blockNumber,
        gasUsed: receipt.gasUsed.toString(),
        itemsSubmitted: sensorIds.length,
      };
    } catch (error) {
      console.error("❌ Failed to submit batch:", error.message);
      throw error;
    }
  }

  /**
   * Get contract information
   * @returns {Object} Contract info
   */
  async getContractInfo() {
    if (!this.contract) {
      throw new Error("Contract not loaded");
    }

    try {
      const info = await this.contract.getContractInfo();
      return {
        totalSubmissions: info.totalSubs.toString(),
        contractAddress: info.contractAddr,
      };
    } catch (error) {
      console.error("❌ Failed to get contract info:", error.message);
      throw error;
    }
  }

  /**
   * Check if connection is healthy
   * @returns {boolean}
   */
  async healthCheck() {
    try {
      if (!this.provider) return false;

      await this.provider.getBlockNumber();
      return true;
    } catch (error) {
      return false;
    }
  }

  /**
   * Disconnect from blockchain
   */
  disconnect() {
    this.provider = null;
    this.contract = null;
    this.signer = null;
    this.isConnected = false;
    console.log("🔌 Disconnected from blockchain");
  }
}

// Export singleton instance
module.exports = new BlockchainClient();
