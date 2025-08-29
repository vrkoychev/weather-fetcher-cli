# Weather Fetcher CLI

A simple Python command-line application that fetches current weather data for a given city. Built to demonstrate production-ready code practices including logging, error handling, and unit testing.

## Features

- Fetches real weather data from the Open-Meteo API.
- Robust error handling for network issues and invalid inputs.
- Comprehensive logging to both file and console.
- Full unit test suite using `pytest` and `unittest.mock`.

## Installation

1. Clone this repository.
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate` (Linux/macOS) or `.\venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`

## Usage

Run the script from the command line with a city name as an argument:

```bash
python weather_fetcher.py London
python weather_fetcher.py "New York"