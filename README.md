# Scalable Blockchain IoT

Lightweight private blockchain platform for storing IoT data.

## 🏗️ Architecture

* **Blockchain Service**: Hardhat Network (Ethereum-compatible)
* **API Service**: Node.js + Express + Ethers.js
* **Smart Contracts**: Solidity

## 🚀 Quick Start

```bash
# Start services
docker-compose up -d

# Deploy smart contract (required on first run)
docker-compose exec blockchain yarn deploy

# Restart API to load the contract
docker-compose restart api

# Check status
curl http://localhost:3000/health
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

---

## 🔌 API Routes

### Base URL

```
http://localhost:3000
```

---

### 📊 Health & Status

#### `GET /health`

Check API and blockchain connectivity.

**Example:**

```bash
curl http://localhost:3000/health
```

**Response:**

```json
{
  "success": true,
  "status": "healthy",
  "blockchain": "connected"
}
```

---

#### `GET /api/iot/stats`

Get blockchain statistics and network information.

**Example:**

```bash
curl http://localhost:3000/api/iot/stats
```

**Response:**

```json
{
  "success": true,
  "stats": {
    "chainId": 1337,
    "networkName": "hardhat",
    "currentBlock": 42,
    "gasPrice": "1000000000",
    "blockTimestamp": 1732096845,
    "miner": "0x0000000000000000000000000000000000000000",
    "txCount": 1
  }
}
```

---

#### `GET /api/iot/info`

Get smart contract information.

**Example:**

```bash
curl http://localhost:3000/api/iot/info
```

**Response:**

```json
{
  "success": true,
  "data": {
    "totalSubmissions": "7",
    "contractAddress": "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512"
  }
}
```

---

### 📝 Submit IoT Data

#### `POST /api/iot/data`

Submit a single IoT sensor reading to the blockchain.

**Request Body:**

```json
{
  "sensorId": "sensor-001",
  "data": {
    "temperature": 23.5,
    "humidity": 60
  },
  "timestamp": "2025-11-25T11:20:00Z"
}
```

**Example:**

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

**Response:**

```json
{
  "success": true,
  "message": "Data submitted successfully",
  "data": {
    "sensorId": "sensor-001",
    "transactionHash": "0x1234...",
    "blockNumber": 5,
    "gasUsed": "45678",
    "timestamp": 1732531200
  }
}
```

**Notes:**

* `timestamp` is optional (defaults to current time)
* `data` can contain any JSON object
* Returns transaction hash and block number

---

#### `POST /api/iot/batch`

Submit multiple IoT sensor readings in a single transaction.

**Request Body:**

```json
{
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
}
```

**Example:**

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

**Response:**

```json
{
  "success": true,
  "message": "Batch submitted successfully",
  "data": {
    "itemsSubmitted": 2,
    "transactionHash": "0x5678...",
    "blockNumber": 6,
    "gasUsed": "89012"
  }
}
```

**Notes:**

* Maximum 50 readings per batch
* More gas-efficient than individual submissions
* All readings must be valid or the entire batch fails

---

### ⚠️ Error Responses

All endpoints return error responses in this format:

```json
{
  "success": false,
  "error": "Error message description"
}
```

**Common HTTP Status Codes:**

* `200` - Success
* `201` - Created (data submitted)
* `400` - Bad Request (invalid input)
* `500` - Internal Server Error (blockchain or server issue)
* `503` - Service Unavailable (blockchain disconnected)

---

## 🔄 Service Management

### 🔁 Complete Restart (rebuild + deploy)

When you modify code or Dockerfiles:

```bash
# Stop everything
docker-compose down

# Rebuild and start
docker-compose up -d --build

# Deploy contract
docker-compose exec blockchain yarn deploy

# Restart API
docker-compose restart api
```

### ⚡ Quick Restart (no code changes)

If services just need a restart:

```bash
# Restart blockchain (⚠️ this resets blockchain state!)
docker-compose restart blockchain

# Redeploy contract (required after blockchain restart)
docker-compose exec blockchain yarn deploy

# Restart API
docker-compose restart api
```

### 📜 View Logs

```bash
# API logs
docker logs -f iot-api

# Blockchain logs
docker logs -f blockchain-hardhat

# Both services
docker-compose logs -f
```

### 🔧 Verify Services

```bash
# Check blockchain
curl http://localhost:8545

# Check API health
curl http://localhost:3000/health

# Check contract info
curl http://localhost:3000/api/iot/info
```

---

## 🔎 Reading Data From the Blockchain

### Query Latest Block Number

```bash
curl -s -X POST http://localhost:8545 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' | jq '.result'
```

### Read Specific Block Contents

Replace `0x7` with your block number:

```bash
curl -s -X POST http://localhost:8545 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_getBlockByNumber","params":["0x7", true],"id":1}' | jq
```

---

## 💾 Blockchain Persistence & Snapshots

⚠️ **Hardhat resets on every restart!** Use snapshots to preserve state.

```bash
# Create snapshot
./scripts/snapshot-helper.sh export

# Restore snapshot
./scripts/snapshot-helper.sh import

# List snapshots
./scripts/snapshot-helper.sh list
```

Snapshots are stored in `data/snapshots/`

---

## 🎯 Roadmap

* [x] Setup base architecture
* [x] Implement IoT smart contract
* [x] REST API for data submission
* [x] Health check and stats endpoints
* [ ] REST API for reading IoT data back
* [ ] Kubernetes deployment (optional)

---

## 📚 Documentation

See `docs/` folder for more details.

## 📄 License

MIT