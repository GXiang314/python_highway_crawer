# Taiwan High Speed Rail Timetable Crawler

This project is a Python-based crawler for Taiwan High Speed Rail (THSR) timetable information. It automates the process of retrieving train schedules between stations.

## Demo

![Demo of THSR crawler in action](./docs/demo.gif)

## Requirements

- Python 3.8 or higher
- Chrome browser
- ChromeDriver (compatible with your Chrome version)
- Required Python packages (see `requirements.txt`)

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/python_highway_crawer.git
cd python_highway_crawer
```

### 2. Create and activate virtual environment

#### For Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### For macOS and Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage (Interactive Mode)

Run the script without arguments to use interactive mode:

```bash
python main.py
```

You'll be prompted to:

1. Select a departure station
2. Select an arrival station
3. Enter a date (or press Enter for today)
4. Enter a time (or press Enter for current time)

### Command-Line Options

The script supports several command-line arguments for automated operation:

```bash
python main.py [OPTIONS]
```

#### Available Options

| Option | Description | Default |
|--------|-------------|---------|
| `--all` | Fetch timetables for all possible station combinations | False |
| `--departure STATION` | Specify the departure station name | Interactive selection |
| `--arrival STATION` | Specify the arrival station name | Interactive selection |
| `--startDate YYYY.MM.DD` | Specify the departure date | Current date |
| `--startTime HH:MM` | Specify the departure time | Current time |
| `--format FORMAT` | Specify output format (json, csv) | json |

#### Examples

Fetch timetable for a specific route:

```bash
python main.py --departure "台北" --arrival "左營"
```

Fetch all routes from a specific departure station:

```bash
python main.py --departure "台北"
```

Fetch all routes to a specific arrival station:

```bash
python main.py --arrival "左營"
```

Fetch all possible routes with specific date and time:

```bash
python main.py --all --startDate "2024.05.01" --startTime "08:30"
```

Fetch timetable and save as CSV:

```bash
python main.py --departure "台北" --arrival "左營" --format csv
```

## Output

Data is saved in `.json` or `.csv` format in the `output` directory with a timestamp in the filename:

```tree
output/timetable_YYYYMMDD_HHMMSS.json
```

Each entry includes:

- Departure and arrival stations
- Departure and arrival times
- Travel time
- Train number
- Seat availability information
- Early bird discount information
- Additional remarks

## Limitations

1. The crawler depends on the THSR website structure; changes to their website may break functionality
2. Chrome browser and ChromeDriver must be installed and compatible
3. Internet connection is required
4. Rate limiting may be applied by the THSR website for frequent requests
5. Departure and arrival stations cannot be the same
6. The crawler may encounter issues with popup handling if the website changes

## Project Structure

```tree
python_highway_crawer/
├── main.py            # Main script
├── output/            # Directory for JSON output
├── requirements.txt   # Python dependencies
├── docs/              # Documentation assets
└── README.md          # This file
```

## Troubleshooting

If you encounter any issues:

1. Ensure Chrome and ChromeDriver are properly installed
2. Check that all dependencies are installed correctly
3. Verify your internet connection
4. Ensure the THSR website is accessible
5. Check for website structure changes that might affect the crawler

## License

MIT
