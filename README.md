# NASA Earth Data Downloader

An AI agent skill for downloading data from NASA Earth Data, specifically designed for MODIS and other NASA Earth science datasets. This project was developed and tested within the TRAE IDE (trae.cn).

## Why This Skill 

When working with science data, I often need to download **long time-series datasets** spanning multiple years or decades. These datasets can be extremely large, with individual files ranging from tens to hundreds of megabytes, and complete time-series requiring dozens or even hundreds of files.

## Features

• Multi-threaded downloads: Increases download speed by using multiple concurrent threads (default: 5 threads)

• Resumable downloads: Continues from where it left off if download is interrupted

• NASA Earth Data authentication: Uses .netrc file for NASA Earth Data login credentials

• File existence check: Automatically skips already downloaded files

• Progress bars: Shows real-time download progress for each file


• Batch download support: Download multiple files in a single command

• TRAE terminal compatible: Works seamlessly in TRAE IDE terminal environment


## Installation

### Method 1: Direct Installation

1. Download or clone this repository
2. Extract or copy the `nasa-earthdata-downloader` folder to your `.trae/skills/` directory
3. Ensure dependencies are installed:
   ```bash
   pip install requests tqdm
   ```

### Method 2: Using TRAE IDE

1. Open TRAE IDE
2. Go to Skills Manager
3. Upload the `nasa-earthdata-downloader.zip` file
4. Follow the installation prompts

### Directory Structure

After installation, your `.trae/skills/` directory should contain:

```
.trae/skills/
└── nasa-earthdata-downloader/
    ├── scripts/              # Python scripts directory
    │   ├── __init__.py       # Python package initialization
    │   ├── downloader.py     # Core download functionality
    │   └── skill.py          # Main skill entry point
    ├── SKILL.md              # Detailed skill documentation
    └── README.md             # This file
```

## Configuration

### NASA Earth Data Account Setup

1. Create an account at https://urs.earthdata.nasa.gov/users/new
2. Configure .netrc file with your credentials:

Windows: Create `C:\Users\YourUsername\.netrc`
```
machine urs.earthdata.nasa.gov
login your_username
password your_password
```

Linux/Mac: Create `~/.netrc`
```
machine urs.earthdata.nasa.gov
login your_username
password your_password
```

3. Set file permissions (Linux/Mac only):
   ```bash
   chmod 600 ~/.netrc
   ```

### Dependencies

• Python 3.6+

• requests (HTTP library)

• tqdm (Progress bar library)


Install dependencies:
```bash
pip install requests tqdm
```

## Usage

### Basic Usage in TRAE Terminal

Execute skill with multiple files:

```powershell
D:\software\anaconda\envs\geo_env\python.exe -c "
import sys
import os
skill_path = os.path.join('.trae', 'skills', 'nasa-earthdata-downloader')
sys.path.insert(0, skill_path)
from skill import run_skill
result = run_skill({
    'save_dir': r'D:\ndvi\hdf',
    'urls': '''
    https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/MOD13Q1.061/MOD13Q1.A2023161.h29v09.061.2023177233537/MOD13Q1.A2023161.h29v09.061.2023177233537.hdf
    https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/MOD13Q1.061/MOD13Q1.A2024161.h29v09.061.2024181211247/MOD13Q1.A2024161.h29v09.061.2024181211247.hdf
    '''
})
print('Result:', result)
"
```

### Parameters

• save_dir (required): Directory path where downloaded files will be saved

• urls (required): Single URL string or multiple URLs (separated by newlines)

• max_threads (optional): Number of concurrent download threads (default: 5)

• chunk_size (optional): Download chunk size in bytes (default: 1MB)


## Example Output

```
=====================================
     NASA Earth Data Downloader
=====================================
Processing dictionary input...
Save directory: D:\ndvi\hdf
Found 1 download URLs
- https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/MOD13Q1.061/MOD13Q1.A2023161.h29v09.061.2023177233537/MOD13Q1.A2023161.h29v09.061.2023177233537.hdf
Preparing to download 1 file to directory: D:\ndvi\hdf
MOD13Q1.A2023161.h29...: 100%|█████████████| 92.7M/92.7M [00:05<00:00, 15.6MB/s]

Download completed!
Success: 1, Failed: 0, Skipped: 0
Files saved to: D:\ndvi\hdf

Result: success
Message: Download completed! Success: 1, Failed: 0, Skipped: 0
=====================================
```

## Supported Data

This skill supports downloading from NASA Earth Data Cloud.



