# Scalable Blockchain IoT

Lightweight blockchain platform for storing IoT sensor data with persistence support.

## 🏗️ Architecture

* **Blockchain**: Hardhat (dev/testing) + Ganache (persistent storage)
* **API**: Node.js + Express + Ethers.js
* **Smart Contracts**: Solidity

---

## 🚀 Quick Start

### Option 1: Hardhat (Development - No Persistence)

```bash
# Start services
docker-compose up -d

# Deploy contract
docker-compose exec blockchain yarn deploy

# Restart API
docker-compose restart api

# Test
curl http://localhost:3000/api/iot/info
```

### Option 2: Ganache (Persistent Blockchain)

```bash
# Start services
docker-compose up -d

# Deploy contract to Ganache
docker-compose exec blockchain yarn deploy:ganache

# Restart Ganache API
docker-compose restart api-ganache

# Test
curl http://localhost:3001/api/iot/info
```

---

## 🔌 Services & Ports

| Service | Blockchain | API Port | RPC Port | Persistence |
|---------|-----------|----------|----------|-------------|
| **Hardhat** | Development | 3000 | 8545 | ❌ Resets on restart |
| **Ganache** | Production | 3001 | 8546 | ✅ Disk-based |

---

## 📝 API Usage

### Submit IoT Data

**Hardhat:**
```bash
curl -X POST http://localhost:3000/api/iot/data \
  -H "Content-Type: application/json" \
  -d '{"sensorId":"sensor-001","data":{"temp":25}}'
```

**Ganache:**
```bash
curl -X POST http://localhost:3001/api/iot/data \
  -H "Content-Type: application/json" \
  -d '{"sensorId":"sensor-001","data":{"temp":25}}'
```

### Check Contract Info

```bash
# Hardhat
curl http://localhost:3000/api/iot/info

# Ganache
curl http://localhost:3001/api/iot/info
```

### Submit Batch Data

```bash
curl -X POST http://localhost:3000/api/iot/batch \
  -H "Content-Type: application/json" \
  -d '{
    "readings": [
      {"sensorId":"sensor-001","data":{"temp":22.1}},
      {"sensorId":"sensor-002","data":{"temp":24.7}}
    ]
  }'
```

---

## 🧪 Testing Ganache Persistence

```bash
# 1. Deploy and submit data
docker-compose exec blockchain yarn deploy:ganache
curl -X POST http://localhost:3001/api/iot/data \
  -H "Content-Type: application/json" \
  -d '{"sensorId":"test","data":{"temp":30}}'

# 2. Check totalSubmissions
curl http://localhost:3001/api/iot/info
# Should show: "totalSubmissions": "1"

# 3. Restart Ganache
docker-compose restart blockchain-ganache api-ganache

# 4. Verify data persisted
curl http://localhost:3001/api/iot/info
# Should STILL show: "totalSubmissions": "1" ✅
```

---

## 🔄 Service Management

### Restart Services

```bash
# Restart Hardhat
docker-compose restart blockchain api

# Restart Ganache
docker-compose restart blockchain-ganache api-ganache

# Restart everything
docker-compose restart
```

### Rebuild After Code Changes

```bash
docker-compose down
docker-compose up -d --build
```

### View Logs

```bash
# Hardhat
docker logs -f blockchain-hardhat
docker logs -f iot-api

# Ganache
docker logs -f blockchain-ganache
docker logs -f iot-api-ganache
```

---

## 💾 Blockchain Snapshots (Hardhat Only)

Hardhat resets on restart. Use snapshots for reference:

```bash
# Export snapshot (saves current state)
docker-compose exec blockchain yarn snapshot:export

# Import snapshot (restore reference data)
docker-compose exec blockchain yarn snapshot:import

# List snapshots
docker-compose exec blockchain yarn snapshot:list
```

**Note:** Snapshots are reference-only. For true persistence, use Ganache.

---

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/iot/info` | GET | Contract info & totalSubmissions |
| `/api/iot/stats` | GET | Blockchain statistics |
| `/api/iot/data` | POST | Submit single reading |
| `/api/iot/batch` | POST | Submit batch readings (max 50) |

---

## 🔧 Troubleshooting

### API won't start

```bash
# Check if contract is deployed
docker exec blockchain-hardhat cat /data/deployed-contracts.json
docker exec blockchain-ganache ls /ganache_data

# Redeploy if missing
docker-compose exec blockchain yarn deploy        # Hardhat
docker-compose exec blockchain yarn deploy:ganache  # Ganache
```

### Persistence not working (Ganache)

```bash
# Check Ganache data directory
docker exec blockchain-ganache ls -la /ganache_data

# Verify volume mount
docker inspect blockchain-ganache | grep ganache_data
```

### Clear all data and start fresh

```bash
docker-compose down -v
rm -rf data/ganache/*
docker-compose up -d --build
```

---

## 🎯 Use Cases

- **Hardhat**: Fast development, testing, contract debugging
- **Ganache**: Production-like environment with data persistence

---

## 📄 License

MIT