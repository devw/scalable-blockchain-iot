require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();

module.exports = {
  solidity: {
    version: "0.8.24",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200
      }
    }
  },
  
  networks: {
    hardhat: {
      chainId: 1337,
      mining: {
        auto: true,
        interval: 0
      },
      accounts: {
        mnemonic: "test test test test test test test test test test test junk",
        count: 10,
        accountsBalance: "10000000000000000000000"
      },
      gas: "auto",
      gasPrice: "auto",
      blockGasLimit: 30000000
    },
    
    localhost: {
      url: "http://127.0.0.1:8545",
      chainId: 1337,
      timeout: 60000
    }
  },
  
  paths: {
    root: "/",                    // ← Set root to allow /contracts
    sources: "/contracts",
    tests: "./test",
    cache: "./cache",
    artifacts: "./artifacts"
  },
  
  mocha: {
    timeout: 40000
  }
};