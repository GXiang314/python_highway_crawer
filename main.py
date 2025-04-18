from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import time
import os

def setup_driver():
    """Initialize and return the webdriver"""
    return webdriver.Chrome()

def get_stations(driver, url):
    """Extract departure and arrival stations from the webpage"""
    # Open the webpage
    driver.get(url)

    # Wait for the page to load
    time.sleep(3)  # Adjust waiting time according to the page loading speed

    # Find the lists of departure and arrival stations
    departure_stations = []
    arrival_stations = []

    # Get departure stations
    departure_options = driver.find_elements(By.CSS_SELECTOR, 'select#select_location01 option')
    for option in departure_options:
        departure_stations.append(option.text.strip())

    # Get arrival stations
    arrival_options = driver.find_elements(By.CSS_SELECTOR, 'select#select_location02 option')
    for option in arrival_options:
        arrival_stations.append(option.text.strip())

    return {
        'departure_stations': departure_stations,
        'arrival_stations': arrival_stations
    }

def save_to_json(data, filename):
    """Save data to a JSON file"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(current_dir, 'output', filename)
    
    # Ensure the output directory exists
    os.makedirs(os.path.join(current_dir, 'output'), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    
    return output_path

def main():
    """Main function to orchestrate the web scraping process"""
    url = 'https://www.thsrc.com.tw/ArticleContent/a3b630bb-1066-4352-a1ef-58c7b4e8ef7c'
    
    try:
        driver = setup_driver()
        stations = get_stations(driver, url)
        output_path = save_to_json(stations, 'stations_selenium.json')
        print(f"Data has been successfully written to {output_path}")
    finally:
        # Ensure driver is closed even if an error occurs
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    main()
