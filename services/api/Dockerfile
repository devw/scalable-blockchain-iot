# Base image - Node.js 22 LTS (same as blockchain service)
FROM node:22-alpine

# Set working directory
WORKDIR /app

# Install production dependencies only
RUN apk add --no-cache \
    tini

# Enable Corepack and set Yarn to version 1
RUN corepack enable && corepack prepare yarn@1.22.22 --activate

# Copy package files
COPY package.json yarn.lock ./

# Install dependencies
RUN yarn install --frozen-lockfile --production && \
    yarn cache clean

# Copy application source
COPY src ./src

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001 && \
    chown -R nodejs:nodejs /app

# Switch to non-root user
USER nodejs

# Expose API port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/health', (res) => { process.exit(res.statusCode === 200 ? 0 : 1); }).on('error', () => process.exit(1));" || exit 1

# Set environment variables
ENV NODE_ENV=production \
    API_PORT=3000

# Use tini for proper signal handling
ENTRYPOINT ["/sbin/tini", "--"]

# Start the API service
CMD ["yarn", "start"]
