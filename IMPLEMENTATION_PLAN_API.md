# API IoT Endpoints Implementation Plan

## 🎯 Goal
Add RESTful API endpoints to store and retrieve IoT sensor data on blockchain.

## 📋 Endpoints to Implement

### 1. POST /api/data
Store new IoT sensor reading on blockchain.

**Request Body:**
```json
{
  "sensorId": "TEMP_001",
  "value": 23.5,
  "unit": "celsius",
  "location": "Room A",
  "timestamp": 1700000000
}
```

**Response:**
```json
{
  "success": true,
  "transactionHash": "0x...",
  "dataId": "0x...",
  "blockNumber": 42
}
```

### 2. GET /api/data/:id
Retrieve specific data entry by ID.

### 3. GET /api/data
List all data entries (paginated).

**Query Params:**
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 10)
- `sensorId`: Filter by sensor ID (optional)

### 4. GET /api/stats
Get blockchain statistics.

**Response:**
```json
{
  "totalEntries": 150,
  "currentBlock": 42,
  "contractAddress": "0x...",
  "lastEntry": { ... }
}
```

## 🏗️ Architecture
```
Client Request
    ↓
Express Router (routes/data.routes.js)
    ↓
Validator Middleware (validators/data.validator.js)
    ↓
Controller (controllers/data.controller.js)
    ↓
Blockchain Service (services/blockchain.service.js)
    ↓
Smart Contract (IoTDataRegistry)
    ↓
Response to Client
```

## 📁 Files to Create/Modify
```
services/api/src/
├── routes/
│   └── data.routes.js          # Route definitions
├── controllers/
│   └── data.controller.js      # Business logic
├── services/
│   └── blockchain.service.js   # Contract interaction
├── validators/
│   └── data.validator.js       # Input validation
├── middlewares/
│   ├── errorHandler.js         # Global error handler
│   └── asyncHandler.js         # Async wrapper
└── app.js                      # Update with new routes
```

## 🔧 Dependencies Needed

- `joi` or `zod` - Input validation
- `ethers` - Blockchain interaction (already have)
- `dotenv` - Environment variables (already have)

## ✅ Implementation Steps

1. [x] Create implementation plan
2. [ ] Setup project structure
3. [ ] Add validation middleware
4. [ ] Create blockchain service
5. [ ] Implement POST /api/data
6. [ ] Implement GET /api/data/:id
7. [ ] Implement GET /api/data (list)
8. [ ] Implement GET /api/stats
9. [ ] Add error handling
10. [ ] Test all endpoints
11. [ ] Update documentation

## 🧪 Testing Strategy

Manual testing with curl:
```bash
# Store data
curl -X POST http://localhost:3000/api/data \
  -H "Content-Type: application/json" \
  -d '{"sensorId":"TEMP_001","value":23.5}'

# Get data
curl http://localhost:3000/api/data/0x...
curl http://localhost:3000/api/data?page=1&limit=10
curl http://localhost:3000/api/stats
```

## 📊 Success Criteria

- ✅ Can store IoT data on blockchain via API
- ✅ Can retrieve data by ID
- ✅ Can list all data with pagination
- ✅ Proper error handling for invalid inputs
- ✅ Response times < 2 seconds for writes
- ✅ Response times < 500ms for reads

## 🚀 Ready for Implementation
