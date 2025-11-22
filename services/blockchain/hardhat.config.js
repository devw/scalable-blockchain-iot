require("@nomicfoundation/hardhat-ethers");
require("dotenv").config();

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
    solidity: {
        version: "0.8.20",
        settings: {
            optimizer: {
                enabled: true,
                runs: 200,
            },
        },
    },
    networks: {
        hardhat: {
            chainId: 1337,
            mining: {
                auto: true,
                interval: 0,
            },
        },
        localhost: {
            url: "http://127.0.0.1:8545",
            chainId: 1337,
        },
        ganache: {
            url: "http://blockchain-ganache:8545", // Porta interna, non 8546
            chainId: 1337,
            accounts: {
                mnemonic: "misery canoe armor cross improve robot permit picture ozone wife awful scout",
            },
        },
    },
    paths: {
        sources: "/app/contracts",
        tests: "./test",
        cache: "./cache",
        artifacts: "./artifacts",
    },
};
