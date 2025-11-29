#!/bin/bash

# CITS3200 Project - Stop Services Script
# This script stops the backend and frontend services

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

print_status "Stopping CITS3200 Project services..."

# Stop services using PIDs if available
if [[ -f .backend_pid ]]; then
    BACKEND_PID=$(cat .backend_pid)
    if kill -0 $BACKEND_PID 2>/dev/null; then
        print_status "Stopping backend server (PID: $BACKEND_PID)..."
        kill $BACKEND_PID
        sleep 2
        if kill -0 $BACKEND_PID 2>/dev/null; then
            print_warning "Backend didn't stop gracefully, forcing termination..."
            kill -9 $BACKEND_PID
        fi
        print_success "Backend server stopped"
    else
        print_warning "Backend PID file exists but process is not running"
    fi
    rm -f .backend_pid
fi

if [[ -f .frontend_pid ]]; then
    FRONTEND_PID=$(cat .frontend_pid)
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        print_status "Stopping frontend server (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID
        sleep 2
        if kill -0 $FRONTEND_PID 2>/dev/null; then
            print_warning "Frontend didn't stop gracefully, forcing termination..."
            kill -9 $FRONTEND_PID
        fi
        print_success "Frontend server stopped"
    else
        print_warning "Frontend PID file exists but process is not running"
    fi
    rm -f .frontend_pid
fi

# Kill any remaining processes by name
print_status "Cleaning up any remaining processes..."

# Kill backend processes
pkill -f "python start_api.py" 2>/dev/null && print_success "Killed remaining backend processes" || print_status "No backend processes to kill"

# Kill frontend processes
pkill -f "npm run dev" 2>/dev/null && print_success "Killed remaining frontend processes" || print_status "No frontend processes to kill"

# Kill any uvicorn processes
pkill -f "uvicorn" 2>/dev/null && print_success "Killed remaining uvicorn processes" || print_status "No uvicorn processes to kill"

# Kill any vite processes
pkill -f "vite" 2>/dev/null && print_success "Killed remaining vite processes" || print_status "No vite processes to kill"

# Check if ports are still in use
if port_in_use 8000; then
    print_warning "Port 8000 is still in use. You may need to manually kill the process."
    print_status "Run: lsof -ti:8000 | xargs kill -9"
fi

if port_in_use 5173; then
    print_warning "Port 5173 is still in use. You may need to manually kill the process."
    print_status "Run: lsof -ti:5173 | xargs kill -9"
fi

print_success "All services stopped successfully!"
echo ""
echo -e "${GREEN}To restart services, run:${NC}"
echo -e "  ${YELLOW}./start-services.sh${NC}"
echo ""
echo -e "${GREEN}Or for full setup:${NC}"
echo -e "  ${YELLOW}./setup-complete.sh${NC}"
