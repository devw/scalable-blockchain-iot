# IoT API Service

This README describes the setup, usage, and troubleshooting specific to the API service in the IoT blockchain infrastructure.

---

## 🚀 Setup

### Build and Start Containers

```bash
# Build and start the API and Blockchain containers
docker-compose up -d api blockchain
```

### Key Environment Variables

* `NODE_ENV`: environment (`development` / `production`)
* `BLOCKCHAIN_RPC_URL`: RPC URL of the blockchain node (`http://blockchain:8545` for Hardhat, `http://blockchain-ganache:8545` for Ganache)
* `PORT`: API port (default `3000`)
* `CONTRACTS_FILE`: deployed contracts file (Ganache only)
* `PRIVATE_KEY`: private key for deployment/testing (Ganache only)

---

## 🔌 Main Endpoints

| Endpoint         | Method | Description                      |
| ---------------- | ------ | -------------------------------- |
| `/health`        | GET    | API health check                 |
| `/api/iot/info`  | GET    | Contract info & totalSubmissions |
| `/api/iot/data`  | POST   | Submit a single reading          |
| `/api/iot/batch` | POST   | Submit batch readings (max 50)   |

Example:

```bash
curl http://localhost:3000/api/iot/info
```

---

## 🛠 Hardhat Troubleshooting

Hardhat resets the blockchain on every restart, so you may see this error:

```
❌ Blockchain initialization failed: No contract deployed at this address
```

### Quick Fix

1. Deploy the contract on the Hardhat node:

```bash
docker-compose exec blockchain yarn deploy
```

2. Restart the API to load the newly deployed contract:

```bash
docker-compose restart api
```

3. Verify the API reads the contract correctly:

```bash
curl http://localhost:3000/api/iot/info
```

> Note: This issue only affects Hardhat. Ganache persists the data.

---

## 🧪 Testing

You can test submitting IoT data:

```bash
curl -X POST http://localhost:3000/api/iot/data \
  -H "Content-Type: application/json" \
  -d '{"sensorId":"sensor-001","data":{"temp":25}}'
```

---

## 📄 License

MIT
