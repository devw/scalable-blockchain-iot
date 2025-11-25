# 📊 Blockscout Dashboard Usage Guide

## 🎯 Overview

This guide shows you how to submit IoT sensor data to the blockchain and view it using Blockscout explorer.

## ✅ Prerequisites

Before starting, make sure:
- 🐳 All Docker containers are running: `docker-compose up -d`
- 🌐 API is available at `http://localhost:3001`
- 🔍 Blockscout is available at `http://localhost:4000`

Check container status:
```bash
docker ps
```

You should see these containers running:
- `sbiot-api-ganache-1`
- `sbiot-blockchain-ganache-1`
- `sbiot-blockscout-1`

## 📤 Submitting Sensor Data

### Basic Example

Send sensor data using `curl`:

```bash
curl -X POST http://localhost:3001/api/iot/data \
  -H "Content-Type: application/json" \
  -d '{"sensorId":"sensor-001","data":{"temp":25}}'
```

### ✨ Successful Response

You'll receive a response like this:

```json
{
  "success": true,
  "message": "Data submitted successfully",
  "data": {
    "sensorId": "sensor-001",
    "transactionHash": "0x98e296303a2b410539a07817bcc30fc04d33eaf63a562d391d1f5e1e0f8905fc",
    "blockNumber": 14,
    "gasUsed": "31991",
    "timestamp": 1764091710
  }
}
```

**Important:** Save the `transactionHash` - you'll need it to view the transaction on Blockscout! 📝

### 📊 More Examples

**Temperature sensor:**
```bash
curl -X POST http://localhost:3001/api/iot/data \
  -H "Content-Type: application/json" \
  -d '{"sensorId":"temp-sensor-01","data":{"temp":22.5,"humidity":65}}'
```

**Motion sensor:**
```bash
curl -X POST http://localhost:3001/api/iot/data \
  -H "Content-Type: application/json" \
  -d '{"sensorId":"motion-001","data":{"motion":true,"timestamp":1234567890}}'
```

**Air quality sensor:**
```bash
curl -X POST http://localhost:3001/api/iot/data \
  -H "Content-Type: application/json" \
  -d '{"sensorId":"air-quality-01","data":{"pm25":45,"pm10":78,"co2":650}}'
```

## 🔍 Viewing Data on Blockscout

### Step 1: Open Blockscout

Navigate to the Blockscout homepage:
```
http://localhost:4000
```

### Step 2: Search for Your Transaction

You have two options:

**Option A - Direct Link** 🔗  
Use the transaction hash from the API response:
```
http://localhost:4000/tx/0x98e296303a2b410539a07817bcc30fc04d33eaf63a562d391d1f5e1e0f8905fc
```

**Option B - Search** 🔎  
1. Go to `http://localhost:4000`
2. Paste your transaction hash in the search bar
3. Press Enter

### Step 3: View Transaction Details

On the transaction page, you'll see:

- ⏱️ **Timestamp** - When the transaction was created
- 🧱 **Block Number** - Which block contains this transaction
- ⛽ **Gas Used** - Transaction cost
- ✅ **Status** - Success or Failed

### Step 4: View Decoded Logs 📋

Click on the **"Logs"** tab to see your sensor data decoded:

```
Event: IoTDataReceived
├── sender: 0x1ca2c39474414726a92c3ed9277e54d6af75eff4
├── sensorId: sensor-001
├── data: {"temp":25}
├── timestamp: 1764091710
└── blockNumber: 14
```

## 🎨 Understanding the Contract

### Contract Address
```
0xcB9E2EC7bF87bFb9f9fe7e4e947d4425407e6a8F
```

You can view the contract details at:
```
http://localhost:4000/address/0xcB9E2EC7bF87bFb9f9fe7e4e947d4425407e6a8F
```

### Available Tabs:

- **📜 Transactions** - All transactions sent to this contract
- **📊 Logs** - All events emitted by the contract
- **💻 Code** - Verified smart contract source code
- **📖 Read Contract** - Query contract state (view functions)
- **✍️ Write Contract** - Interact with contract (write functions)

## 🔧 Common Issues

### ❌ "Failed to decode log data"

**Problem:** The smart contract is not verified on Blockscout.

**Solution:** 
1. Go to the contract page
2. Click **"Verify & Publish"**
3. Use these settings:
   - Compiler: `v0.8.20`
   - Optimization: `Yes` with `200` runs
   - Paste the contract source code from `contracts/IoTDataRegistry.sol`

### ❌ API Returns Error

**Problem:** Container might not be running.

**Solution:**
```bash
docker-compose restart api-ganache
docker logs sbiot-api-ganache-1
```

### ❌ Blockscout Not Loading

**Problem:** Container might need restart.

**Solution:**
```bash
docker-compose restart blockscout
# Wait 30 seconds for initialization
```

## 📚 Additional Resources

- **Smart Contract:** `contracts/IoTDataRegistry.sol`
- **Architecture:** `docs/ARCHITECTURE.md`
- **API Documentation:** `services/api/README.md`
- **Blockchain Setup:** `services/blockchain/README.md`

## 💡 Tips

- 🔄 Refresh Blockscout page if data doesn't appear immediately
- 📝 Keep transaction hashes for future reference
- 🎯 Use descriptive sensor IDs to organize your data
- ⚡ Check gas usage to optimize your data submissions

---

**Happy exploring! 🚀**