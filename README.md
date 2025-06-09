# 🚀 NASA Asteroids Explorer

A Streamlit web application for exploring NASA's asteroid database with interactive visualizations and custom search capabilities.

## Features

- 📊 **Dashboard**: Overview of asteroid statistics and key metrics
- 🔍 **Quick Queries**: Pre-built SQL queries for common asteroid data analysis
- 🎯 **Custom Search**: Advanced filtering with multiple parameters
- 📈 **Charts**: Interactive visualizations using Plotly

## Screenshots

![Dashboard](docs/images/dashboard.png)
*Dashboard overview with key metrics*

## Prerequisites

- Python 3.8 or higher
- MySQL database server
- NASA asteroid data (instructions below)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/nasa-asteroids-app.git
   cd nasa-asteroids-app
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
   - Update database credentials in `app.py` (lines 45-50)
   - Import the database schema from `database/schema.sql`
   - Load your NASA asteroid data

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

## Database Configuration

Update the database connection settings in `app.py`:

```python
connection = mysql.connector.connect(
    host="localhost",      # Your database host
    user="your_username",  # Your username
    password="your_password",  # Your password
    database="nasa"        # Your database name
)
```

## Database Schema

The application expects two main tables:

### asteroids table
- `id` (Primary Key)
- `name`
- `is_potentially_hazardous_asteroid`
- `estimated_diameter_min_km`
- `estimated_diameter_max_km`

### close_approaches table
- `neo_reference_id` (Foreign Key to asteroids.id)
- `close_approach_date`
- `relative_velocity_kmph`
- `astronomical_au`
- `miss_distance_lunar`
- `orbiting_body`

## Usage

1. **Dashboard**: View overall statistics and metrics
2. **Quick Queries**: Run pre-built analyses like:
   - Most frequent asteroid approaches
   - Fastest asteroids
   - Seasonal approach patterns
3. **Custom Search**: Filter asteroids by:
   - Date range
   - Velocity
   - Distance (AU and Lunar Distance)
   - Size (diameter)
   - Hazard classification
4. **Charts**: Visualize data with interactive plots

## Data Sources

This application is designed to work with NASA's Near Earth Object Web Service (NeoWs) data. You can obtain asteroid data from:
- [NASA NeoWs API](https://api.nasa.gov/)
- [NASA JPL Small-Body Database](https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- NASA for providing asteroid data through their APIs
- Streamlit team for the amazing web framework
- Plotly for interactive visualizations

## Contact

Your Name - ranjithiam23@gmail.com
Project Link: [https://github.com/RanjithSunder/NASA-Asteroids-Explorer]

## Changelog

### v1.0.0 (2024-06-09)
- Initial release
- Dashboard with key metrics
- Quick queries functionality
- Custom search with advanced filters
- Interactive charts and visualizations
