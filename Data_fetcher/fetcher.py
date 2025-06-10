"""
NASA Near Earth Objects (NEO) Data Fetcher

This module fetches asteroid data from NASA's NEO API and stores it in a MySQL database.
It includes proper error handling, logging, and database connection management.
"""

import logging
import datetime
import time
from typing import List, Dict, Optional, Tuple
import requests
import mysql.connector
from mysql.connector import Error
from contextlib import contextmanager

# Configuration
API_KEY = "YFIweBiyHPfMZlH2fuXemnidjfnn2GcM9ob7kpVL"
BASE_URL = "https://api.nasa.gov/neo/rest/v1/feed"
TARGET_RECORDS = 10000
REQUEST_DELAY = 1  # seconds between API requests to respect rate limits

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'vmfg',
    'password': 'vmfgpwd!',
    'database': 'nasa'
}

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('nasa_neo_fetcher.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class NASANeoFetcher:
    """Class to handle NASA NEO data fetching and database operations."""

    def __init__(self, api_key: str, db_config: Dict):
        self.api_key = api_key
        self.db_config = db_config
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'NASA-NEO-Fetcher/1.0'})

    def fetch_neo_data(self, start_date: str, end_date: str, target_count: int) -> List[Dict]:
        """
        Fetch NEO data from NASA API.

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            target_count: Number of records to fetch

        Returns:
            List of asteroid dictionaries
        """
        asteroids_data = []
        url = f"{BASE_URL}?start_date={start_date}&end_date={end_date}&api_key={self.api_key}"

        logger.info(f"Starting to fetch {target_count} asteroid records")

        while len(asteroids_data) < target_count:
            try:
                logger.info(f"Fetching data from: {url}")
                response = self.session.get(url, timeout=30)
                response.raise_for_status()

                data = response.json()

                # Check for API errors
                if 'error' in data:
                    logger.error(f"API Error: {data['error']}")
                    break

                # Process asteroid data
                processed_count = self._process_asteroid_batch(
                    data.get('near_earth_objects', {}),
                    asteroids_data,
                    target_count
                )

                logger.info(f"Processed {processed_count} asteroids. Total: {len(asteroids_data)}")

                # Check if we have more data to fetch
                if len(asteroids_data) >= target_count:
                    break

                # Get next page URL
                next_url = data.get('links', {}).get('next')
                if not next_url:
                    logger.warning("No more data available from API")
                    break

                url = next_url
                time.sleep(REQUEST_DELAY)  # Rate limiting

            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed: {e}")
                break
            except KeyError as e:
                logger.error(f"Unexpected API response structure: {e}")
                break
            except Exception as e:
                logger.error(f"Unexpected error during data fetch: {e}")
                break

        logger.info(f"Successfully fetched {len(asteroids_data)} asteroid records")
        return asteroids_data

    def _process_asteroid_batch(self, neo_data: Dict, asteroids_data: List, target_count: int) -> int:
        """Process a batch of asteroid data from API response."""
        processed_count = 0

        for date, ast_details in neo_data.items():
            for ast in ast_details:
                try:
                    asteroid_record = self._parse_asteroid_data(ast)
                    asteroids_data.append(asteroid_record)
                    processed_count += 1

                    if len(asteroids_data) >= target_count:
                        return processed_count

                except Exception as e:
                    logger.warning(f"Failed to parse asteroid {ast.get('id', 'unknown')}: {e}")
                    continue

        return processed_count

    def _parse_asteroid_data(self, ast: Dict) -> Dict:
        """Parse individual asteroid data from API response."""
        try:
            close_approach = ast['close_approach_data'][0]

            return {
                'id': int(ast['id']),
                'neo_id': int(ast['neo_reference_id']),
                'name': ast['name'],
                'abs_magnitude': float(ast['absolute_magnitude_h']),
                'dia_min': float(ast['estimated_diameter']['kilometers']['estimated_diameter_min']),
                'dia_max': float(ast['estimated_diameter']['kilometers']['estimated_diameter_max']),
                'is_potentially_hazardous_asteroid': bool(ast['is_potentially_hazardous_asteroid']),
                'close_approach_date': datetime.datetime.strptime(close_approach['close_approach_date'],
                                                                  '%Y-%m-%d').date(),
                'relative_velocity': float(close_approach['relative_velocity']['kilometers_per_hour']),
                'astronomical': float(close_approach['miss_distance']['astronomical']),
                'miss_distance_lunar': float(close_approach['miss_distance']['lunar']),
                'miss_distance': float(close_approach['miss_distance']['kilometers']),
                'orbiting_body': close_approach['orbiting_body']
            }
        except (KeyError, ValueError, IndexError) as e:
            raise ValueError(f"Invalid asteroid data structure: {e}")

    @contextmanager
    def get_db_connection(self):
        """Context manager for database connections."""
        connection = None
        try:
            connection = mysql.connector.connect(**self.db_config)
            logger.info("Database connection established")
            yield connection
        except Error as e:
            logger.error(f"Database connection failed: {e}")
            raise
        finally:
            if connection and connection.is_connected():
                connection.close()
                logger.info("Database connection closed")

    def insert_asteroid_data(self, asteroids_data: List[Dict]) -> Tuple[int, int]:
        """
        Insert asteroid data into database.

        Returns:
            Tuple of (successful_asteroids, successful_approaches)
        """
        successful_asteroids = 0
        successful_approaches = 0

        with self.get_db_connection() as conn:
            cursor = conn.cursor()

            try:
                # Disable autocommit for batch processing
                conn.autocommit = False

                for i, asteroid in enumerate(asteroids_data):
                    try:
                        # Insert asteroid record
                        asteroid_query = """
                            INSERT IGNORE INTO asteroids (
                                id, name, absolute_magnitude_h,
                                estimated_diameter_min_km, estimated_diameter_max_km,
                                is_potentially_hazardous_asteroid
                            ) VALUES (%s, %s, %s, %s, %s, %s)
                        """
                        cursor.execute(asteroid_query, (
                            asteroid['id'],
                            asteroid['name'],
                            asteroid['abs_magnitude'],
                            asteroid['dia_min'],
                            asteroid['dia_max'],
                            asteroid['is_potentially_hazardous_asteroid']
                        ))

                        if cursor.rowcount > 0:
                            successful_asteroids += 1

                        # Insert close approach record
                        approach_query = """
                            INSERT INTO close_approaches (
                                neo_reference_id, close_approach_date, relative_velocity_kmph,
                                astronomical_au, miss_distance_km, miss_distance_lunar,
                                orbiting_body
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """
                        cursor.execute(approach_query, (
                            asteroid['neo_id'],
                            asteroid['close_approach_date'],
                            asteroid['relative_velocity'],
                            asteroid['astronomical'],
                            asteroid['miss_distance'],
                            asteroid['miss_distance_lunar'],
                            asteroid['orbiting_body']
                        ))

                        if cursor.rowcount > 0:
                            successful_approaches += 1

                        # Commit in batches
                        if (i + 1) % 100 == 0:
                            conn.commit()
                            logger.info(f"Committed batch: {i + 1} records processed")

                    except Error as e:
                        logger.warning(f"Failed to insert asteroid {asteroid['id']}: {e}")
                        continue

                # Final commit
                conn.commit()
                logger.info("All data committed successfully")

            except Exception as e:
                logger.error(f"Database transaction failed: {e}")
                conn.rollback()
                raise
            finally:
                cursor.close()

        return successful_asteroids, successful_approaches


def main():
    """Main execution function."""
    try:
        start_time = time.time()
        # Initialize fetcher
        fetcher = NASANeoFetcher(API_KEY, DB_CONFIG)

        # Fetch data
        start_date = "2024-01-01"
        end_date = "2024-01-07"

        logger.info("Starting NASA NEO data fetch process")
        asteroids_data = fetcher.fetch_neo_data(start_date, end_date, TARGET_RECORDS)

        if not asteroids_data:
            logger.error("No data fetched. Exiting.")
            return

        # Insert into database
        logger.info("Starting database insertion")
        successful_asteroids, successful_approaches = fetcher.insert_asteroid_data(asteroids_data)
        end_time = time.time()
        logger.info(f"Process completed successfully:")
        logger.info(f"- Asteroids inserted: {successful_asteroids}")
        logger.info(f"- Close approaches inserted: {successful_approaches}")
        logger.info(f"Execution time: {end_time - start_time} seconds")
    except Exception as e:
        logger.error(f"Process failed: {e}")
        raise


if __name__ == "__main__":
    main()
