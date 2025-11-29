#!/bin/bash

# CITS3200 Project - Start Services Script
# This script starts the backend and frontend services

set -e

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

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if port is in use
port_in_use() {
    lsof -ti:$1 >/dev/null 2>&1
}

# Function to wait for service
wait_for_service() {
    local url=$1
    local max_attempts=$2
    local attempt=1
    
    print_status "Waiting for service at $url..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s "$url" >/dev/null 2>&1; then
            print_success "Service is ready!"
            return 0
        fi
        
        echo -n "."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    print_error "Service failed to start within $((max_attempts * 2)) seconds"
    return 1
}

# Check if we're in the right directory
if [[ ! -d "Backend" || ! -d "Frontend" ]]; then
    print_error "Please run this script from the CITS3200-project root directory"
    exit 1
fi

# Check if services are already running
if port_in_use 8000; then
    print_warning "Backend service is already running on port 8000"
else
    # Start backend
    print_status "Starting backend server..."
    cd Backend
    
    if [[ ! -d "venv" ]]; then
        print_error "Backend virtual environment not found. Please run setup first."
        exit 1
    fi
    
    source venv/bin/activate
    python start_api.py &
    BACKEND_PID=$!
    cd ..
    
    # Wait for backend to start
    if wait_for_service "http://localhost:8000/api/health" 30; then
        print_success "Backend server started successfully"
    else
        print_error "Backend server failed to start"
        kill $BACKEND_PID 2>/dev/null || true
        exit 1
    fi
    
    # Save PID
    echo $BACKEND_PID > .backend_pid
fi

if port_in_use 5173; then
    print_warning "Frontend service is already running on port 5173"
else
    # Start frontend
    print_status "Starting frontend server..."
    cd Frontend
    
    if [[ ! -d "node_modules" ]]; then
        print_error "Frontend dependencies not found. Please run setup first."
        exit 1
    fi
    
    npm run dev &
    FRONTEND_PID=$!
    cd ..
    
    # Wait for frontend to start
    if wait_for_service "http://localhost:5173" 30; then
        print_success "Frontend server started successfully"
    else
        print_error "Frontend server failed to start"
        kill $FRONTEND_PID 2>/dev/null || true
        exit 1
    fi
    
    # Save PID
    echo $FRONTEND_PID > .frontend_pid
fi

# Import data if backend just started
if [[ ! -f .backend_pid ]] || ! port_in_use 8000; then
    print_status "Importing library and bureau data..."
    sleep 5
    
    if curl -s -X POST http://localhost:8000/api/import-libraries >/dev/null; then
        print_success "Libraries imported successfully"
    else
        print_warning "Failed to import libraries"
    fi
    
    if curl -s -X POST http://localhost:8000/api/import-bureaus >/dev/null; then
        print_success "Bureaus imported successfully"
    else
        print_warning "Failed to import bureaus"
    fi
fi

print_success "All services are running!"
echo ""
echo -e "${GREEN}Access Points:${NC}"
echo -e "  🌐 Frontend:     ${YELLOW}http://localhost:5173${NC}"
echo -e "  🔧 Backend API:  ${YELLOW}http://localhost:8000${NC}"
echo -e "  📚 API Docs:     ${YELLOW}http://localhost:8000/docs${NC}"
echo ""
echo -e "${BLUE}Press Ctrl+C to stop all services${NC}"

# Keep script running
while true; do
    sleep 1
done
