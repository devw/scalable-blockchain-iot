#!/bin/bash

# Snapshot Helper Script
# Provides easy commands for blockchain snapshot management

set -e

CONTAINER_NAME="blockchain-hardhat"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_usage() {
    echo -e "${BLUE}Blockchain Snapshot Helper${NC}"
    echo ""
    echo "Usage: ./scripts/snapshot-helper.sh [command]"
    echo ""
    echo "Commands:"
    echo "  export    - Create a new snapshot of current blockchain state"
    echo "  import    - Restore blockchain state from latest snapshot"
    echo "  list      - List all available snapshots"
    echo "  clean     - Remove all snapshots"
    echo ""
    echo "Examples:"
    echo "  ./scripts/snapshot-helper.sh export"
    echo "  ./scripts/snapshot-helper.sh list"
    echo ""
}

check_container_running() {
    if ! docker ps | grep -q "$CONTAINER_NAME"; then
        echo -e "${RED}❌ Error: Container '$CONTAINER_NAME' is not running${NC}"
        echo "Start the container with: docker-compose up -d"
        exit 1
    fi
}

export_snapshot() {
    echo -e "${BLUE}📸 Creating blockchain snapshot...${NC}"
    check_container_running
    
    docker exec $CONTAINER_NAME yarn snapshot:export
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Snapshot created successfully${NC}"
    else
        echo -e "${RED}❌ Snapshot creation failed${NC}"
        exit 1
    fi
}

import_snapshot() {
    echo -e "${BLUE}📥 Restoring blockchain snapshot...${NC}"
    check_container_running
    
    docker exec $CONTAINER_NAME yarn snapshot:import
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Snapshot restored successfully${NC}"
        echo -e "${YELLOW}⚠️  Note: Redeploy contracts to restore full state${NC}"
    else
        echo -e "${RED}❌ Snapshot restore failed${NC}"
        exit 1
    fi
}

list_snapshots() {
    echo -e "${BLUE}📋 Listing available snapshots...${NC}"
    check_container_running
    
    docker exec $CONTAINER_NAME yarn snapshot:list
}

clean_snapshots() {
    echo -e "${YELLOW}⚠️  This will delete all snapshots. Are you sure? (y/N)${NC}"
    read -r response
    
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo -e "${BLUE}🗑️  Cleaning snapshots...${NC}"
        
        # Clean in container
        docker exec $CONTAINER_NAME sh -c "rm -f /data/snapshots/*.json"
        
        # Clean in host
        rm -f ./data/snapshots/*.json 2>/dev/null || true
        
        echo -e "${GREEN}✅ All snapshots removed${NC}"
    else
        echo -e "${BLUE}Cancelled${NC}"
    fi
}

# Main script logic
case "$1" in
    export)
        export_snapshot
        ;;
    import)
        import_snapshot
        ;;
    list)
        list_snapshots
        ;;
    clean)
        clean_snapshots
        ;;
    *)
        print_usage
        exit 1
        ;;
esac