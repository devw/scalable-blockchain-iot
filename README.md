# Scalable Blockchain IoT

Lightweight private blockchain platform for storing IoT data.

## 🏗️ Architecture

* **Blockchain Service**: Hardhat Network (Ethereum-compatible)
* **API Service**: Node.js + Express + Ethers.js
* **Smart Contracts**: Solidity

## 🚀 Quick Start

```bash
# Copy configuration file
cp .env.example .env

# Start services
docker-compose up -d

# Check status
docker-compose ps
```

## 📁 Project Structure

```
scalable-blockchain-iot/
├── services/
│   ├── blockchain/       # Hardhat blockchain service
│   └── api/              # REST API service
├── contracts/            # Solidity smart contracts
├── data/                 # Blockchain persistence (Docker volume)
└── docker-compose.yml    # Service orchestration
```

## 🔧 Requirements

* Docker >= 20.10
* Docker Compose >= 2.0
* 1GB available RAM

## 📚 Documentation

See `docs/` folder for more details.

## 🔌 API Usage

### Submit Single IoT Reading

```bash
curl -X POST http://localhost:3000/api/iot/data \
-H "Content-Type: application/json" \
-d '{
  "sensorId": "sensor-001",
  "data": {
    "temperature": 23.5,
    "humidity": 60
  },
  "timestamp": "2025-11-25T11:20:00Z"
}'
```

### Submit Batch IoT Readings

```bash
curl -X POST http://localhost:3000/api/iot/batch \
-H "Content-Type: application/json" \
-d '{
  "readings": [
    {
      "sensorId": "sensor-001",
      "data": { "temperature": 22.1 },
      "timestamp": "2025-11-25T11:20:00Z"
    },
    {
      "sensorId": "sensor-002",
      "data": { "temperature": 24.7 },
      "timestamp": "2025-11-25T11:21:00Z"
    }
  ]
}'
```

## 🔎 Reading Data From the Blockchain

The current version stores IoT readings **on-chain**, but reading them back requires querying the contract directly.

### Get Contract Info

```bash
curl http://localhost:3000/api/iot/info
```

### Query Blockchain Directly

You can manually inspect blocks using JSON-RPC.

#### Get Latest Block Number

```bash
curl -s -X POST http://localhost:8545 \
-H "Content-Type: application/json" \
-d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' | jq '.result'
```

#### Read Contents of a Specific Block

Replace `0x7` with your block number:

```bash
curl -s -X POST http://localhost:8545 \
-H "Content-Type: application/json" \
-d '{"jsonrpc":"2.0","method":"eth_getBlockByNumber","params":["0x7", true],"id":1}' | jq
```

This returns:

* timestamp
* miner
* transactions in the block
* hashes
* gas used

### Optional: List All Blocks Using a Script

A helper script can be created (not included by default) to iterate and print all blocks.

## 💾 Blockchain Persistence & Snapshots

Hardhat resets the blockchain on every restart.
Snapshots allow you to **save and reload blockchain state**.

### Create Snapshot

```bash
./scripts/snapshot-helper.sh export
```

### Restore Snapshot

```bash
./scripts/snapshot-helper.sh import
```

### List Snapshots

```bash
./scripts/snapshot-helper.sh list
```

### View Saved Blockchain Data

All snapshot files are stored in:

```
data/snapshots/
```

## 🎯 Roadmap

* [x] Setup base architecture
* [x] Implement IoT smart contract
* [x] REST API for data submission
* [ ] REST API for reading IoT data back
* [ ] Kubernetes deployment (optional)

## 📄 License

MIT
