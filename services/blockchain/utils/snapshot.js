const { ethers } = require("ethers");
const fs = require("fs");
const path = require("path");

const SNAPSHOT_DIR = process.env.SNAPSHOT_DIR || "/data/snapshots";
const RPC_URL = process.env.RPC_URL || "http://localhost:8545";

const ensureSnapshotDirectory = () => {
    if (!fs.existsSync(SNAPSHOT_DIR)) {
        fs.mkdirSync(SNAPSHOT_DIR, { recursive: true });
        console.log(`✓ Created snapshot directory: ${SNAPSHOT_DIR}`);
    }
};

const getProvider = () => new ethers.JsonRpcProvider(RPC_URL);

/**
 * Read all IoT events from the blockchain
 * @param {ethers.Contract} contract - Contract instance
 * @param {number} fromBlock - Starting block (default: 0)
 * @param {number|string} toBlock - Ending block (default: 'latest')
 * @returns {Array} Array of IoT event data
 */
const readIoTEvents = async (contract, fromBlock = 0, toBlock = "latest") => {
    try {
        console.log(`📖 Reading IoT events from block ${fromBlock} to ${toBlock}...`);

        const events = await contract.queryFilter("IoTDataReceived", fromBlock, toBlock);

        const iotData = events.map((event) => ({
            sender: event.args.sender,
            sensorId: event.args.sensorId,
            data: event.args.data,
            timestamp: Number(event.args.timestamp),
            blockNumber: Number(event.args.blockNumber),
            transactionHash: event.transactionHash,
        }));

        console.log(`✓ Found ${iotData.length} IoT events`);

        // Calculate approximate data size
        const dataSize = JSON.stringify(iotData).length;
        const dataSizeKB = (dataSize / 1024).toFixed(2);
        console.log(`✓ Events data size: ${dataSizeKB} KB`);

        return iotData;
    } catch (error) {
        console.warn(`⚠️  Could not read IoT events: ${error.message}`);
        return [];
    }
};

const exportSnapshot = async () => {
    try {
        console.log("📸 Creating blockchain snapshot...");
        ensureSnapshotDirectory();

        const provider = getProvider();
        const blockNumber = await provider.getBlockNumber();
        console.log(`✓ Current block: ${blockNumber}`);

        const deploymentPath = path.join(__dirname, "..", "deployment.json");
        let deployment = null;

        if (fs.existsSync(deploymentPath)) {
            deployment = JSON.parse(fs.readFileSync(deploymentPath, "utf8"));
            console.log(`✓ Found deployment: ${deployment.address}`);
        }

        const accounts = await provider.listAccounts();
        const accountsData = await Promise.all(
            accounts.map(async (account) => {
                const address = account.address;
                const balance = await provider.getBalance(address);
                return { address, balance: balance.toString() };
            })
        );

        console.log(`✓ Captured ${accountsData.length} accounts`);

        let contractState = null;
        let iotEvents = [];

        if (deployment) {
            try {
                const artifactPath = path.join(
                    __dirname,
                    "..",
                    "artifacts",
                    "contracts",
                    "IoTDataRegistry.sol",
                    "IoTDataRegistry.json"
                );

                if (fs.existsSync(artifactPath)) {
                    const artifact = JSON.parse(fs.readFileSync(artifactPath, "utf8"));
                    const contract = new ethers.Contract(deployment.address, artifact.abi, provider);
                    const code = await provider.getCode(deployment.address);

                    contractState = {
                        address: deployment.address,
                        code,
                        deploymentBlock: deployment.blockNumber || 0,
                    };

                    console.log(`✓ Captured contract state`);

                    // Read IoT events from blockchain
                    iotEvents = await readIoTEvents(contract, 0, "latest");
                }
            } catch (error) {
                console.warn(`⚠️  Could not capture contract state: ${error.message}`);
            }
        }

        const snapshot = {
            version: "2.0.0", // Bumped version to indicate IoT events support
            timestamp: new Date().toISOString(),
            blockNumber,
            accounts: accountsData,
            deployment,
            contractState,
            iotEvents, // Added IoT events data
            iotEventsCount: iotEvents.length,
            network: {
                chainId: (await provider.getNetwork()).chainId.toString(),
                name: "hardhat",
            },
        };

        const filename = `snapshot-${Date.now()}.json`;
        const filepath = path.join(SNAPSHOT_DIR, filename);
        fs.writeFileSync(filepath, JSON.stringify(snapshot, null, 2));

        const latestPath = path.join(SNAPSHOT_DIR, "latest.json");
        fs.writeFileSync(latestPath, JSON.stringify(snapshot, null, 2));

        console.log(`✓ Snapshot saved: ${filename}`);
        console.log(`✓ Latest snapshot updated`);
        console.log(`✅ Snapshot created successfully\n`);

        return true;
    } catch (error) {
        console.error(`❌ Snapshot export failed: ${error.message}`);
        return false;
    }
};

const importSnapshot = async (snapshotFile = "latest.json") => {
    try {
        console.log(`📥 Restoring blockchain snapshot: ${snapshotFile}...`);

        const filepath = path.join(SNAPSHOT_DIR, snapshotFile);

        if (!fs.existsSync(filepath)) {
            console.warn(`⚠️  Snapshot file not found: ${filepath}`);
            console.log("Starting with fresh blockchain state");
            return false;
        }

        const snapshot = JSON.parse(fs.readFileSync(filepath, "utf8"));
        console.log(`✓ Loaded snapshot from ${snapshot.timestamp}`);
        console.log(`✓ Snapshot version: ${snapshot.version}`);
        console.log(`✓ Block number: ${snapshot.blockNumber}`);

        if (snapshot.deployment) {
            const deploymentPath = path.join(__dirname, "..", "deployment.json");
            fs.writeFileSync(deploymentPath, JSON.stringify(snapshot.deployment, null, 2));
            console.log(`✓ Restored deployment info: ${snapshot.deployment.address}`);
        }

        // Show IoT events info if available
        if (snapshot.iotEvents && snapshot.iotEvents.length > 0) {
            console.log(`✓ Snapshot contains ${snapshot.iotEvents.length} IoT events`);
            console.log(`   - Data preserved for reference`);
            console.log(`   - Events can be viewed in snapshot file`);
        }

        console.log(`\n⚠️  Note: Hardhat resets on restart. This snapshot provides:`);
        console.log(`   - Contract deployment reference`);
        console.log(`   - Account configurations`);
        console.log(`   - IoT events data (read-only reference)`);
        console.log(`   - State documentation`);
        console.log(`\n💡 To restore IoT data, redeploy contract and resubmit data from snapshot`);
        console.log(`\n✅ Snapshot restored (reference mode)\n`);

        return true;
    } catch (error) {
        console.error(`❌ Snapshot import failed: ${error.message}`);
        return false;
    }
};

const listSnapshots = () => {
    try {
        ensureSnapshotDirectory();

        const files = fs
            .readdirSync(SNAPSHOT_DIR)
            .filter((f) => f.endsWith(".json"))
            .sort()
            .reverse();

        if (files.length === 0) {
            console.log("No snapshots found");
            return;
        }

        console.log("\n📋 Available Snapshots:");
        console.log("=".repeat(60));

        files.forEach((file) => {
            const filepath = path.join(SNAPSHOT_DIR, file);
            const snapshot = JSON.parse(fs.readFileSync(filepath, "utf8"));
            console.log(`\n${file}`);
            console.log(`  Version: ${snapshot.version || "1.0.0"}`);
            console.log(`  Timestamp: ${snapshot.timestamp}`);
            console.log(`  Block: ${snapshot.blockNumber}`);
            console.log(`  Accounts: ${snapshot.accounts.length}`);
            if (snapshot.deployment) {
                console.log(`  Contract: ${snapshot.deployment.address}`);
            }
            if (snapshot.iotEventsCount !== undefined) {
                console.log(`  IoT Events: ${snapshot.iotEventsCount}`);
            }
        });

        console.log("\n" + "=".repeat(60) + "\n");
    } catch (error) {
        console.error(`❌ List failed: ${error.message}`);
    }
};

const main = async () => {
    const command = process.argv[2];

    switch (command) {
        case "export":
            await exportSnapshot();
            break;
        case "import":
            const file = process.argv[3] || "latest.json";
            await importSnapshot(file);
            break;
        case "list":
            listSnapshots();
            break;
        default:
            console.log(`
Blockchain Snapshot Manager

Usage:
  node utils/snapshot.js export           - Create new snapshot with IoT events
  node utils/snapshot.js import [file]    - Restore from snapshot
  node utils/snapshot.js list             - List available snapshots
      `);
            process.exit(1);
    }
};

module.exports = { exportSnapshot, importSnapshot, listSnapshots };

if (require.main === module) {
    main()
        .then(() => process.exit(0))
        .catch((error) => {
            console.error(error);
            process.exit(1);
        });
}
