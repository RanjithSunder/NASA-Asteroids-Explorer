# 🚀 NASA Asteroids Explorer

A Streamlit web application for exploring NASA's asteroid database with interactive visualizations and custom search capabilities.

## Features

- 📊 **Dashboard**: Overview of asteroid statistics and key metrics
- 🔍 **Quick Queries**: Pre-built SQL queries for common asteroid data analysis
- 🎯 **Custom Search**: Advanced filtering with multiple parameters
- 📈 **Charts**: Interactive visualizations using Plotly
- 🔄 **Data Fetcher**: Automated NASA API data collection and database population

## Screenshots
📊 **Dashboard**:
![image](https://github.com/user-attachments/assets/ae5e375c-a5e2-4f5c-9cca-5b52a780dc5e)
🔍 **Quick Queries**:
![image](https://github.com/user-attachments/assets/2259498c-e839-4627-9f09-7a5691f5e2a8)
🎯 **Custom Search**:
![image](https://github.com/user-attachments/assets/a2957bda-8674-4a9c-b21d-6b3859c019e2)
📈 **Charts**: 
![image](https://github.com/user-attachments/assets/53eb7f6a-94c7-445b-828e-49906f8b2b3e)

*Dashboard overview with key metrics*

## 🛠️ Prerequisites

- Python 3.8 or higher
- MySQL database server
- NASA API key (free from [NASA API Portal](https://api.nasa.gov/))

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/RanjithSunder/NASA-Asteroids-Explorer.git
   cd NASA-Asteroids-Explorer
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

4. **Database Setup**
   - Install MySQL and create a database named `nasa`
   - Update database credentials in `config.py` or environment variables
   - Import the database schema from `database/schema.sql`

5. **Configure NASA API**
   - Get your free API key from [NASA API Portal](https://api.nasa.gov/)
   - Update the API key in `data_fetcher/nasa_neo_fetcher.py` or use environment variables

6. **Populate Database (Optional)**
   ```bash
   python data_fetcher/nasa_neo_fetcher.py
   ```

7. **Run the application**
   ```bash
   streamlit run app.py
   ```

## ⚙️ Configuration

### Database Configuration
Update the database connection settings in `app.py`:

```python
connection = mysql.connector.connect(
    host="localhost",        # Your database host
    user="your_username",    # Your username
    password="your_password", # Your password
    database="nasa"          # Your database name
)
```

### NASA API Configuration
Update your NASA API key in `data_fetcher/nasa_neo_fetcher.py`:

```python
API_KEY = "your_nasa_api_key_here"
```

## 🗄️ Database Schema

The application expects two main tables:

### `asteroids` table:
- `id` (Primary Key)
- `name`
- `is_potentially_hazardous_asteroid`
- `estimated_diameter_min_km`
- `estimated_diameter_max_km`
- More fields as defined in `database/schema.sql`

### `close_approaches` table:
- `neo_reference_id` (Foreign Key to asteroids.id)
- `close_approach_date`
- `relative_velocity_kmph`
- `astronomical_au`
- `miss_distance_lunar`
- `orbiting_body`
- More fields as defined in `database/schema.sql`

## 🎯 Usage

### Web Application
- **Dashboard**: View overall statistics and metrics
- **Quick Queries**: Run pre-built analyses like:
  - Most frequent asteroid approaches
  - Fastest asteroids
  - Seasonal approach patterns
- **Custom Search**: Filter asteroids by:
  - Date range
  - Velocity
  - Distance (AU and Lunar Distance)
  - Size (diameter)
  - Hazard classification
- **Charts**: Visualize data with interactive plots

### Data Fetcher
The included NASA NEO data fetcher automatically:
- Fetches asteroid data from NASA's NEO API
- Handles API rate limiting and error handling
- Stores data in MySQL database with proper relationships
- Provides comprehensive logging

To run the data fetcher:
```bash
python data_fetcher/nasa_neo_fetcher.py
```

## 📊 Data Source

This application works with NASA's Near Earth Object Web Service (NeoWs) data. The data fetcher automatically retrieves data from:
- [NASA NeoWs API](https://api.nasa.gov/neo/rest/v1/feed)
- [NASA API Documentation](https://cneos.jpl.nasa.gov/about/neo_groups.html)

## 🔧 Project Structure

```
NASA-Asteroids-Explorer/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── config.py                       # Configuration settings
├── data_fetcher/
│   ├── __init__.py
│   └── nasa_neo_fetcher.py        # NASA API data fetcher
├── database/
│   └── schema.sql                 # Database schema
├── utils/
│   └── database_utils.py          # Database utility functions
└── README.md                      # Project documentation
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- NASA for providing asteroid data through their APIs
- Streamlit team for the amazing web framework
- Plotly for interactive visualizations

## 📧 Contact

Ranjith Sunder - [ranjithiam23@gmail.com](mailto:ranjithiam23@gmail.com)

Project Link: [https://github.com/RanjithSunder/NASA-Asteroids-Explorer](https://github.com/RanjithSunder/NASA-Asteroids-Explorer)

## 📝 Changelog

### v2.0.0 (Latest)
- Added automated NASA API data fetcher
- Improved database schema and relationships
- Enhanced error handling and logging
- Added comprehensive configuration options
- Updated documentation with setup instructions

### v1.0.0
- Initial release
- Dashboard with key metrics
- Quick queries functionality
- Custom search with advanced filters
- Interactive charts and visualizations
