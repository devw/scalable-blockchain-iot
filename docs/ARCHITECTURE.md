# Architettura

## Overview

Architettura a microservizi con separazione delle responsabilità (SOLID principles).

## Componenti

### 1. Blockchain Service
- Hardhat Network in modalità standalone
- Esposizione RPC su porta 8545
- Persistenza dati tramite volume Docker

### 2. API Service  
- Express.js server
- Ethers.js per interazione blockchain
- REST API per submission dati IoT

### 3. Smart Contracts
- Registry dati IoT
- Event-based logging

## Comunicazione

```
IoT Device -> API Service -> Blockchain Service -> Smart Contract
```

## Scalabilità

Preparato per deploy su Kubernetes con:
- Deployment separati per ogni servizio
- ConfigMaps per configurazione
- PersistentVolumes per dati blockchain
