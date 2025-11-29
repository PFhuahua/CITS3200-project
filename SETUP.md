# CITS3200 Project - Complete Setup Guide

This guide provides comprehensive setup instructions for the Census Document Discovery System. Choose your preferred setup method below.

## 🚀 Quick Setup Options

### Option 1: Docker Setup (Recommended - Easiest)
### Option 2: Manual Setup (Full Control)
### Option 3: Hybrid Setup (Docker + Local Development)

---

## 🐳 Option 1: Docker Setup (Recommended)

The fastest way to get the entire system running with minimal configuration.

### Prerequisites

- **Docker** and **Docker Compose** installed
- **Git** for cloning the repository

### Step 1: Clone and Navigate

```bash
git clone <repository-url>
cd CITS3200-project
```

### Step 2: Environment Configuration

Create a `.env` file in the project root:

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your API keys
nano .env  # or use your preferred editor
```

**Required Environment Variables:**

```env
# Google Gemini API Key (Required for AI features)
GEMINI_API_KEY=your_gemini_api_key_here

# Google Custom Search Engine ID (Required for web search)
SEARCH_ID=your_google_search_engine_id_here

# Database Configuration (Optional - defaults provided)
DATABASE_URL=mysql+pymysql://root:3200@db:3306/project

# API Configuration (Optional - defaults provided)
API_HOST=0.0.0.0
API_PORT=8000
```

### Step 3: Start All Services

```bash
# Start all services (database, backend, frontend)
docker-compose up -d

# Check service status
docker-compose ps
```

### Step 4: Initialize Database

```bash
# Wait for services to be ready (30-60 seconds)
sleep 60

# Import library and bureau data
docker-compose exec backend python -c "
import requests
import time
import sys

# Wait for API to be ready
for i in range(30):
    try:
        response = requests.get('http://localhost:8000/api/health')
        if response.status_code == 200:
            print('API is ready!')
            break
    except:
        print(f'Waiting for API... ({i+1}/30)')
        time.sleep(2)
else:
    print('API failed to start within 60 seconds')
    sys.exit(1)

# Import data
try:
    print('Importing libraries...')
    response = requests.post('http://localhost:8000/api/import-libraries')
    print(f'Libraries import: {response.status_code}')
    
    print('Importing bureaus...')
    response = requests.post('http://localhost:8000/api/import-bureaus')
    print(f'Bureaus import: {response.status_code}')
    
    print('✅ Database initialization complete!')
except Exception as e:
    print(f'❌ Error during initialization: {e}')
"
```

### Step 5: Verify Setup

```bash
# Check API health
curl http://localhost:8000/api/health

# Check database diagnostics
curl http://localhost:8000/api/diagnostics
```

### Step 6: Access the Application

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

### Docker Commands

```bash
# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Restart services
docker-compose restart

# Rebuild containers
docker-compose up --build -d

# Clean up (remove containers and volumes)
docker-compose down -v
```

---

## 🛠️ Option 2: Manual Setup

For full control over the installation and development environment.

### Prerequisites

- **Python 3.8+** with pip
- **Node.js 16+** with npm
- **MySQL 8.0+** database server
- **Git** for cloning the repository

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd CITS3200-project
```

### Step 2: Database Setup

#### Install MySQL

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
sudo systemctl enable mysql
```

**macOS (using Homebrew):**
```bash
brew install mysql
brew services start mysql
```

**Windows:**
- Download MySQL Installer from https://dev.mysql.com/downloads/installer/
- Run the installer and follow the setup wizard

#### Create Database

```bash
# Connect to MySQL
mysql -u root -p

# Create database and user
CREATE DATABASE project;
CREATE USER 'census_user'@'localhost' IDENTIFIED BY 'census_password';
GRANT ALL PRIVILEGES ON project.* TO 'census_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Step 3: Backend Setup

#### Create Virtual Environment

```bash
cd Backend
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

#### Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
pip install -r requirements.txt

# Install GoogleSearch_WS dependencies
cd GoogleSearch_WS
pip install -r requirements.txt

# Install Playwright browsers
python -m playwright install chromium
python -m playwright install-deps chromium
cd ..
```

#### Environment Configuration

```bash
# Create .env file
cat > .env << EOF
GEMINI_API_KEY=your_gemini_api_key_here
SEARCH_ID=your_google_search_engine_id_here
DATABASE_URL=mysql+pymysql://census_user:census_password@localhost:3306/project
API_HOST=0.0.0.0
API_PORT=8000
EOF
```

#### Initialize Database

```bash
# Create database tables
cd db
python create_db.py
cd ..

# Start the API server
python start_api.py &
API_PID=$!

# Wait for API to start
sleep 10

# Import data
curl -X POST http://localhost:8000/api/import-libraries
curl -X POST http://localhost:8000/api/import-bureaus

# Verify setup
curl http://localhost:8000/api/health
curl http://localhost:8000/api/diagnostics
```

### Step 4: Frontend Setup

#### Install Dependencies

```bash
cd ../Frontend
npm install
```

#### Environment Configuration (Optional)

```bash
# Create .env file for frontend (optional)
echo "VITE_API_URL=http://localhost:8000" > .env
```

#### Start Development Server

```bash
npm run dev
```

### Step 5: Verify Complete Setup

```bash
# Check backend
curl http://localhost:8000/api/health

# Check frontend (should return HTML)
curl http://localhost:5173

# Check database
mysql -u census_user -p project -e "SHOW TABLES;"
```

---

## 🔄 Option 3: Hybrid Setup (Docker + Local Development)

Use Docker for services (database) and run backend/frontend locally for development.

### Step 1: Start Database with Docker

```bash
# Start only the database service
docker-compose up -d db

# Wait for database to be ready
sleep 30
```

### Step 2: Backend Setup (Local)

```bash
cd Backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate  # Windows

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
cd GoogleSearch_WS
pip install -r requirements.txt
python -m playwright install chromium
cd ..

# Configure environment for Docker database
cat > .env << EOF
GEMINI_API_KEY=your_gemini_api_key_here
SEARCH_ID=your_google_search_engine_id_here
DATABASE_URL=mysql+pymysql://root:3200@localhost:3307/project
API_HOST=0.0.0.0
API_PORT=8000
EOF

# Initialize database
cd db
python create_db.py
cd ..

# Start backend
python start_api.py &
```

### Step 3: Frontend Setup (Local)

```bash
cd ../Frontend
npm install
npm run dev
```

### Step 4: Import Data

```bash
# Wait for backend to start
sleep 10

# Import data
curl -X POST http://localhost:8000/api/import-libraries
curl -X POST http://localhost:8000/api/import-bureaus
```

---

## 🔑 Getting API Keys

### Google Gemini API Key

1. Visit https://aistudio.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key
5. Add to your `.env` file as `GEMINI_API_KEY`

### Google Custom Search Engine ID

1. Visit https://developers.google.com/custom-search/v1/introduction
2. Click "Get a Key"
3. Create a new project or select existing
4. Enable the Custom Search API
5. Create credentials (API key)
6. Go to https://cse.google.com/cse/
7. Click "Add" to create a new search engine
8. Configure the search engine:
   - **Sites to search:** `*` (search entire web)
   - **Name:** "Census Document Search"
9. Click "Create"
10. Go to "Setup" → "Basics"
11. Copy the "Search engine ID"
12. Add to your `.env` file as `SEARCH_ID`

---

## 🧪 Testing Your Setup

### Backend Tests

```bash
cd Backend/GoogleSearch_WS
python SysTests.py
```

### API Health Check

```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00.000000",
  "version": "1.0.0"
}
```

### Database Diagnostics

```bash
curl http://localhost:8000/api/diagnostics
```

Expected response:
```json
{
  "status": "ok",
  "database": {
    "libraries_count": 50,
    "bureaus_count": 30,
    "sample_library_countries": ["France", "Spain", "UK"],
    "sample_bureau_countries": ["France", "South Africa", "UK"]
  },
  "environment": {
    "GEMINI_API_KEY": true,
    "SEARCH_ID": true
  }
}
```

### Frontend Test

1. Open http://localhost:5173 in your browser
2. You should see the Census Document Search interface
3. Try a sample search:
   - **Title:** "Census of France"
   - **Country:** "France"
   - Click "Search"

---

## 🚨 Troubleshooting

### Common Issues

#### 1. Database Connection Failed

**Symptoms:**
- `sqlalchemy.exc.OperationalError: (pymysql.err.OperationalError)`
- API returns 500 errors

**Solutions:**
```bash
# Check MySQL is running
sudo systemctl status mysql  # Linux
brew services list | grep mysql  # macOS

# Test database connection
mysql -u root -p -e "SHOW DATABASES;"

# Check database exists
mysql -u root -p -e "USE project; SHOW TABLES;"

# Recreate database if needed
mysql -u root -p -e "DROP DATABASE IF EXISTS project; CREATE DATABASE project;"
```

#### 2. API Keys Not Working

**Symptoms:**
- "GEMINI_API_KEY not configured" errors
- Search returns "Invalid query format"

**Solutions:**
```bash
# Check environment variables
echo $GEMINI_API_KEY
echo $SEARCH_ID

# Verify .env file exists and has correct format
cat Backend/.env

# Restart backend after changing .env
pkill -f "python start_api.py"
cd Backend && python start_api.py &
```

#### 3. Port Already in Use

**Symptoms:**
- `OSError: [Errno 48] Address already in use`
- Frontend/backend won't start

**Solutions:**
```bash
# Find process using port 8000
lsof -ti:8000  # Linux/macOS
netstat -ano | findstr :8000  # Windows

# Kill the process
lsof -ti:8000 | xargs kill -9  # Linux/macOS
taskkill /PID <PID> /F  # Windows

# Or change port in .env
echo "API_PORT=8001" >> Backend/.env
```

#### 4. Frontend Build Errors

**Symptoms:**
- `npm install` fails
- `npm run dev` shows errors

**Solutions:**
```bash
cd Frontend

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm cache clean --force
npm install

# Check Node.js version
node --version  # Should be 16+

# Update npm
npm install -g npm@latest
```

#### 5. Playwright Installation Issues

**Symptoms:**
- `playwright install` fails
- Browser not found errors

**Solutions:**
```bash
cd Backend/GoogleSearch_WS

# Install system dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libwayland-client0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils

# Reinstall Playwright
python -m playwright install chromium
python -m playwright install-deps chromium
```

#### 6. Docker Issues

**Symptoms:**
- `docker-compose up` fails
- Containers won't start

**Solutions:**
```bash
# Check Docker is running
docker --version
docker-compose --version

# Clean up Docker
docker-compose down -v
docker system prune -f

# Rebuild containers
docker-compose up --build -d

# Check container logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db
```

### Performance Issues

#### Slow Search Performance

**Solutions:**
```bash
# Reduce search parameters in frontend
# Edit Frontend/src/App.jsx, reduce:
# - numLibResults: 1
# - numBurResults: 3
# - wsResults: 3
# - wsAmt: 10
# - maxWorkers: 5
```

#### High Memory Usage

**Solutions:**
```bash
# Process smaller batches
# Split large CSV files into smaller chunks
# Reduce maxWorkers parameter
# Monitor system resources: htop, Activity Monitor, Task Manager
```

---

## 🔧 Development Workflow

### Daily Development

```bash
# Start development environment
cd CITS3200-project

# Option 1: Full Docker
docker-compose up -d

# Option 2: Hybrid (database in Docker, code local)
docker-compose up -d db
cd Backend && source venv/bin/activate && python start_api.py &
cd ../Frontend && npm run dev

# Make changes to code
# Backend auto-reloads with uvicorn --reload
# Frontend auto-reloads with Vite HMR

# Test changes
curl http://localhost:8000/api/health
# Open http://localhost:5173 in browser
```

### Adding New Libraries/Bureaus

```bash
# Edit data files
nano Backend/data/libraries.json
nano Backend/data/bureaus.json

# Import updated data
curl -X POST http://localhost:8000/api/import-libraries
curl -X POST http://localhost:8000/api/import-bureaus

# Verify import
curl http://localhost:8000/api/libraries | jq length
curl http://localhost:8000/api/bureaus | jq length
```

### Database Management

```bash
# Connect to database
mysql -u root -p project

# View tables
SHOW TABLES;

# Check library data
SELECT COUNT(*) FROM libraries;
SELECT name, country FROM libraries LIMIT 5;

# Check bureau data
SELECT COUNT(*) FROM bureaus;
SELECT name, country FROM bureaus LIMIT 5;

# Backup database
mysqldump -u root -p project > backup.sql

# Restore database
mysql -u root -p project < backup.sql
```

---

## 📊 Monitoring and Logs

### Backend Logs

```bash
# Docker setup
docker-compose logs -f backend

# Manual setup
tail -f Backend/api.log  # if logging to file
# Or check terminal where start_api.py is running
```

### Frontend Logs

```bash
# Check browser console (F12 → Console)
# Or check terminal where npm run dev is running
```

### Database Logs

```bash
# Docker setup
docker-compose logs -f db

# Manual setup
sudo tail -f /var/log/mysql/error.log  # Linux
tail -f /usr/local/var/mysql/*.err  # macOS
```

### System Monitoring

```bash
# Check resource usage
htop  # Linux
top  # macOS/Linux
# Task Manager on Windows

# Check disk space
df -h

# Check network connections
netstat -tulpn | grep :8000
netstat -tulpn | grep :5173
```

---

## 🚀 Production Deployment

### Backend Production Setup

```bash
# Install production WSGI server
pip install gunicorn

# Create production .env
cat > Backend/.env.production << EOF
GEMINI_API_KEY=your_production_gemini_key
SEARCH_ID=your_production_search_id
DATABASE_URL=mysql+pymysql://prod_user:secure_password@prod_host:3306/project
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=production
EOF

# Start with Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker api:app --bind 0.0.0.0:8000
```

### Frontend Production Build

```bash
cd Frontend

# Build production bundle
npm run build

# Serve with nginx
sudo cp -r dist/* /var/www/html/

# Or serve with Node.js
npm install -g serve
serve -s dist -l 3000
```

### Database Production Setup

```bash
# Create production database user
mysql -u root -p
CREATE USER 'prod_user'@'%' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON project.* TO 'prod_user'@'%';
FLUSH PRIVILEGES;

# Configure MySQL for production
# Edit /etc/mysql/mysql.conf.d/mysqld.cnf
# Set appropriate values for:
# - max_connections
# - innodb_buffer_pool_size
# - query_cache_size
```

---

## 📚 Additional Resources

### Documentation Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Playwright Documentation](https://playwright.dev/python/)

### API References

- [Google Gemini API](https://ai.google.dev/docs)
- [Google Custom Search API](https://developers.google.com/custom-search/v1/introduction)
- [MySQL Documentation](https://dev.mysql.com/doc/)

### Project-Specific Documentation

- [BATCH_SEARCH_GUIDE.md](BATCH_SEARCH_GUIDE.md) - Batch processing guide
- [CASCADING_SEARCH_SETUP.md](CASCADING_SEARCH_SETUP.md) - Cascading search setup
- [Backend/GoogleSearch_WS/README.md](Backend/GoogleSearch_WS/README.md) - Search engine documentation
- [Frontend/README.md](Frontend/README.md) - Frontend documentation

---

## 🆘 Getting Help

### Before Asking for Help

1. **Check the logs** - Backend, frontend, and database logs often contain the solution
2. **Verify prerequisites** - Ensure all required software is installed and up to date
3. **Test API keys** - Verify your Gemini API key and Google Search Engine ID are correct
4. **Check network connectivity** - Ensure ports 8000 and 5173 are accessible
5. **Review this guide** - Many common issues are covered in the troubleshooting section

### When Asking for Help

Please include:

1. **Your setup method** - Docker, manual, or hybrid
2. **Operating system** - Linux, macOS, Windows, and version
3. **Error messages** - Full error output from logs
4. **Steps taken** - What you've already tried
5. **Environment details** - Python version, Node.js version, etc.

### Contact Information

- **Project Repository:** [GitHub Issues](https://github.com/your-repo/issues)
- **Course Coordinator:** Matt Noble <matt.noble@uwa.edu.au>
- **Client:** Dr Christopher Parsons

---

## 🎉 Success!

If you've reached this point and everything is working, congratulations! You now have a fully functional Census Document Discovery System.

### Next Steps

1. **Explore the API** - Visit http://localhost:8000/docs for interactive API documentation
2. **Try sample searches** - Use the frontend to search for census documents
3. **Test batch processing** - Upload a CSV file with multiple documents
4. **Review the code** - Understand how the cascading search works
5. **Contribute** - Add new libraries, improve search algorithms, or enhance the UI

### Happy Searching! 🔍📊