# 🌐 Public Exposure Guide with Cloudflare Tunnel

## 🎯 Overview

This guide shows you how to expose your local IoT blockchain services (API and Blockscout) to the internet using Cloudflare Tunnel, allowing external users to interact with your system.

## 📋 Prerequisites

- ✅ All Docker containers running (`docker-compose up -d`)
- ✅ Cloudflare account (free) - https://dash.cloudflare.com/sign-up
- ✅ Homebrew installed (macOS/Linux)

## 🚀 Setup Cloudflare Tunnel

### Step 1: Install cloudflared

```bash
brew install cloudflared
```

Verify installation:
```bash
cloudflared --version
```

### Step 2: Authenticate with Cloudflare

```bash
cloudflared tunnel login
```

This will:
1. Open your browser
2. Ask you to login to Cloudflare
3. Authorize cloudflared
4. Save credentials to `~/.cloudflared/cert.pem`

You should see a success message in the terminal.

## 🔧 Running Tunnels in Background

### Start API Tunnel (Port 3001)

```bash
nohup cloudflared tunnel --url http://localhost:3001 > ~/cloudflared-api.log 2>&1 &
```

### Start Blockscout Tunnel (Port 4000)

```bash
nohup cloudflared tunnel --url http://localhost:4000 > ~/cloudflared-blockscout.log 2>&1 &
```

### 📝 Get Public URLs

Wait 5-10 seconds for tunnels to initialize, then:

```bash
# Get API URL
tail -30 ~/cloudflared-api.log | grep trycloudflare

# Get Blockscout URL
tail -30 ~/cloudflared-blockscout.log | grep trycloudflare
```

You'll see URLs like:
```
https://random-words-1234.trycloudflare.com  (API)
https://another-random-5678.trycloudflare.com  (Blockscout)
```

**⚠️ Important:** These URLs change every time you restart the tunnels. Save them and share with external users.

## 📤 Sharing with External Users

### For API Access

Share the API URL with users who need to send IoT data:

**Example command for external users:**
```bash
curl -X POST https://random-words-1234.trycloudflare.com/api/iot/data \
  -H "Content-Type: application/json" \
  -d '{"sensorId":"sensor-001","data":{"temp":25}}'
```

### For Blockscout Dashboard

Share the Blockscout URL for viewing transactions:

```
https://another-random-5678.trycloudflare.com
```

Users can:
- 🔍 Search transactions by hash
- 📊 View decoded logs and events
- 💻 Explore the smart contract
- 📈 Monitor blockchain activity

## 🛠️ Managing Tunnels

### Check if Tunnels are Running

```bash
ps aux | grep cloudflared
```

You should see 2 processes running.

### View Live Logs

**API Tunnel:**
```bash
tail -f ~/cloudflared-api.log
```

**Blockscout Tunnel:**
```bash
tail -f ~/cloudflared-blockscout.log
```

Press `Ctrl+C` to stop viewing logs.

### Stop All Tunnels

```bash
pkill cloudflared
```

### Restart Tunnels

```bash
# Stop existing tunnels
pkill cloudflared

# Wait 2 seconds
sleep 2

# Start new tunnels
nohup cloudflared tunnel --url http://localhost:3001 > ~/cloudflared-api.log 2>&1 &
nohup cloudflared tunnel --url http://localhost:4000 > ~/cloudflared-blockscout.log 2>&1 &

# Get new URLs after 5-10 seconds
tail -30 ~/cloudflared-api.log | grep trycloudflare
tail -30 ~/cloudflared-blockscout.log | grep trycloudflare
```

## 📊 Complete Workflow Example

### 1. Start Your Services

```bash
# Start Docker containers
docker-compose up -d

# Wait for services to be ready (~30 seconds)
docker ps
```

### 2. Start Tunnels

```bash
nohup cloudflared tunnel --url http://localhost:3001 > ~/cloudflared-api.log 2>&1 &
nohup cloudflared tunnel --url http://localhost:4000 > ~/cloudflared-blockscout.log 2>&1 &
```

### 3. Get Public URLs

```bash
# Wait 10 seconds
sleep 10

# Extract URLs
echo "=== API URL ==="
tail -30 ~/cloudflared-api.log | grep trycloudflare

echo "=== Blockscout URL ==="
tail -30 ~/cloudflared-blockscout.log | grep trycloudflare
```

### 4. Share with External Users

Send them:
- 📤 API URL for submitting data
- 🔍 Blockscout URL for viewing transactions
- 📚 Link to `docs/BLOCKSCOUT_USAGE.md` for usage instructions

### 5. External User Sends Data

```bash
curl -X POST https://your-api-url.trycloudflare.com/api/iot/data \
  -H "Content-Type: application/json" \
  -d '{"sensorId":"remote-sensor-01","data":{"temp":28,"humidity":70}}'
```

Response:
```json
{
  "success": true,
  "transactionHash": "0x...",
  "blockNumber": 42
}
```

### 6. View on Blockscout

Navigate to:
```
https://your-blockscout-url.trycloudflare.com/tx/0x...
```

## 🔒 Security Considerations

### ⚠️ Important Notes

1. **Quick Tunnels are Public** - Anyone with the URL can access your services
2. **URLs Change on Restart** - Not suitable for permanent deployments
3. **No Authentication** - Consider adding API keys for production use
4. **Rate Limiting** - Cloudflare may throttle high traffic

### 🛡️ Best Practices

- 🔐 Use tunnels only for testing/demos with trusted users
- ⏱️ Stop tunnels when not needed: `pkill cloudflared`
- 📝 Monitor logs regularly for suspicious activity
- 🚫 Don't share URLs publicly on the internet
- ✅ For production, use Cloudflare's named tunnels with proper domains

## ❓ Troubleshooting

### Tunnel Not Starting

**Problem:** `cloudflared` command fails immediately

**Solution:**
```bash
# Check if cloudflared is already running
pkill cloudflared

# Try again
nohup cloudflared tunnel --url http://localhost:3001 > ~/cloudflared-api.log 2>&1 &
```

### Can't Find Public URL

**Problem:** No trycloudflare URL in logs

**Solution:**
```bash
# Check full log file
cat ~/cloudflared-api.log

# Look for any errors
grep -i error ~/cloudflared-api.log
```

### External Users Get Connection Error

**Problem:** Users can't access the URL

**Solutions:**
1. Check if Docker containers are running: `docker ps`
2. Verify tunnels are active: `ps aux | grep cloudflared`
3. Check tunnel logs for errors
4. Restart tunnels: `pkill cloudflared` then start again

### Tunnel Stops Working After a While

**Problem:** URL stops responding after hours/days

**Solution:**
Cloudflare quick tunnels may disconnect. Restart them:
```bash
pkill cloudflared
# Wait 5 seconds
nohup cloudflared tunnel --url http://localhost:3001 > ~/cloudflared-api.log 2>&1 &
nohup cloudflared tunnel --url http://localhost:4000 > ~/cloudflared-blockscout.log 2>&1 &
```

## 🎯 Alternative: Use Named Tunnels (Advanced)

For permanent, production-ready tunnels with custom domains, see Cloudflare's named tunnels documentation:
https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/

## 📚 Related Documentation

- **Usage Guide:** `docs/BLOCKSCOUT_USAGE.md` - How to submit data and view on Blockscout
- **Architecture:** `docs/ARCHITECTURE.md` - System design and components
- **API Docs:** `services/api/README.md` - API endpoints and configuration

## 💡 Quick Reference

```bash
# Start tunnels
nohup cloudflared tunnel --url http://localhost:3001 > ~/cloudflared-api.log 2>&1 &
nohup cloudflared tunnel --url http://localhost:4000 > ~/cloudflared-blockscout.log 2>&1 &

# Get URLs (wait 10 seconds first)
tail -30 ~/cloudflared-api.log | grep trycloudflare
tail -30 ~/cloudflared-blockscout.log | grep trycloudflare

# Stop tunnels
pkill cloudflared

# View logs
tail -f ~/cloudflared-api.log
tail -f ~/cloudflared-blockscout.log
```

---

**Happy sharing! 🚀**