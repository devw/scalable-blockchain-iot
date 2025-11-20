# Stage 1: Dependencies
FROM node:22-alpine AS dependencies

WORKDIR /app

# Copy package files
COPY package.json yarn.lock* ./

# Install dependencies
RUN if [ -f yarn.lock ]; then \
      yarn install --frozen-lockfile; \
    else \
      yarn install; \
    fi

# Stage 2: Runtime
FROM node:22-alpine

WORKDIR /app

# Copy dependencies from previous stage
COPY --from=dependencies /app/node_modules ./node_modules

# Copy scripts and utilities
COPY scripts ./scripts
COPY utils ./utils

# Note: contracts are mounted as volume from host
# See docker-compose.yml for volume mount

# Copy configuration
COPY hardhat.config.js ./
COPY package.json ./

# Create directories for artifacts and snapshots
RUN mkdir -p /app/artifacts /app/cache /data/snapshots

# Expose blockchain RPC port
EXPOSE 8545

# Health check
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
  CMD wget --spider -q http://localhost:8545 || exit 1

# Start Hardhat node
CMD ["yarn", "start"]