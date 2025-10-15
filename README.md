# CITS3200 Project - Census Document Discovery System

## 🎯 Project Overview

**Documentation Identification Software/AI Agent**

This project develops a comprehensive system to systematically locate, store, and identify primary census documents from libraries worldwide. The system uses AI-powered cascading search to find census documents across multiple sources including national libraries, statistical bureaus, and web resources.

### 🏛️ Project Context

Human mobility is key to poverty reduction and shared global prosperity. With the 2030 Agenda for Sustainable Development, the international community recognized the contribution that migration makes to global welfare. This system supports research into climate-induced demographic change by providing access to comprehensive census data.

**Client:** Dr Christopher Parsons  
**Mentor:** Matt Noble <matt.noble@uwa.edu.au>  
**Location:** Crawley

### 👥 Team Members

- Rania Khan
- James Felstead  
- Peter Fang
- Chunyu Zheng
- Hazel Wang

## 🏗️ System Architecture

The system consists of three main components:

1. **Backend API** (FastAPI + Python) - Core search engine and data processing
2. **Frontend Web App** (React + Vite) - User interface for search and batch processing
3. **Database** (MySQL) - Storage for libraries, bureaus, and search metadata

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** with pip
- **Node.js 16+** with npm
- **MySQL 8.0+** database server
- **Docker & Docker Compose** (optional, for containerized setup)

### 🐳 Docker Setup (Recommended)

The fastest way to get started:

```bash
# Clone the repository
git clone <repository-url>
cd CITS3200-project

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Start all services
docker-compose up -d

# Import initial data
docker-compose exec backend python -c "
import requests
requests.post('http://localhost:8000/api/import-libraries')
requests.post('http://localhost:8000/api/import-bureaus')
"
```

Access the application at:
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

### 🛠️ Manual Setup

For detailed manual setup instructions, see [SETUP.md](SETUP.md).

## 🔧 Configuration

### Required API Keys

Create a `.env` file in the project root:

```env
# Google Gemini API (for AI query generation)
GEMINI_API_KEY=your_gemini_api_key_here

# Google Custom Search Engine (for web search)
SEARCH_ID=your_google_search_engine_id_here

# Database Configuration
DATABASE_URL=mysql+pymysql://root:3200@localhost:3306/project
```

### Getting API Keys

1. **Gemini API Key:**
   - Visit https://aistudio.google.com/app/apikey
   - Create a new API key
   - Add to your `.env` file

2. **Google Custom Search Engine ID:**
   - Visit https://developers.google.com/custom-search/v1/introduction
   - Create a custom search engine
   - Get the Search Engine ID
   - Add to your `.env` file

## 📋 Features

### 🔍 Cascading Search

The system performs intelligent cascading searches through three phases:

1. **Library Phase** - Searches national and university libraries
2. **Bureau Phase** - Searches statistical bureaus and government agencies  
3. **Web Phase** - Performs web searches for additional resources

### 📊 Batch Processing

- Upload CSV files with multiple census documents
- Parallel processing of up to 5 searches simultaneously
- Progress tracking and error handling
- Export results to CSV format

### 🎯 Advanced Search Parameters

- **Required:** English title, country
- **Optional:** Original title, province, census year, publisher, volume, coloniser
- **Configurable:** Search result limits, worker threads, search depth

### 💾 Data Management

- **Libraries Database:** 50+ national and university libraries
- **Bureaus Database:** 30+ statistical bureaus and government agencies
- **Search History:** Save and reload previous searches
- **Filter Management:** Customizable search filters

## 🗂️ Project Structure

```
CITS3200-project/
├── Backend/                    # Python FastAPI backend
│   ├── api.py                 # Main API application
│   ├── start_api.py          # API startup script
│   ├── requirements.txt      # Python dependencies
│   ├── dockerfile           # Docker configuration
│   ├── data/                # Library and bureau configurations
│   │   ├── libraries.json   # Library search configurations
│   │   └── bureaus.json     # Bureau search configurations
│   ├── db/                  # Database models and setup
│   │   ├── models.py        # SQLAlchemy models
│   │   ├── db.py           # Database connection
│   │   ├── create_db.py    # Database creation script
│   │   └── seed.py         # Sample data seeding
│   └── GoogleSearch_WS/     # Core search engine modules
│       ├── AITool.py       # AI query generation and ranking
│       ├── Func_Library.py # Library search functions
│       ├── Func_PDF_GoogleWS.py # Web search functions
│       ├── ScraperTool.py  # Web scraping utilities
│       ├── Setup.py        # Module setup script
│       ├── testCensusWS.py # Test implementation
│       └── Unit_Tests/     # Unit tests
├── Frontend/                 # React frontend application
│   ├── src/
│   │   ├── App.jsx         # Main application component
│   │   ├── App.css         # Application styles
│   │   └── main.jsx        # Application entry point
│   ├── package.json        # Node.js dependencies
│   ├── vite.config.js      # Vite configuration
│   └── README.md           # Frontend documentation
├── docker-compose.yml       # Docker services configuration
├── setup.sh                # Unix setup script
├── setup.bat               # Windows setup script
├── SETUP.md                # Detailed setup instructions
├── BATCH_SEARCH_GUIDE.md   # Batch processing guide
├── CASCADING_SEARCH_SETUP.md # Cascading search setup
└── README.md               # This file
```

## 🔌 API Endpoints

### Core Search Endpoints

- `POST /api/cascading-search` - Perform cascading search
- `POST /api/batch-search` - Upload CSV for batch processing
- `GET /api/health` - Health check
- `GET /api/diagnostics` - System diagnostics

### Data Management Endpoints

- `GET /api/libraries` - List all libraries
- `POST /api/libraries` - Create new library
- `PUT /api/libraries/{id}` - Update library
- `DELETE /api/libraries/{id}` - Delete library
- `POST /api/import-libraries` - Import libraries from JSON

- `GET /api/bureaus` - List all bureaus  
- `POST /api/bureaus` - Create new bureau
- `PUT /api/bureaus/{id}` - Update bureau
- `DELETE /api/bureaus/{id}` - Delete bureau
- `POST /api/import-bureaus` - Import bureaus from JSON

- `GET /api/filters` - List search filters
- `POST /api/filters` - Create new filter
- `PUT /api/filters/{id}` - Update filter
- `DELETE /api/filters/{id}` - Delete filter

## 🧪 Testing

### Backend Tests

```bash
cd Backend/GoogleSearch_WS
python SysTests.py
```

### Unit Tests

```bash
cd Backend/GoogleSearch_WS/Unit_Tests
python -m pytest
```

### Frontend Tests

```bash
cd Frontend
npm test
```

## 📊 Usage Examples

### Single Document Search

```bash
curl -X POST http://localhost:8000/api/cascading-search \
  -H "Content-Type: application/json" \
  -d '{
    "englishTitle": "Census of France 1861",
    "country": "France",
    "cite": "1861"
  }'
```

### Batch Search CSV Format

```csv
Title (In English),Country,Original title,Province,Date/Year of census
"First Census of Argentina 1869",Argentina,"PRIMER CENSO DE LA REPUBLICA ARGENTINA",National Record,1869
"Census of France - Population",France,"STATISTIQUE DE LA FRANCE - POPULATION",National Record,1861
```

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   ```bash
   # Check MySQL is running
   mysql -u root -p -e "SHOW DATABASES;"
   
   # Create database if needed
   mysql -u root -p -e "CREATE DATABASE project;"
   ```

2. **API Keys Not Working**
   - Verify GEMINI_API_KEY is valid
   - Check SEARCH_ID is correct
   - Ensure API quotas haven't been exceeded

3. **Port Already in Use**
   ```bash
   # Find and kill process on port 8000
   lsof -ti:8000 | xargs kill -9
   
   # Or change port in .env
   API_PORT=8001
   ```

4. **Frontend Build Errors**
   ```bash
   cd Frontend
   rm -rf node_modules package-lock.json
   npm install
   ```

### Performance Optimization

- **Reduce Search Time:** Lower `maxWorkers` and `wsAmt` parameters
- **Handle Rate Limits:** Add delays between API calls
- **Database Performance:** Add indexes for frequently queried fields
- **Memory Usage:** Process large batches in smaller chunks

## 🔒 Security Considerations

- **API Keys:** Never commit API keys to version control
- **Database:** Use strong passwords and limit database access
- **CORS:** Configure CORS origins for production deployment
- **Rate Limiting:** Implement rate limiting for production use

## 🚀 Production Deployment

### Backend Deployment

1. **Environment Setup:**
   ```bash
   # Set production environment variables
   export DATABASE_URL="mysql+pymysql://user:pass@host:port/db"
   export GEMINI_API_KEY="your_production_key"
   export SEARCH_ID="your_production_search_id"
   ```

2. **WSGI Server:**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker api:app
   ```

3. **Database Migration:**
   ```bash
   python db/create_db.py
   python -c "
   import requests
   requests.post('http://your-domain/api/import-libraries')
   requests.post('http://your-domain/api/import-bureaus')
   "
   ```

### Frontend Deployment

1. **Build Production Bundle:**
   ```bash
   cd Frontend
   npm run build
   ```

2. **Serve Static Files:**
   ```bash
   # Using nginx
   server {
       listen 80;
       server_name your-domain.com;
       root /path/to/Frontend/dist;
       index index.html;
       
       location / {
           try_files $uri $uri/ /index.html;
       }
   }
   ```

## 📚 Documentation

- [SETUP.md](SETUP.md) - Detailed setup instructions
- [BATCH_SEARCH_GUIDE.md](BATCH_SEARCH_GUIDE.md) - Batch processing guide
- [CASCADING_SEARCH_SETUP.md](CASCADING_SEARCH_SETUP.md) - Cascading search setup
- [API Documentation](http://localhost:8000/docs) - Interactive API docs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is developed for CITS3200 Professional Computing at UWA.

## 🆘 Support

For issues or questions:

1. Check the troubleshooting section above
2. Review the detailed documentation in the `/docs` folder
3. Check backend logs for error messages
4. Verify API keys and database connectivity
5. Contact the development team

## 🎉 Acknowledgments

- Dr Christopher Parsons for the project requirements
- Matt Noble for mentorship and guidance
- UWA CITS3200 course coordinators
- All contributors to the open-source libraries used in this project

---

**Happy searching! 🔍📊**