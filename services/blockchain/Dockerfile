# Base image - using Alpine for minimal size
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Install dependencies for native modules
RUN apk add --no-cache \
    python3 \
    make \
    g++ \
    git

# Copy package files
COPY package*.json ./

# Install npm dependencies
RUN npm ci --only=production && \
    npm cache clean --force

# Copy Hardhat configuration
COPY hardhat.config.js ./

# Copy scripts directory
COPY scripts ./scripts

# Create data directory for blockchain persistence
RUN mkdir -p /data

# Expose JSON-RPC port
EXPOSE 8545

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD node -e "require('http').get('http://localhost:8545', (res) => { process.exit(res.statusCode === 200 ? 0 : 1); }).on('error', () => process.exit(1));" || exit 1

# Set environment variables
ENV NODE_ENV=production
ENV HARDHAT_NETWORK=localhost

# Start the blockchain service
CMD ["npm", "start"]