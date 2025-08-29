import requests
import argparse
import logging
import sys
from typing import Optional, Dict, Any

# Configure logging
# This will write logs to a file and also print them to the console (stream)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("weather_fetcher.log"),  # Log to file
        logging.StreamHandler(sys.stdout)            # Also print to console
    ]
)
logger = logging.getLogger(__name__)

def get_coordinates_for_city(city_name: str) -> Optional[Dict[str, float]]:
    """
    Fetches latitude and longitude for a given city name using Open-Meteo's geocoding API.

    Args:
        city_name (str): The name of the city to geocode.

    Returns:
        Optional[Dict]: A dictionary with 'latitude' and 'longitude' if successful, None otherwise.
    """
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city_name, "count": 1}
    
    try:
        logger.info(f"Attempting to geocode city: {city_name}")
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad status codes (4xx, 5xx)
        
        data = response.json()
        if not data.get('results'):
            logger.error(f"City '{city_name}' not found.")
            return None
            
        result = data['results'][0]
        coordinates = {
            "latitude": result['latitude'],
            "longitude": result['longitude']
        }
        logger.info(f"Found coordinates for {city_name}: {coordinates}")
        return coordinates
        
    except requests.exceptions.RequestException as e:
        # This catches network errors, timeouts, and HTTP errors
        logger.error(f"Network/HTTP error occurred during geocoding: {e}")
        return None
    except (KeyError, IndexError) as e:
        logger.error(f"Unexpected API response structure: {e}")
        return None
    
def get_current_weather(latitude: float, longitude: float) -> Optional[Dict[str, Any]]:
    """
    Fetches current weather data for given coordinates.

    Args:
        latitude (float): The latitude of the location.
        longitude (float): The longitude of the location.

    Returns:
        Optional[Dict]: The current weather data dictionary if successful, None otherwise.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True
    }
    
    try:
        logger.info(f"Fetching weather for coordinates: {latitude}, {longitude}")
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        return data.get('current_weather')
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Network/HTTP error occurred during weather fetch: {e}")
        return None
    except (KeyError, ValueError) as e:
        logger.error(f"Unexpected API response structure or JSON decode error: {e}")
        return None

def main():
    """Main function to run the CLI application."""
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Fetch the current weather for a city.")
    parser.add_argument("city", type=str, help="Name of the city to get weather for")
    args = parser.parse_args()
    
    city_name = args.city
    logger.info(f"Weather Fetcher started for city: {city_name}")
    
    # 1. Get Coordinates
    coordinates = get_coordinates_for_city(city_name)
    if not coordinates:
        logger.critical(f"Failed to get coordinates for '{city_name}'. Exiting.")
        sys.exit(1) # Exit with an error code
        
    # 2. Get Weather
    weather_data = get_current_weather(coordinates['latitude'], coordinates['longitude'])
    if not weather_data:
        logger.critical(f"Failed to get weather data for '{city_name}'. Exiting.")
        sys.exit(1)
        
    # 3. Display Results
    print(f"\nCurrent Weather in {city_name}:")
    print(f"Temperature: {weather_data['temperature']}°C")
    print(f"Wind Speed: {weather_data['windspeed']} km/h")
    print(f"Wind Direction: {weather_data['winddirection']}°")
    print(f"Weather Code: {weather_data['weathercode']} (see API docs for meaning)")
    logger.info("Weather data successfully displayed. Exiting.")

# This if statement ensures main() only runs when the script is executed directly,
# not when it's imported as a module (e.g., during testing)
if __name__ == "__main__":
    main()