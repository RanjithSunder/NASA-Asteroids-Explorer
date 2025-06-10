"""
Configuration file for NASA Asteroids Explorer

This file contains all configuration settings for the application.
Use environment variables to override these settings in production.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# NASA API Configuration
NASA_API_KEY = os.getenv('NASA_API_KEY', 'DEMO_KEY')
NASA_BASE_URL = "https://api.nasa.gov/neo/rest/v1/feed"

# Database Configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'nasa'),
    'port': int(os.getenv('DB_PORT', 3306))
}

# Data Fetcher Configuration
FETCHER_CONFIG = {
    'target_records': int(os.getenv('TARGET_RECORDS', 10000)),
    'request_delay': float(os.getenv('REQUEST_DELAY', 1.0)),  # seconds
    'batch_size': int(os.getenv('BATCH_SIZE', 100)),
    'log_level': os.getenv('LOG_LEVEL', 'INFO')
}

# Streamlit Configuration
STREAMLIT_CONFIG = {
    'page_title': "NASA Asteroids Explorer",
    'page_icon': "🌌",
    'layout': "wide",
    'initial_sidebar_state': "expanded"
}

# Logging Configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'nasa_asteroids_explorer.log',
            'formatter': 'default',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'loggers': {
        '': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Application Constants
DEFAULT_DATE_RANGE = {
    'start_date': '2024-01-01',
    'end_date': '2024-12-31'
}

# Chart Configuration
CHART_CONFIG = {
    'template': 'plotly_white',
    'color_palette': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'],
    'height': 400,
    'margin': {'l': 50, 'r': 50, 't': 50, 'b': 50}
}
