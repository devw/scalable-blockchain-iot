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
