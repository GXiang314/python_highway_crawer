# Python Highway Crawer

This project is a Python-based crawler for highway information.

## Requirements

- Python 3.8 or higher
- pip3 (package installer for Python)
- Virtual environment (venv)

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
pip3 install -r requirements.txt
```

## Usage

To run the crawler:

```bash
python main.py
```

## Expected Results

After running the crawler successfully, you should see:

1. Console output showing the crawling progress
2. Data saved in the `output` directory (in JSON format by default)
3. Summary of collected data points

## Project Structure

```tree
python_highway_crawer/
├── main.py            # Entry point
├── output/            # Output directory for data
├── requirements.txt   # Dependencies
└── README.md          # This file
```

## Troubleshooting

If you encounter any issues:

1. Ensure you're using the correct Python version
2. Check that all dependencies are installed
3. Verify your internet connection
4. Check the logs for detailed error messages

## License

MIT
