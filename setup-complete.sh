#!/bin/bash

# CITS3200 Project - Complete Automated Setup Script
# This script sets up the entire Census Document Discovery System

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_header() {
    echo -e "${PURPLE}========================================${NC}"
    echo -e "${PURPLE}$1${NC}"
    echo -e "${PURPLE}========================================${NC}"
}

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

print_step() {
    echo -e "${CYAN}[STEP]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
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

# Function to setup environment file
setup_env_file() {
    local env_file=$1
    
    if [ ! -f "$env_file" ]; then
        print_step "Creating environment file: $env_file"
        
        cat > "$env_file" << EOF
# Google Gemini API Key (Required for AI features)
# Get your key from: https://aistudio.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here

# Google Custom Search Engine ID (Required for web search)
# Get your ID from: https://developers.google.com/custom-search/v1/introduction
SEARCH_ID=your_google_search_engine_id_here

# Database Configuration
DATABASE_URL=mysql+pymysql://root:3200@localhost:3306/project

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
EOF
        
        print_warning "Please edit $env_file and add your API keys before continuing!"
        print_warning "Press Enter when you've added your API keys..."
        read -r
    else
        print_status "Environment file already exists: $env_file"
    fi
}

# Function to check prerequisites
check_prerequisites() {
    print_header "Checking Prerequisites"
    
    local missing_deps=()
    
    # Check Python
    if command_exists python3; then
        local python_version=$(python3 --version | cut -d' ' -f2)
        print_success "Python 3 found: $python_version"
    else
        missing_deps+=("python3")
    fi
    
    # Check pip
    if command_exists pip3; then
        print_success "pip3 found"
    else
        missing_deps+=("pip3")
    fi
    
    # Check Node.js
    if command_exists node; then
        local node_version=$(node --version)
        print_success "Node.js found: $node_version"
    else
        missing_deps+=("node")
    fi
    
    # Check npm
    if command_exists npm; then
        local npm_version=$(npm --version)
        print_success "npm found: $npm_version"
    else
        missing_deps+=("npm")
    fi
    
    # Check MySQL
    if command_exists mysql; then
        print_success "MySQL client found"
    else
        print_warning "MySQL client not found - you may need to install MySQL server"
    fi
    
    # Check Docker (optional)
    if command_exists docker; then
        print_success "Docker found (optional for containerized setup)"
    else
        print_warning "Docker not found - you can install it for easier setup"
    fi
    
    # Check Docker Compose (optional)
    if command_exists docker-compose; then
        print_success "Docker Compose found (optional for containerized setup)"
    else
        print_warning "Docker Compose not found - you can install it for easier setup"
    fi
    
    if [ ${#missing_deps[@]} -gt 0 ]; then
        print_error "Missing required dependencies: ${missing_deps[*]}"
        print_error "Please install the missing dependencies and run this script again."
        exit 1
    fi
    
    print_success "All required prerequisites are installed!"
}

# Function to setup backend
setup_backend() {
    print_header "Setting Up Backend"
    
    cd Backend
    
    # Check if we're in the right directory
    if [[ ! -f "requirements.txt" ]]; then
        print_error "requirements.txt not found. Please run this script from the project root."
        exit 1
    fi
    
    # Create virtual environment
    if [[ ! -d "venv" ]]; then
        print_step "Creating Python virtual environment..."
        python3 -m venv venv
        print_success "Virtual environment created"
    else
        print_warning "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    print_step "Activating virtual environment..."
    source venv/bin/activate
    
    # Upgrade pip
    print_step "Upgrading pip..."
    pip install --upgrade pip
    
    # Install main requirements
    print_step "Installing Python dependencies..."
    pip install -r requirements.txt
    
    # Install GoogleSearch_WS requirements
    print_step "Installing GoogleSearch_WS dependencies..."
    cd GoogleSearch_WS
    pip install -r requirements.txt
    
    # Install Playwright browsers
    print_step "Installing Playwright browsers..."
    python -m playwright install chromium
    python -m playwright install-deps chromium
    
    cd ..
    
    # Setup environment file
    setup_env_file ".env"
    
    # Deactivate virtual environment
    deactivate
    
    print_success "Backend setup completed!"
    cd ..
}

# Function to setup frontend
setup_frontend() {
    print_header "Setting Up Frontend"
    
    cd Frontend
    
    # Check if we're in the right directory
    if [[ ! -f "package.json" ]]; then
        print_error "package.json not found. Please run this script from the project root."
        exit 1
    fi
    
    # Install Node.js dependencies
    print_step "Installing Node.js dependencies..."
    npm install
    
    # Setup environment file (optional)
    if [[ ! -f ".env" ]]; then
        print_step "Creating frontend environment file..."
        echo "VITE_API_URL=http://localhost:8000" > .env
    fi
    
    print_success "Frontend setup completed!"
    cd ..
}

# Function to setup database
setup_database() {
    print_header "Setting Up Database"
    
    # Check if MySQL is running
    if ! command_exists mysql; then
        print_error "MySQL client not found. Please install MySQL server first."
        exit 1
    fi
    
    # Try to connect to MySQL
    print_step "Testing MySQL connection..."
    if mysql -u root -p3200 -e "SELECT 1;" >/dev/null 2>&1; then
        print_success "MySQL connection successful"
    else
        print_warning "Could not connect to MySQL with default credentials"
        print_warning "Please ensure MySQL is running and accessible"
        print_warning "Default credentials: root/3200"
        
        # Try to create database anyway
        print_step "Attempting to create database..."
        if mysql -u root -p3200 -e "CREATE DATABASE IF NOT EXISTS project;" 2>/dev/null; then
            print_success "Database created successfully"
        else
            print_error "Failed to create database. Please check MySQL configuration."
            exit 1
        fi
    fi
    
    # Initialize database tables
    print_step "Initializing database tables..."
    cd Backend
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Create tables
    cd db
    python create_db.py
    cd ..
    
    # Deactivate virtual environment
    deactivate
    
    cd ..
    
    print_success "Database setup completed!"
}

# Function to start services
start_services() {
    print_header "Starting Services"
    
    # Check if ports are already in use
    if port_in_use 8000; then
        print_warning "Port 8000 is already in use. Stopping existing process..."
        lsof -ti:8000 | xargs kill -9 2>/dev/null || true
        sleep 2
    fi
    
    if port_in_use 5173; then
        print_warning "Port 5173 is already in use. Stopping existing process..."
        lsof -ti:5173 | xargs kill -9 2>/dev/null || true
        sleep 2
    fi
    
    # Start backend
    print_step "Starting backend server..."
    cd Backend
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
    
    # Start frontend
    print_step "Starting frontend server..."
    cd Frontend
    npm run dev &
    FRONTEND_PID=$!
    cd ..
    
    # Wait for frontend to start
    if wait_for_service "http://localhost:5173" 30; then
        print_success "Frontend server started successfully"
    else
        print_error "Frontend server failed to start"
        kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
        exit 1
    fi
    
    # Import data
    print_step "Importing library and bureau data..."
    sleep 5  # Give backend a moment to fully initialize
    
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
    
    # Save PIDs for cleanup
    echo $BACKEND_PID > .backend_pid
    echo $FRONTEND_PID > .frontend_pid
    
    print_success "All services started successfully!"
}

# Function to verify setup
verify_setup() {
    print_header "Verifying Setup"
    
    # Test backend health
    print_step "Testing backend health..."
    if curl -s http://localhost:8000/api/health | grep -q "healthy"; then
        print_success "Backend health check passed"
    else
        print_error "Backend health check failed"
        return 1
    fi
    
    # Test database diagnostics
    print_step "Testing database diagnostics..."
    if curl -s http://localhost:8000/api/diagnostics | grep -q "ok"; then
        print_success "Database diagnostics passed"
    else
        print_warning "Database diagnostics failed - check database connection"
    fi
    
    # Test frontend
    print_step "Testing frontend..."
    if curl -s http://localhost:5173 | grep -q "Census Document Search"; then
        print_success "Frontend is accessible"
    else
        print_warning "Frontend test failed - check if it's running properly"
    fi
    
    # Test API documentation
    print_step "Testing API documentation..."
    if curl -s http://localhost:8000/docs | grep -q "Swagger"; then
        print_success "API documentation is accessible"
    else
        print_warning "API documentation test failed"
    fi
    
    print_success "Setup verification completed!"
}

# Function to show final instructions
show_final_instructions() {
    print_header "Setup Complete! 🎉"
    
    echo -e "${GREEN}Your Census Document Discovery System is now running!${NC}"
    echo ""
    echo -e "${CYAN}Access Points:${NC}"
    echo -e "  🌐 Frontend:     ${YELLOW}http://localhost:5173${NC}"
    echo -e "  🔧 Backend API:  ${YELLOW}http://localhost:8000${NC}"
    echo -e "  📚 API Docs:     ${YELLOW}http://localhost:8000/docs${NC}"
    echo ""
    echo -e "${CYAN}Next Steps:${NC}"
    echo -e "  1. Open ${YELLOW}http://localhost:5173${NC} in your browser"
    echo -e "  2. Try a sample search:"
    echo -e "     - Title: ${YELLOW}Census of France${NC}"
    echo -e "     - Country: ${YELLOW}France${NC}"
    echo -e "  3. Explore the API documentation at ${YELLOW}http://localhost:8000/docs${NC}"
    echo ""
    echo -e "${CYAN}Important Notes:${NC}"
    echo -e "  • Make sure you've added your API keys to ${YELLOW}Backend/.env${NC}"
    echo -e "  • The system will stop when you close this terminal"
    echo -e "  • To stop manually: ${YELLOW}./stop-services.sh${NC}"
    echo -e "  • To restart: ${YELLOW}./start-services.sh${NC}"
    echo ""
    echo -e "${CYAN}Troubleshooting:${NC}"
    echo -e "  • Check logs: ${YELLOW}tail -f Backend/api.log${NC}"
    echo -e "  • Restart services: ${YELLOW}./restart-services.sh${NC}"
    echo -e "  • View this guide: ${YELLOW}cat SETUP.md${NC}"
    echo ""
    echo -e "${GREEN}Happy searching! 🔍📊${NC}"
}

# Function to cleanup on exit
cleanup() {
    print_status "Cleaning up..."
    
    # Kill background processes
    if [ -f .backend_pid ]; then
        kill $(cat .backend_pid) 2>/dev/null || true
        rm -f .backend_pid
    fi
    
    if [ -f .frontend_pid ]; then
        kill $(cat .frontend_pid) 2>/dev/null || true
        rm -f .frontend_pid
    fi
    
    # Kill any remaining processes
    pkill -f "python start_api.py" 2>/dev/null || true
    pkill -f "npm run dev" 2>/dev/null || true
}

# Set up signal handlers
trap cleanup EXIT INT TERM

# Main execution
main() {
    print_header "CITS3200 Project - Complete Setup"
    echo -e "${CYAN}This script will set up the entire Census Document Discovery System${NC}"
    echo ""
    
    # Check if we're in the right directory
    if [[ ! -d "Backend" || ! -d "Frontend" ]]; then
        print_error "Please run this script from the CITS3200-project root directory"
        exit 1
    fi
    
    # Ask user for setup method
    echo -e "${CYAN}Choose setup method:${NC}"
    echo "1) Full setup (Backend + Frontend + Database)"
    echo "2) Backend only"
    echo "3) Frontend only"
    echo "4) Database only"
    echo "5) Start services only"
    echo "6) Verify setup only"
    echo ""
    read -p "Enter your choice (1-6): " choice
    
    case $choice in
        1)
            check_prerequisites
            setup_backend
            setup_frontend
            setup_database
            start_services
            verify_setup
            show_final_instructions
            ;;
        2)
            check_prerequisites
            setup_backend
            ;;
        3)
            check_prerequisites
            setup_frontend
            ;;
        4)
            setup_database
            ;;
        5)
            start_services
            show_final_instructions
            ;;
        6)
            verify_setup
            ;;
        *)
            print_error "Invalid choice. Please run the script again and select 1-6."
            exit 1
            ;;
    esac
    
    # Keep services running
    if [ "$choice" = "1" ] || [ "$choice" = "5" ]; then
        print_status "Services are running. Press Ctrl+C to stop all services."
        while true; do
            sleep 1
        done
    fi
}

# Run main function
main "$@"
