import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'vmfg'),
    'password': os.getenv('DB_PASSWORD', 'vmfgpwd!'),
    'database': os.getenv('DB_NAME', 'nasa')
}

# App configuration
APP_TITLE = "NASA Asteroids Explorer"
APP_ICON = "🚀"
