#!/bin/bash

# Script to update all documentation to English
# Author: Auto-update
# Date: 2025-11-07

set -e

echo "================================================"
echo "  Updating documentation to English"
echo "================================================"
echo ""

# Update main README.md
echo "📝 Updating main README.md..."
cat > README.md << 'EOF'
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
EOF

# Update blockchain service README
echo "📝 Updating services/blockchain/README.md..."
cat > services/blockchain/README.md << 'EOF'
# Blockchain Service

Blockchain service based on Hardhat Network.

## Configuration

Hardhat Network configuration will be added in the next step.

## Contract Deployment

Deployment scripts will be configured to run automatically on container startup.

## Features

- Ethereum-compatible JSON-RPC endpoint
- Automatic contract deployment
- Data persistence via Docker volumes
- Lightweight (~80-120MB RAM)

## Endpoints

- RPC: `http://localhost:8545`
- Chain ID: 1337 (default)
EOF

# Update API service README
echo "📝 Updating services/api/README.md..."
cat > services/api/README.md << 'EOF'
# API Service

REST API service for blockchain interaction.

## Endpoints

### POST /api/iot/data
Submit IoT sensor data to the blockchain.

**Request body:**
```json
{
  "sensorId": "sensor_001",
  "data": "temperature:25.5",
  "timestamp": 1699372800
}
```

**Response:**
```json
{
  "success": true,
  "transactionHash": "0x...",
  "blockNumber": 123
}
```

## Testing

```bash
npm test
```

## Development

```bash
npm run dev
```
EOF

# Update ARCHITECTURE.md
echo "📝 Updating docs/ARCHITECTURE.md..."
cat > docs/ARCHITECTURE.md << 'EOF'
# Architecture

## Overview

Microservices architecture with separation of concerns (SOLID principles).

## Components

### 1. Blockchain Service
- Hardhat Network in standalone mode
- RPC exposed on port 8545
- Data persistence via Docker volume

### 2. API Service  
- Express.js server
- Ethers.js for blockchain interaction
- REST API for IoT data submission

### 3. Smart Contracts
- IoT data registry
- Event-based logging

## Communication Flow

```
IoT Device -> API Service -> Blockchain Service -> Smart Contract
```

## Data Flow

1. IoT device sends data via HTTP POST to API
2. API validates and formats data
3. API submits transaction to blockchain via JSON-RPC
4. Smart contract emits event with data
5. API returns transaction hash to device

## Scalability

Prepared for Kubernetes deployment with:
- Separate deployments for each service
- ConfigMaps for configuration
- PersistentVolumes for blockchain data
- Horizontal Pod Autoscaling for API service

## Resource Usage

- **Blockchain Service**: ~100MB RAM, minimal CPU
- **API Service**: ~50MB RAM, minimal CPU
- **Total**: <200MB RAM for both services

## Security Considerations

- Private network (not exposed to public internet)
- No real cryptocurrency involved
- Data validation at API level
- Rate limiting on API endpoints (future implementation)
EOF

# Update .env.example
echo "📝 Updating .env.example..."
cat > .env.example << 'EOF'
# Blockchain Configuration
BLOCKCHAIN_PORT=8545
BLOCKCHAIN_NETWORK_ID=1337
BLOCKCHAIN_CHAIN_ID=1337

# API Configuration
API_PORT=3000
API_HOST=0.0.0.0

# Blockchain Connection
BLOCKCHAIN_RPC_URL=http://blockchain:8545

# Development
NODE_ENV=development
LOG_LEVEL=info

# Smart Contract (will be set after deployment)
IOT_CONTRACT_ADDRESS=
EOF

# Update docker-compose.yml with English comments
echo "📝 Updating docker-compose.yml..."
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  # Hardhat blockchain service
  blockchain:
    build: ./services/blockchain
    container_name: blockchain-node
    ports:
      - "8545:8545"
    volumes:
      - ./data:/data
      - ./contracts:/contracts
    environment:
      - NODE_ENV=development
    networks:
      - blockchain-network
    restart: unless-stopped

  # REST API service
  api:
    build: ./services/api
    container_name: api-service
    ports:
      - "3000:3000"
    depends_on:
      - blockchain
    environment:
      - BLOCKCHAIN_RPC_URL=http://blockchain:8545
      - NODE_ENV=development
    volumes:
      - ./contracts:/contracts:ro
    networks:
      - blockchain-network
    restart: unless-stopped

networks:
  blockchain-network:
    driver: bridge

volumes:
  blockchain-data:
EOF

# Create CONTRIBUTING.md
echo "📝 Creating CONTRIBUTING.md..."
cat > CONTRIBUTING.md << 'EOF'
# Contributing Guidelines

Thank you for considering contributing to this project!

## Development Setup

1. Clone the repository
2. Copy `.env.example` to `.env`
3. Run `docker-compose up -d`

## Commit Message Convention

We use emojis for commit messages:

- 🎉 `:tada:` - Initial commit
- ✨ `:sparkles:` - New features
- 🐛 `:bug:` - Bug fixes
- 📝 `:memo:` - Documentation
- 🔧 `:wrench:` - Configuration files
- 🐳 `:whale:` - Docker-related changes
- ⚡ `:zap:` - Performance improvements
- 🚀 `:rocket:` - Deployment
- ♻️ `:recycle:` - Refactoring
- 🧪 `:test_tube:` - Tests

## Code Style

- Use English for all code, comments, and documentation
- Follow SOLID principles
- Write meaningful commit messages
- Add tests for new features

## Pull Request Process

1. Create a feature branch
2. Make your changes
3. Run tests
4. Submit PR with clear description
EOF

echo ""
echo "================================================"
echo "  ✅ All files updated to English!"
echo "================================================"
echo ""
echo "📋 Updated files:"
echo "  - README.md"
echo "  - services/blockchain/README.md"
echo "  - services/api/README.md"
echo "  - docs/ARCHITECTURE.md"
echo "  - .env.example"
echo "  - docker-compose.yml"
echo "  - CONTRIBUTING.md (new)"
echo ""
echo "🎯 Next steps:"
echo "  1. Review the changes"
echo "  2. Commit with: git add . && git commit -m '📝 Update documentation to English'"
echo "  3. Proceed with Hardhat implementation"
echo ""