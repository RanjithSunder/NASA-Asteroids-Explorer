# Setup Instructions for NASA Asteroids Explorer

This guide will walk you through setting up the NASA Asteroids Explorer application with the data fetcher component.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+**: Download from [python.org](https://www.python.org/downloads/)
- **MySQL 8.0+**: Download from [mysql.com](https://dev.mysql.com/downloads/)
- **Git**: Download from [git-scm.com](https://git-scm.com/)

## 🚀 Quick Start

### 1. Clone and Setup Project

```bash
# Clone the repository
git clone https://github.com/RanjithSunder/NASA-Asteroids-Explorer.git
cd NASA-Asteroids-Explorer

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup

#### Option A: Using MySQL Command Line
```bash
# Login to MySQL
mysql -u root -p

# Create database and user
CREATE DATABASE nasa CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'nasa_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON nasa.* TO 'nasa_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# Import schema
mysql -u nasa_user -p nasa < database/schema.sql
```

#### Option B: Using MySQL Workbench
1. Open MySQL Workbench
2. Create a new connection to your MySQL server
3. Create a new schema named `nasa`
4. Open and execute the `database/schema.sql` file

### 3. Configuration

#### Create Environment File
```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your settings
nano .env  # or use your preferred editor
```

#### Update .env File
```bash
# NASA API Configuration
NASA_API_KEY=your_actual_nasa_api_key_here

# Database Configuration
DB_HOST=localhost
DB_USER=nasa_user
DB_PASSWORD=secure_password
DB_NAME=nasa
DB_PORT=3306

# Data Fetcher Configuration
TARGET_RECORDS=10000
REQUEST_DELAY=1.0
BATCH_SIZE=100
LOG_LEVEL=INFO
```

### 4. Get NASA API Key

1. Visit [NASA API Portal](https://api.nasa.gov/)
2. Click on "Get Started"
3. Fill out the form to get your API key
4. Copy the API key to your `.env` file

### 5. Fetch Initial Data

```bash
# Run the data fetcher to populate your database
python data_fetcher/nasa_neo_fetcher.py
```

This will:
- Connect to NASA's API
- Fetch asteroid data
- Store it in your MySQL database
- Create proper relationships between tables

### 6. Run the Application

```bash
# Start the Streamlit application
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## 🔧 Advanced Configuration

### Database Connection Testing

Create a test script to verify your database connection:

```python
# test_db_connection.py
import mysql.connector
from config import DB_CONFIG

try:
    connection = mysql.connector.connect(**DB_CONFIG)
    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM asteroids")
        count = cursor.fetchone()[0]
        print(f"✅ Database connected successfully!")
        print(f"📊 Found {count} asteroids in database")
    connection.close()
except Exception as e:
    print(f"❌ Database connection failed: {e}")
```

### Custom Data Fetching

You can customize the data fetcher by modifying `data_fetcher/nasa_neo_fetcher.py`:

```python
# Fetch data for a specific date range
start_date = "2024-01-01"
end_date = "2024-12-31"
target_records = 5000

fetcher = NASANeoFetcher(API_KEY, DB_CONFIG)
data = fetcher.fetch_neo_data(start_date, end_date, target_records)
```

### Logging Configuration

Logs are stored in `nasa_asteroids_explorer.log`. To change log levels:

```python
# In config.py
FETCHER_CONFIG = {
    'log_level': 'DEBUG'  # Change to DEBUG for detailed logs
}
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. MySQL Connection Error
```
mysql.connector.errors.ProgrammingError: 1045 (28000): Access denied
```
**Solution**: Check your database credentials in `.env` file

#### 2. NASA API Rate Limiting
```
requests.exceptions.HTTPError: 429 Client Error: Too Many Requests
```
**Solution**: Increase `REQUEST_DELAY` in your `.env` file

#### 3. Missing Dependencies
```
ModuleNotFoundError: No module named 'streamlit'
```
**Solution**: Make sure your virtual environment is activated and run `pip install -r requirements.txt`

#### 4. Database Schema Issues
```
mysql.connector.errors.ProgrammingError: 1146 (42S02): Table 'nasa.asteroids' doesn't exist
```
**Solution**: Run the database schema: `mysql -u nasa_user -p nasa < database/schema.sql`

### Performance Optimization

#### For Large Datasets
```python
# Increase batch size for faster processing
FETCHER_CONFIG = {
    'batch_size': 500,  # Process 500 records at once
    'target_records': 50000  # Fetch more data
}
```

#### Database Indexing
The schema includes optimized indexes, but for very large datasets, consider:
```sql
-- Add additional indexes if needed
CREATE INDEX idx_composite_date_velocity ON close_approaches (close_approach_date, relative_velocity_kmph);
CREATE INDEX idx_diameter_hazard ON asteroids (estimated_diameter_max_km, is_potentially_hazardous_asteroid);
```

## 📊 Data Validation

After setup, validate your data:

```python
# validation_script.py
import mysql.connector
from config import DB_CONFIG

connection = mysql.connector.connect(**DB_CONFIG)
cursor = connection.cursor()

# Check data quality
queries = [
    "SELECT COUNT(*) as total_asteroids FROM asteroids",
    "SELECT COUNT(*) as total_approaches FROM close_approaches",
    "SELECT COUNT(*) as potentially_hazardous FROM asteroids WHERE is_potentially_hazardous_asteroid = TRUE",
    "SELECT MIN(close_approach_date), MAX(close_approach_date) FROM close_approaches"
]

for query in queries:
    cursor.execute(query)
    result = cursor.fetchone()
    print(f"{query}: {result}")

connection.close()
```

## 🚀 Deployment

### Local Development
The setup above is perfect for local development and testing.

### Production Deployment
For production deployment, consider:

1. **Environment Variables**: Use proper environment variable management
2. **Database Security**: Use strong passwords and limit database access
3. **API Key Security**: Store API keys securely, not in code
4. **Resource Monitoring**: Monitor database and API usage
5. **Backup Strategy**: Regular database backups

### Docker Deployment (Optional)
A `Dockerfile` can be created for containerized deployment:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["streamlit", "run", "app.py"]
```

## 🆘 Getting Help

If you encounter issues:

1. Check the logs in `nasa_asteroids_explorer.log`
2. Verify your `.env` configuration
3. Test database connectivity
4. Check NASA API status
5. Create an issue on GitHub with detailed error information

## 📝 Next Steps

After successful setup:

1. Explore the Streamlit dashboard at `http://localhost:8501`
2. Try the different features (Dashboard, Quick Queries, Custom Search, Charts)
3. Schedule regular data fetching using cron jobs or task schedulers
4. Customize the application for your specific needs
5. Consider contributing improvements back to the project

## 🔄 Regular Maintenance

### Daily Data Updates
Set up a cron job to fetch new data daily:

```bash
# Add to crontab (crontab -e)
0 2 * * * /path/to/your/venv/bin/python /path/to/NASA-Asteroids-Explorer/data_fetcher/nasa_neo_fetcher.py
```

### Database Maintenance
```sql
-- Optimize tables monthly
OPTIMIZE TABLE asteroids;
OPTIMIZE TABLE close_approaches;

-- Update statistics
ANALYZE TABLE asteroids;
ANALYZE TABLE close_approaches;
```
