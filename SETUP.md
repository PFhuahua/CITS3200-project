# CITS3200 Project Setup

This document explains how to initialize and set up both the frontend and backend environments for the CITS3200 project.

## Prerequisites

Before running the setup scripts, make sure you have the following installed:

### For Backend (Python)
- Python 3.7 or higher
- pip (Python package installer)

### For Frontend (Node.js)
- Node.js (version 16 or higher recommended)
- npm (comes with Node.js)

## Quick Setup

### For macOS/Linux users:
```bash
./setup.sh
```

### For Windows users:
```cmd
setup.bat
```

## What the Setup Scripts Do

### Backend Setup:
1. Creates a Python virtual environment (`venv/`) in the Backend directory
2. Activates the virtual environment
3. Upgrades pip to the latest version
4. Installs all dependencies from `requirements.txt`

### Frontend Setup:
1. Navigates to the Frontend directory
2. Runs `npm install` to install all Node.js dependencies from `package.json`

## Manual Setup (Alternative)

If you prefer to set up manually or the scripts don't work:

### Backend Manual Setup:
```bash
cd Backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
```

### Frontend Manual Setup:
```bash
cd Frontend
npm install
```

## Running the Application

After setup is complete:

### Start the Backend:
```bash
cd Backend
source venv/bin/activate  # On Windows: venv\Scripts\activate.bat
python start_api.py
```

### Start the Frontend:
```bash
cd Frontend
npm run dev
```

## Troubleshooting

### Common Issues:

1. **Permission denied when running setup.sh**
   - Run: `chmod +x setup.sh`

2. **Python/Node.js not found**
   - Make sure Python 3 and Node.js are installed and added to your PATH

3. **Virtual environment activation fails**
   - Make sure you're in the correct directory
   - On Windows, try using `venv\Scripts\activate.bat` instead of `source`

4. **npm install fails**
   - Try deleting `node_modules/` and `package-lock.json`, then run `npm install` again
   - Make sure you have the latest version of npm: `npm install -g npm@latest`

## Development Workflow

1. Always activate the Python virtual environment when working on backend code
2. Use `npm run dev` for frontend development with hot reloading
3. Both servers can run simultaneously on different ports

## Additional Commands

### Backend:
- `pip freeze > requirements.txt` - Update requirements file
- `deactivate` - Exit virtual environment

### Frontend:
- `npm run build` - Build for production
- `npm run lint` - Run linting
- `npm run preview` - Preview production build
