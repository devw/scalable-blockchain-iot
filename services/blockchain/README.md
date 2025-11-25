# 🔗 Blockchain Service

Two blockchain networks for IoT data registry:
- **blockchain-hardhat** → Port 8545 (ephemeral, resets on restart)
- **blockchain-ganache** → Port 8546 (persistent state)

## 🚀 Quick Start

```bash
# Start containers
docker-compose up -d blockchain-hardhat blockchain-ganache

# Deploy contracts
docker exec blockchain-hardhat yarn deploy          # Hardhat
docker exec blockchain-hardhat yarn deploy:ganache  # Ganache
```

📁 Contract addresses saved to `../../data/deployed-contracts*.json`

## ⚠️ Important: Hardhat Reset Behavior

Hardhat **does not persist state** between restarts. After restart:
```bash
docker exec blockchain-hardhat yarn deploy  # Must redeploy!
```

## 📸 Snapshots (Ganache Only)

```bash
# Create snapshot
../../scripts/snapshot-helper.sh create "my-snapshot"

# Restore snapshot
../../scripts/snapshot-helper.sh restore <snapshot_id>
```

📂 Stored in `../../data/snapshots/`

## 🔧 Container Management

```bash
# Health check
docker ps --filter "name=blockchain"

# Restart (⚠️ Hardhat loses state)
docker-compose restart blockchain-hardhat
docker-compose restart blockchain-ganache

# View logs
docker logs -f blockchain-hardhat
```

## ⚙️ Configuration

**Hardhat** (`hardhat.config.js`)
- Chain ID: 31337
- 20 accounts × 10000 ETH

**Ganache** (`docker-compose.yml`)
- Chain ID: 1337
- Persistent: `../../data/ganache/`

## 🐛 Troubleshooting

```bash
# Port conflict
lsof -i :8545  # or :8546
docker stop blockchain-hardhat blockchain-ganache

# Force recreate
docker-compose rm -f blockchain-hardhat blockchain-ganache
docker-compose up -d blockchain-hardhat blockchain-ganache

# Test connectivity
curl -X POST http://localhost:8545 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'
```

## 📚 Related Docs

- [📖 Main README](../../README.md)
- [🔌 API Service](../api/README.md)
- [🏗️ Architecture](../../docs/ARCHITECTURE.md)