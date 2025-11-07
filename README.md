# Scalable Blockchain IoT

Piattaforma blockchain privata leggera per la memorizzazione di dati IoT a scopo didattico e di test.

## 🏗️ Architettura

- **Blockchain Service**: Hardhat Network (Ethereum-compatible)
- **API Service**: Node.js + Express + Ethers.js
- **Smart Contracts**: Solidity

## 🚀 Quick Start

```bash
# Copia il file di configurazione
cp .env.example .env

# Avvia i servizi
docker-compose up -d

# Verifica stato
docker-compose ps
```

## 📁 Struttura Progetto

```
scalable-blockchain-iot/
├── services/
│   ├── blockchain/       # Servizio blockchain Hardhat
│   └── api/             # Servizio API REST
├── contracts/           # Smart contracts Solidity
├── data/               # Persistenza blockchain (volume Docker)
└── docker-compose.yml  # Orchestrazione servizi
```

## 🔧 Requisiti

- Docker >= 20.10
- Docker Compose >= 2.0
- 1GB RAM disponibile

## 📚 Documentazione

Vedi la cartella `docs/` per maggiori dettagli.

## 🎯 Roadmap

- [x] Setup architettura base
- [ ] Implementazione smart contract IoT
- [ ] API REST per submission dati
- [ ] Deploy su Kubernetes (opzionale)

## 📄 Licenza

MIT
