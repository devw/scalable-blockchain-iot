# Blockchain Service - Hardhat with Snapshot Persistence

Ethereum blockchain service powered by Hardhat with snapshot-based state management for the IoT Data Registry demo.

## 🎯 Features

- ✅ **Hardhat Network**: Fast, local Ethereum development network
- ✅ **Snapshot Management**: Export/import blockchain state
- ✅ **Auto-deployment**: Contracts deployed automatically on startup
- ✅ **ARM64 Native**: Works perfectly on Apple Silicon (M1/M2/M3)
- ✅ **Docker Ready**: Fully containerized setup
- ✅ **Hot Reload**: Contract changes reflected immediately

## 🏗️ Architecture

```
services/blockchain/
├── contracts/          # Solidity smart contracts
├── scripts/           # Deployment and helper scripts
│   ├── deploy.js      # Contract deployment
│   └── snapshot-helper.sh
├── utils/             # Utility modules
│   └── snapshot.js    # Snapshot management
├── hardhat.config.js  # Hardhat configuration
├── Dockerfile         # Container definition
└── package.json       # Dependencies and scripts
```

## 🚀 Quick Start

### Start the Blockchain

```bash
# From project root
docker-compose up blockchain -d

# Check logs
docker-compose logs -f blockchain
```

### Deploy Contracts

```bash
# Deploy to running blockchain
docker-compose exec blockchain yarn deploy

# Or redeploy after changes
docker-compose exec blockchain yarn compile
docker-compose exec blockchain yarn deploy
```

## 📸 Snapshot Management

### Create Snapshot

Capture current blockchain state (accounts, deployments, balances):

```bash
# Using helper script (recommended)
./scripts/snapshot-helper.sh export

# Or directly in container
docker-compose exec blockchain yarn snapshot:export
```

### Restore Snapshot

Restore deployment references from saved snapshot:

```bash
# Using helper script
./scripts/snapshot-helper.sh import

# Or directly in container
docker-compose exec blockchain yarn snapshot:import
```

### List Snapshots

View all available snapshots:

```bash
./scripts/snapshot-helper.sh list
```

### Clean Snapshots

Remove all snapshots:

```bash
./scripts/snapshot-helper.sh clean
```

## 📋 Available Commands

### Inside Container

```bash
# Compile contracts
yarn compile

# Deploy contracts
yarn deploy

# Run tests
yarn test

# Snapshot management
yarn snapshot:export
yarn snapshot:import
yarn snapshot:list
```

### From Host

```bash
# Using helper script
./scripts/snapshot-helper.sh [export|import|list|clean]

# Using docker-compose
docker-compose exec blockchain [command]
```

## 🔧 Configuration

### Environment Variables

```bash
# In docker-compose.yml or .env
SNAPSHOT_DIR=/data/snapshots    # Snapshot storage location
RPC_URL=http://localhost:8545   # Blockchain RPC endpoint
```

### Network Configuration

```javascript
// hardhat.config.js
networks: {
  hardhat: {
    chainId: 1337,      // Local network ID
    mining: {
      auto: true,        // Auto-mine blocks
      interval: 0        // Instant mining
    }
  }
}
```

## 💾 Persistence

### What is Persisted?

Snapshots capture:
- ✅ Deployed contract addresses
- ✅ Deployment block numbers
- ✅ Account balances
- ✅ Network configuration
- ✅ Contract bytecode

### What is NOT Persisted?

⚠️ **Important**: Hardhat resets on each restart. Snapshots provide:
- Reference for redeployment
- Documentation of previous state
- Configuration backup

For true persistence, the contract must be redeployed after container restart.

## 🔍 Workflow Example

```bash
# 1. Start blockchain
docker-compose up blockchain -d

# 2. Deploy contracts
docker-compose exec blockchain yarn deploy

# 3. Use the application
# (API interacts with contracts, stores IoT data)

# 4. Create snapshot before stopping
./scripts/snapshot-helper.sh export

# 5. Stop container
docker-compose down

# 6. Later: restart and restore
docker-compose up blockchain -d
docker-compose exec blockchain yarn deploy  # Redeploy
./scripts/snapshot-helper.sh import         # Reference previous state
```

## 🐛 Troubleshooting

### Blockchain not starting

```bash
# Check logs
docker-compose logs blockchain

# Rebuild container
docker-compose build blockchain
docker-compose up blockchain -d
```

### Port 8545 already in use

```bash
# Find process using port
lsof -i :8545

# Stop other blockchain services
docker-compose down
```

### Snapshot not found

```bash
# List available snapshots
./scripts/snapshot-helper.sh list

# Check snapshot directory
ls -la ./data/snapshots/
```

## 📚 Resources

- [Hardhat Documentation](https://hardhat.org/docs)
- [Ethers.js Documentation](https://docs.ethers.org/)
- [Solidity Documentation](https://docs.soliditylang.org/)

## 🤝 Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for development guidelines.

## 📝 License

MIT