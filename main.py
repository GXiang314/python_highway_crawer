from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os
from datetime import datetime
import argparse


def setup_driver():
    """Initialize and return the webdriver"""
    return webdriver.Chrome()


def get_stations(driver: Chrome):
    """Extract departure and arrival stations from the webpage"""
    # Find the lists of departure and arrival stations
    departure_stations = []
    arrival_stations = []

    # Get departure stations
    departure_options = driver.find_elements(
        By.CSS_SELECTOR, 'select#select_location01 option')
    for option in departure_options:
        departure_stations.append(option.text.strip())

    # Get arrival stations
    arrival_options = driver.find_elements(
        By.CSS_SELECTOR, 'select#select_location02 option')
    for option in arrival_options:
        arrival_stations.append(option.text.strip())

    return {
        'departure_stations': departure_stations,
        'arrival_stations': arrival_stations
    }


def extract_timetable(driver: Chrome):
    """Extract timetable data from the current page"""
    timetable_data = []
    current_elements = []

    while True:
        timestableBlock = driver.find_element(By.CSS_SELECTOR, 'div#ttab-01')
        
        wait = WebDriverWait(timestableBlock, timeout=3)
        wait.until(
            lambda d: d.find_elements(By.TAG_NAME, 'a') != current_elements
        )
        current_elements = timestableBlock.find_elements(By.TAG_NAME, 'a')

        departureStation = timestableBlock.find_element(
            By.CSS_SELECTOR, '.from').text.strip()
        arrivalStation = timestableBlock.find_element(
            By.CSS_SELECTOR, '.to').text.strip()

        # Extract the timetable data
        for row in current_elements:
            columns = row.find_elements(By.CSS_SELECTOR, 'div.tr-td')
            if len(columns) == 0:
                continue
                
            # Skip if this data-seq already exists in timetable_data
            data_seq = row.get_attribute('data-seq')
            if any(item.get('data-seq') == data_seq for item in timetable_data):
                continue
                
            timetable_data.append({
                "data-seq": data_seq,
                "departureStation": departureStation,
                "arrivalStation": arrivalStation,
                'startTime': columns[0].text.strip(),
                'travelTime': columns[1].text.strip(),
                'arriveTime': columns[2].text.strip(),
                'trainNo': columns[3].text.strip(),
                'freeSeat': columns[4].text.strip(),
                'earlyBird': columns[5].text.strip(),
                'remark': columns[6].text.strip()
            })
        
        nextBtn = driver.find_element(By.CSS_SELECTOR, 'a#ttab-01_nextPage')
        if ('visibility: hidden' in nextBtn.get_attribute('style')):
            break
        nextBtn.click()
    
    print(f"Total timetable data: {len(timetable_data)}")
    return timetable_data


def get_timetable(driver: Chrome, departure_station, arrival_station, start_date, start_time):
    """Get timetable for specific stations and time"""
    print(f"Searching for trains from {departure_station} to {arrival_station}")
    print(f"Date: {start_date}, Time: {start_time}")
    
    # Set date and time
    start_date_input = driver.find_element(By.CSS_SELECTOR, 'input#Departdate03')
    start_time_input = driver.find_element(By.CSS_SELECTOR, 'input#outWardTime')
    
    # Use JavaScript to set input values
    driver.execute_script(f"arguments[0].value = '{start_date}'", start_date_input)
    driver.execute_script(f"arguments[0].value = '{start_time}'", start_time_input)

    # Select departure and arrival stations
    departure_select = driver.find_element(By.CSS_SELECTOR, 'select#select_location01')
    arrival_select = driver.find_element(By.CSS_SELECTOR, 'select#select_location02')
    
    departure_option = departure_select.find_element(By.XPATH, f"option[text()='{departure_station}']")
    departure_option.click()
    
    arrival_option = arrival_select.find_element(By.XPATH, f"option[text()='{arrival_station}']")
    arrival_option.click()
    
    # Click the search button
    search_button = driver.find_element(By.CSS_SELECTOR, 'button#start-search')
    search_button.click()

    # Wait for search results to load
    wait = WebDriverWait(driver, timeout=10)
    wait.until(
        lambda d: d.find_element(
            By.CSS_SELECTOR, 'div#search-loading').get_attribute('style') == 'display: none;'
    )
    
    # Extract timetable data
    return extract_timetable(driver)


def save_to_json(data, filename):
    """Save data to a JSON file"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(current_dir, 'output', filename)

    # Ensure the output directory exists
    os.makedirs(os.path.join(current_dir, 'output'), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    return output_path


def display_stations(stations):
    """Display stations for user to select from"""
    print("\n=== Available Stations ===")
    for i, station in enumerate(stations, 1):
        print(f"{i}: {station}")
    print("=========================\n")


def get_user_input(stations, default_station=None):
    """Get user input for station selection with default option"""
    if default_station:
        default_index = stations.index(default_station) + 1 if default_station in stations else None
        prompt = f"Enter station number (press Enter for default - {default_station}): "
    else:
        default_index = None
        prompt = "Enter station number: "
    
    while True:
        choice = input(prompt)
        if choice == "" and default_index:
            return stations[default_index - 1]
        try:
            choice = int(choice)
            if 1 <= choice <= len(stations):
                return stations[choice - 1]
            else:
                print(f"Please enter a number between 1 and {len(stations)}")
        except ValueError:
            print("Please enter a valid number")


def validate_date(date_str):
    """Validate date string in YYYY.MM.DD format"""
    try:
        datetime.strptime(date_str, '%Y.%m.%d')
        return True
    except ValueError:
        return False


def validate_time(time_str):
    """Validate time string in HH:MM format"""
    try:
        datetime.strptime(time_str, '%H:%M')
        return True
    except ValueError:
        return False


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Taiwan High Speed Rail Timetable Crawler')
    parser.add_argument('--all', action='store_true', help='Fetch timetables for all departure and arrival stations')
    parser.add_argument('--departure', type=str, help='Departure station name')
    parser.add_argument('--arrival', type=str, help='Arrival station name')
    parser.add_argument('--startDate', type=str, help='Start date in YYYY.MM.DD format')
    parser.add_argument('--startTime', type=str, help='Start time in HH:MM format')
    
    return parser.parse_args()


def main():
    """Main function to orchestrate the web scraping process"""
    url = 'https://www.thsrc.com.tw/ArticleContent/a3b630bb-1066-4352-a1ef-58c7b4e8ef7c'

    # Set default values
    default_date = datetime.now().strftime('%Y.%m.%d')
    default_time = datetime.now().strftime('%H:%M')
    
    # Parse command line arguments
    args = parse_args()
    
    try:
        print("Initializing web driver...")
        driver = setup_driver()
        driver.get(url)
        
        # Handle popup if appears
        try:
            wait = WebDriverWait(driver, timeout=5)
            cancel_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.swal2-cancel.swal2-styled'))
            )
            cancel_button.click()
        except:
            print("No popup found or it couldn't be closed.")
        
        print("Getting available stations...")
        stations_data = get_stations(driver)
        
        # Set date and time
        start_date = args.startDate if args.startDate and validate_date(args.startDate) else default_date
        start_time = args.startTime if args.startTime and validate_time(args.startTime) else default_time

        all_results = []
        
        # Handle different command line option scenarios
        if args.all:
            # Process all departures and all arrivals
            print("Processing all departure and arrival stations...")
            for dep_station in stations_data['departure_stations']:
                for arr_station in stations_data['arrival_stations']:
                    if dep_station != arr_station:  # Skip same departure and arrival
                        try:
                            result = get_timetable(driver, dep_station, arr_station, start_date, start_time)
                            all_results.extend(result)
                        except Exception as e:
                            print(f"Error processing {dep_station} to {arr_station}: {str(e)}")
        
        elif args.departure and not args.arrival:
            # Process specified departure to all arrivals
            if args.departure not in stations_data['departure_stations']:
                print(f"Error: Departure station '{args.departure}' not found.")
                display_stations(stations_data['departure_stations'])
                return
                
            print(f"Processing departure from {args.departure} to all arrivals...")
            for arr_station in stations_data['arrival_stations']:
                if args.departure != arr_station:  # Skip same departure and arrival
                    try:
                        result = get_timetable(driver, args.departure, arr_station, start_date, start_time)
                        all_results.extend(result)
                    except Exception as e:
                        print(f"Error processing {args.departure} to {arr_station}: {str(e)}")
        
        elif args.arrival and not args.departure:
            # Process all departures to specified arrival
            if args.arrival not in stations_data['arrival_stations']:
                print(f"Error: Arrival station '{args.arrival}' not found.")
                display_stations(stations_data['arrival_stations'])
                return
                
            print(f"Processing all departures to {args.arrival}...")
            for dep_station in stations_data['departure_stations']:
                if dep_station != args.arrival:  # Skip same departure and arrival
                    try:
                        result = get_timetable(driver, dep_station, args.arrival, start_date, start_time)
                        all_results.extend(result)
                    except Exception as e:
                        print(f"Error processing {dep_station} to {args.arrival}: {str(e)}")
        
        elif args.departure and args.arrival:
            # Process specific departure to specific arrival
            if args.departure not in stations_data['departure_stations']:
                print(f"Error: Departure station '{args.departure}' not found.")
                display_stations(stations_data['departure_stations'])
                return
                
            if args.arrival not in stations_data['arrival_stations']:
                print(f"Error: Arrival station '{args.arrival}' not found.")
                display_stations(stations_data['arrival_stations'])
                return
                
            if args.departure == args.arrival:
                print("Error: Departure and arrival stations cannot be the same.")
                return
                
            print(f"Processing {args.departure} to {args.arrival}...")
            result = get_timetable(driver, args.departure, args.arrival, start_date, start_time)
            all_results.extend(result)
        
        else:
            # Interactive mode if no command line options specified
            # Display departure stations and get user selection with default
            default_departure = stations_data['departure_stations'][0]
            print(f"\nSelect departure station (default: {default_departure}):")
            display_stations(stations_data['departure_stations'])
            departure_station = get_user_input(stations_data['departure_stations'], default_departure)
            
            # Display arrival stations and get user selection with default
            default_arrival = stations_data['arrival_stations'][-1]
            print(f"\nSelect arrival station (default: {default_arrival}):")
            display_stations(stations_data['arrival_stations'])
            arrival_station = get_user_input(stations_data['arrival_stations'], default_arrival)
            
            # Validate departure and arrival stations aren't the same
            while departure_station == arrival_station:
                print("Departure and arrival stations cannot be the same. Please select a different arrival station.")
                print("\nSelect arrival station:")
                display_stations(stations_data['arrival_stations'])
                arrival_station = get_user_input(stations_data['arrival_stations'])
            
            # Get date from user with default
            while True:
                start_date = input(f"\nEnter departure date (YYYY.MM.DD) (press Enter for today - {default_date}): ")
                if start_date == "":
                    start_date = default_date
                    break
                if validate_date(start_date):
                    break
                print("Invalid date format. Please use YYYY.MM.DD format.")
            
            # Get time from user with default
            while True:
                start_time = input(f"Enter departure time (HH:MM) (press Enter for current time - {default_time}): ")
                if start_time == "":
                    start_time = default_time
                    break
                if validate_time(start_time):
                    break
                print("Invalid time format. Please use HH:MM format.")
            
            # Get timetable data for single selection
            result = get_timetable(driver, departure_station, arrival_station, start_date, start_time)
            all_results.extend(result)
        
        # Save all results to file
        if all_results:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"timetable_{timestamp}.json"
            output_path = save_to_json(all_results, filename)
            print(f"\nData has been successfully written to {output_path}")
            print(f"Total records: {len(all_results)}")
        else:
            print("No data was collected.")
            
    finally:
        # Ensure driver is closed even if an error occurs
        if 'driver' in locals():
            driver.quit()


if __name__ == "__main__":
    main()
