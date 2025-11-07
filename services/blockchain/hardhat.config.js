require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
    solidity: {
        version: "0.8.24",
        settings: {
            optimizer: {
                enabled: true,
                runs: 200,
            },
        },
    },

    networks: {
        // Hardhat local network configuration
        hardhat: {
            chainId: 1337,
            mining: {
                auto: true,
                interval: 0, // Mine instantly on transaction
            },
            accounts: {
                mnemonic: "test test test test test test test test test test test junk",
                count: 10,
                accountsBalance: "10000000000000000000000", // 10000 ETH per account
            },
            gas: "auto",
            gasPrice: "auto",
            blockGasLimit: 30000000,
        },

        // Localhost network (for external connections)
        localhost: {
            url: "http://127.0.0.1:8545",
            chainId: 1337,
            timeout: 60000,
        },
    },

    paths: {
        sources: "/contracts",
        tests: "./test",
        cache: "./cache",
        artifacts: "./artifacts",
    },

    // Mocha test configuration
    mocha: {
        timeout: 40000,
    },
};
