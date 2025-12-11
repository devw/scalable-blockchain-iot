# 🔧 TROUBLESHOOTING GUIDE

This guide addresses common issues encountered when deploying, running, or interacting with the Scalable Blockchain IoT framework using Docker Compose.

---

## 🛑 API Won't Start (Connection or Contract Missing)

### Problem Description

The API service (Hardhat on port 3000 or Ganache on port 3001) starts and then immediately exits, or logs an error indicating it cannot find the deployed contract address or connect to the blockchain node.

### Possible Causes

1.  The Smart Contract has not been deployed to the target blockchain network.
2.  The deployed contract address hasn't been successfully written to the API environment file/variable.
3.  The associated blockchain node is not running or is still initializing.

### Solution Steps

1.  **Check Contract Deployment Status:**
    * **Hardhat:** Check if the contract artifact file exists in the container:
        ```bash
        docker exec blockchain-hardhat cat /data/deployed-contracts.json
        ```
    * **Ganache:** Check if the Ganache data volume contains chain info:
        ```bash
        docker exec blockchain-ganache ls /ganache_data
        ```

2.  **Redeploy the Contract:**
    * If the contract is missing, deploy it to the respective network:
        ```bash
        # For Hardhat (Development)
        docker-compose exec blockchain yarn deploy

        # For Ganache (Persistence)
        docker-compose exec blockchain yarn deploy:ganache
        ```

3.  **Restart the API Service:**
    * After deployment, always restart the API container to ensure it loads the new contract address:
        ```bash
        docker-compose restart api  # Hardhat API
        docker-compose restart api-ganache # Ganache API
        ```

---

## 💾 Persistence Not Working (Ganache)

### Problem Description

After submitting data to the Ganache stack (port 3001) and then restarting the containers, the `totalSubmissions` count resets to zero, indicating data was not saved to disk.

### Possible Causes

1.  The Docker volume mount for the Ganache data directory is incorrect or failing.
2.  The directory where Ganache saves its state (`/ganache_data` inside the container) is not correctly mapped to the host machine.

### Solution Steps

1.  **Verify Volume Mount:** Inspect the Ganache container to ensure the volume is correctly mapped to the host directory (e.g., `./data/ganache` on the host).
    ```bash
    docker inspect blockchain-ganache | grep ganache_data
    ```

2.  **Check Ganache Data Directory:** Ensure files (like the chain data) are present inside the container's persistence path.
    ```bash
    docker exec blockchain-ganache ls -la /ganache_data
    ```

3.  **Ensure Correct Deployment:** Confirm you are using the persistence-enabled deployment command:
    ```bash
    docker-compose exec blockchain yarn deploy:ganache
    ```

---

## 🗑️ Clear All Data and Start Fresh

If you encounter irrecoverable state errors, especially with Hardhat snapshots or Ganache data volumes, you can perform a full reset. **🚨 Warning:** This will permanently delete all stored blockchain data.

```bash
# 1. Stop and remove containers, networks, and volumes (-v flag)
docker-compose down -v

# 2. Manually remove any lingering local persistence data on the host
rm -rf data/ganache/*

# 3. Rebuild (if needed) and start services
docker-compose up -d --build