# 📝 API USAGE EXAMPLES

This document provides command-line examples for interacting with the Blockchain IoT API using cURL. Note the distinct ports used for each environment:

* **Hardhat (Development):** Port `3000`
* **Ganache (Persistent):** Port `3001`

---

## 💾 Submit IoT Data

### Single Reading Submission (`POST /api/iot/data`)

Submit a single sensor reading to the blockchain via the API gateway.

**Hardhat (Development):**
```bash
curl -X POST http://localhost:3000/api/iot/data \
  -H "Content-Type: application/json" \
  -d '{"sensorId":"sensor-001","data":{"temp":25.3, "humidity": 65}}'
````

**Ganache (Persistent):**

```bash
curl -X POST http://localhost:3001/api/iot/data \
  -H "Content-Type: application/json" \
  -d '{"sensorId":"sensor-001","data":{"temp":25.3, "humidity": 65}}'
```

### Batch Data Submission (`POST /api/iot/batch`)

Submit multiple readings in a single transaction to improve efficiency. The contract typically enforces a maximum number of readings per batch (e.g., max 50).

**Example (Hardhat):**

```bash
curl -X POST http://localhost:3000/api/iot/batch \
  -H "Content-Type: application/json" \
  -d '{
    "readings": [
      {"sensorId":"sensor-001","data":{"temp":22.1}},
      {"sensorId":"sensor-002","data":{"temp":24.7}},
      {"sensorId":"sensor-003","data":{"temp":23.0}}
    ]
  }'
```

-----

## 🔎 Check Contract Info (`GET /api/iot/info`)

Retrieve basic metadata and runtime statistics from the deployed smart contract, including the total number of submissions made so far.

**Hardhat (Development):**

```bash
curl http://localhost:3000/api/iot/info
```

**Ganache (Persistent):**

```bash
curl http://localhost:3001/api/iot/info
```

-----

## 📊 Get Blockchain Statistics (`GET /api/iot/stats`)

*(Note: The full functionality and response format for this endpoint are detailed in [API\_REFERENCE.MD](https://www.google.com/search?q=./API_REFERENCE.MD).)*

```bash
# Example for Hardhat
curl http://localhost:3000/api/iot/stats
```
