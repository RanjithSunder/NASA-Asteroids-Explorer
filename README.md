# 🪐 NASA Asteroids Explorer

An interactive Streamlit web application for exploring NASA's Near-Earth Object (NEO) asteroid data with comprehensive analytics, visualizations, and custom filtering capabilities.

![NASA Asteroids Explorer](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)

## 🌟 Features

- **📊 Predefined Queries**: 20+ pre-built analyses covering asteroid approaches, velocities, sizes, and hazard classifications
- **🔍 Custom Filters**: Interactive filtering by date range, distance, velocity, size, and hazard status
- **📈 Data Visualizations**: Interactive charts showing approach patterns, velocity distributions, and risk analysis
- **⚡ Real-time Analytics**: Live database queries with exportable results
- **🎯 Hazard Assessment**: Track potentially hazardous asteroids and their approach frequencies

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- MySQL 8.0 or higher
- NASA NEO database (setup instructions below)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/nasa-asteroids-explorer.git
   cd nasa-asteroids-explorer
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup MySQL Database**
   ```bash
   # Create database
   mysql -u root -p
   CREATE DATABASE nasa;
   CREATE USER 'vmfg'@'localhost' IDENTIFIED BY 'vmfgpwd!';
   GRANT ALL PRIVILEGES ON nasa.* TO 'vmfg'@'localhost';
   FLUSH PRIVILEGES;
   ```

5. **Import NASA data** (see Database Setup section)

6. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 🗄️ Database Setup

### Required Tables

The application expects two main tables:

#### `asteroids` table
```sql
CREATE TABLE asteroids (
    id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(255),
    estimated_diameter_min_km DECIMAL(10,6),
    estimated_diameter_max_km DECIMAL(10,6),
    is_potentially_hazardous_asteroid BOOLEAN,
    absolute_magnitude_h DECIMAL(8,4)
);
```

#### `close_approaches` table
```sql
CREATE TABLE close_approaches (
    id INT AUTO_INCREMENT PRIMARY KEY,
    neo_reference_id VARCHAR(20),
    close_approach_date DATE,
    orbiting_body VARCHAR(50),
    relative_velocity_kmph DECIMAL(12,2),
    miss_distance_km DECIMAL(15,2),
    miss_distance_lunar DECIMAL(10,6),
    astronomical_au DECIMAL(12,8),
    FOREIGN KEY (neo_reference_id) REFERENCES asteroids(id)
);
```

### Data Sources

- **NASA NEO API**: https://api.nasa.gov/neo/
- **JPL Small-Body Database**: https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html

## 🔧 Configuration

Update database credentials in `app.py`:

```python
def get_connection():
    return mysql.connector.connect(
        host="your_host",
        user="your_username", 
        password="your_password",
        database="your_database"
    )
```

For production, use environment variables:

```python
import os

def get_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'vmfg'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME', 'nasa')
    )
```

## 📊 Available Analyses

### Predefined Queries
- Asteroid approach frequency analysis
- Velocity and size distributions  
- Potentially hazardous asteroid tracking
- Seasonal approach patterns
- Distance and timing analysis

### Custom Filtering
- Date range selection
- Distance thresholds (AU, Lunar Distance)
- Velocity ranges
- Size parameters
- Hazard classification

### Visualizations
- Monthly approach frequency
- Velocity distribution histograms
- Distance vs velocity scatter plots
- Hazard classification pie charts

## 🛠️ Development

### Project Structure
```
nasa-asteroids-explorer/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── LICENSE            # MIT License
├── .gitignore         # Git ignore rules
├── config/
│   └── database.sql   # Database schema
├── data/
│   └── sample_data.sql # Sample data for testing
└── docs/
    └── screenshots/   # Application screenshots
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 Usage Examples

### Basic Query Execution
```python
# Execute predefined query
selected_query = "🔢 Count how many times each asteroid has approached Earth"
execute_query(queries[selected_query]['query'], selected_query)
```

### Custom Filtering
```python
# Apply custom filters
filter_query = build_filter_query(
    start_date=date(2024, 1, 1),
    end_date=date(2024, 12, 31),
    au=(0.0, 0.05),
    velocity=(0.0, 75000.0)
)
```

## 🐛 Troubleshooting

### Common Issues

**Database Connection Error**
- Verify MySQL is running
- Check credentials in connection function
- Ensure database and tables exist

**No Data Displayed**
- Confirm data import was successful
- Check table relationships and foreign keys
- Verify date formats in database

**Performance Issues**
- Add indexes on frequently queried columns
- Limit result sets for large datasets
- Consider pagination for large queries

## 📈 Performance Optimization

### Recommended Indexes
```sql
-- Optimize common queries
CREATE INDEX idx_close_approach_date ON close_approaches(close_approach_date);
CREATE INDEX idx_orbiting_body ON close_approaches(orbiting_body);
CREATE INDEX idx_velocity ON close_approaches(relative_velocity_kmph);
CREATE INDEX idx_miss_distance ON close_approaches(miss_distance_km);
CREATE INDEX idx_hazardous ON asteroids(is_potentially_hazardous_asteroid);
```

## 🔒 Security Notes

- Never commit database credentials to version control
- Use environment variables for sensitive configuration
- Implement proper input validation for custom queries
- Consider using connection pooling for production deployments

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **NASA** for providing comprehensive NEO data through their APIs
- **JPL** for asteroid orbital data and research
- **Streamlit** for the excellent web app framework
- **Plotly** for interactive visualizations

## 📞 Support

- Create an [Issue](https://github.com/yourusername/nasa-asteroids-explorer/issues) for bug reports
- Start a [Discussion](https://github.com/yourusername/nasa-asteroids-explorer/discussions) for questions
- Follow the project for updates

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Docker Deployment
```bash
docker build -t nasa-asteroids-explorer .
docker run -p 8501:8501 nasa-asteroids-explorer
```

### Cloud Deployment
- **Streamlit Cloud**: Connect your GitHub repo directly
- **Heroku**: Use the included Procfile
- **AWS/GCP**: Deploy using container services

---

⭐ **Star this repository if you find it useful!**
