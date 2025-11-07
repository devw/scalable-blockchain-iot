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
