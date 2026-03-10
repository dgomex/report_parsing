# Report Parsing Project

This project parses reports using Python.

## Requirements

- Python 3.8 or higher

## Installation

1. **Clone the repository** (if you haven't already):
   ```sh
   git clone <repository-url>
   cd report_parsing
   ```

2. **(Recommended) Create a virtual environment:**
   ```sh
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # Or
   source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

## Running the Project


## Usage

The main script requires a command-line argument to specify the path to the directory containing the report files:

```
python main.py --reports_path <path_to_reports_directory>
```

**Arguments:**

- `--reports_path` (required): Path to the directory where the report files to be processed are located.

**Behavior:**
- The script will process each file in the specified directory using the report parser.
- After processing, each file is moved to a subdirectory called `files_processed` within the same directory.

**Example:**

```
python main.py --reports_path "C:\path\to\your\reports"
```

## Notes
- Make sure you have all required permissions to read/write files as needed by the script.
- For any issues, check the dependencies in `requirements.txt` and ensure your Python version is compatible.
