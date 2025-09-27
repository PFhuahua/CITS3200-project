#!/bin/bash

# CITS3200 Project Setup Script
# This script initializes both frontend and backend environments

set -e  # Exit on any error

echo "🚀 Starting CITS3200 Project Setup..."
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
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

# Check if we're in the right directory
if [[ ! -d "Frontend" || ! -d "Backend" ]]; then
    print_error "Please run this script from the CITS3200-project root directory"
    exit 1
fi

# Backend Setup
echo ""
print_status "Setting up Backend (Python Virtual Environment)..."
echo "=================================================="

cd Backend

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

print_status "Python version: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [[ ! -d "venv" ]]; then
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_warning "Virtual environment already exists"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install requirements
if [[ -f "requirements.txt" ]]; then
    print_status "Installing Python dependencies from requirements.txt..."
    pip install -r requirements.txt
    print_success "Python dependencies installed"
else
    print_warning "requirements.txt not found in Backend directory"
fi

# Deactivate virtual environment
deactivate

print_success "Backend setup completed!"

# Frontend Setup
echo ""
print_status "Setting up Frontend (Node.js Dependencies)..."
echo "=============================================="

cd ../Frontend

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js first."
    exit 1
fi

print_status "Node.js version: $(node --version)"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    print_error "npm is not installed. Please install npm first."
    exit 1
fi

print_status "npm version: $(npm --version)"

# Install dependencies
if [[ -f "package.json" ]]; then
    print_status "Installing Node.js dependencies..."
    npm install
    print_success "Node.js dependencies installed"
else
    print_warning "package.json not found in Frontend directory"
fi

print_success "Frontend setup completed!"

# Final instructions
echo ""
echo "🎉 Setup Complete!"
echo "=================="
print_success "Both frontend and backend have been initialized successfully!"

echo ""
echo "📝 Next Steps:"
echo "-------------"
echo "To run the backend:"
echo "  cd Backend"
echo "  source venv/bin/activate  # Activate virtual environment"
echo "  python start_api.py       # Start the backend server"

echo ""
echo "To run the frontend:"
echo "  cd Frontend"
echo "  npm run dev              # Start the development server"

echo ""
echo "To run both simultaneously, open two terminal windows and run the commands above in each."

print_success "Happy coding! 🚀"
