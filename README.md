# Scalable Blockchain IoT

Lightweight private blockchain platform for storing IoT data for educational and testing purposes.

## 🏗️ Architecture

- **Blockchain Service**: Hardhat Network (Ethereum-compatible)
- **API Service**: Node.js + Express + Ethers.js
- **Smart Contracts**: Solidity

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
│   └── api/             # REST API service
├── contracts/           # Solidity smart contracts
├── data/               # Blockchain persistence (Docker volume)
└── docker-compose.yml  # Service orchestration
```

## 🔧 Requirements

- Docker >= 20.10
- Docker Compose >= 2.0
- 1GB available RAM

## 📚 Documentation

See `docs/` folder for more details.

## 🎯 Roadmap

- [x] Setup base architecture
- [ ] Implement IoT smart contract
- [ ] REST API for data submission
- [ ] Kubernetes deployment (optional)

## 📄 License

MIT
