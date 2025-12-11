# 🔄 SERVICE MANAGEMENT COMMANDS

This document provides a reference for managing the Docker containers that make up the Scalable Blockchain IoT framework. Use these commands for common operational tasks such as restarting, rebuilding, and viewing logs.

## 🚀 Quick Start (Full Setup Reference)

For a complete first-time setup, follow the steps below, selecting your preferred blockchain environment (Hardhat for development, Ganache for persistence).

### Option 1: Hardhat (Development - No Persistence)

```bash
# 1. Start services
docker-compose up -d

# 2. Deploy contract
docker-compose exec blockchain yarn deploy

# 3. Restart API to load contract address
docker-compose restart api
````

### Option 2: Ganache (Persistent Blockchain)

```bash
# 1. Start services
docker-compose up -d

# 2. Deploy contract to Ganache
docker-compose exec blockchain yarn deploy:ganache

# 3. Restart Ganache API to load contract address
docker-compose restart api-ganache
```

-----

## 🔁 Restart Services

Use these commands to restart specific components or the entire stack without losing volume data (except for Hardhat's in-memory state).

### Restart Specific Environments

| Target | Command | Notes |
| :--- | :--- | :--- |
| **Hardhat Stack** | `docker-compose restart blockchain api` | Restart the Hardhat node and the associated API. |
| **Ganache Stack** | `docker-compose restart blockchain-ganache api-ganache` | Restart the Ganache node and the associated API (data persists). |

### Full Stack Restart

```bash
docker-compose restart
```

-----

## 🛠️ Rebuild & Clean Up

Use these commands when you modify the source code or need to clear existing data.

### Rebuild After Code Changes

If you change the code in the API or smart contracts, you must rebuild and redeploy.

```bash
# 1. Stop and remove containers
docker-compose down

# 2. Rebuild images and start services
docker-compose up -d --build
```

### Clear All Data and Start Fresh (🚨 Caution\!)

This command removes all containers, networks, and **volumes**, including persistent Ganache data.

```bash
# Stop and remove containers/volumes
docker-compose down -v

# Manually clear local Ganache data (if mounted)
rm -rf data/ganache/*

# Rebuild images and start services
docker-compose up -d --build
```

-----

## 👁️ View Logs

Use the following commands to monitor the output and debug the running services.

| Environment | Service | Command |
| :--- | :--- | :--- |
| **Hardhat** | Blockchain Node | `docker logs -f blockchain-hardhat` |
| **Hardhat** | API Microservice | `docker logs -f iot-api` |
| **Ganache** | Persistent Node | `docker logs -f blockchain-ganache` |
| **Ganache** | Persistent API | `docker logs -f iot-api-ganache` |

**Tip:** Use `Ctrl+C` to stop tailing the logs.
