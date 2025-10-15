#!/bin/bash

# CITS3200 Project - Restart Services Script
# This script stops and then starts the backend and frontend services

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_header() {
    echo -e "${YELLOW}========================================${NC}"
    echo -e "${YELLOW}$1${NC}"
    echo -e "${YELLOW}========================================${NC}"
}

print_header "Restarting CITS3200 Project Services"

# Stop services first
print_status "Stopping existing services..."
./stop-services.sh

# Wait a moment for cleanup
sleep 3

# Start services
print_status "Starting services..."
./start-services.sh
