---
name: nasa-earthdata-downloader
description:'Triggered when users need to download earthdata scientific data, such as when users provide links like https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/MOD13A1.061/MOD13A1.A2015225.h29v09.061.2021331155049/MOD13A1.A2015225.h29v09.061.2021331155049.hdf'
---


# nasa-earthdata-downloader

**Description:** A skill for downloading data from NASA Earth Data, specifically designed for MODIS and other NASA datasets. Supports batch downloading with multi-threading, resumable downloads, and NASA Earth Data authentication.

**Details:**

## When to Use

Use this skill when you need to:
- Download NASA Earth Data products
- Batch download multiple files from NASA Earth Data Cloud
- Resume interrupted downloads
- Download data with NASA Earth Data authentication

## How to Use

To use this skill, provide the following information:

1. **Save directory**: The local directory where you want to save the downloaded files
2. **Download URLs**: One or more URLs from NASA Earth Data Cloud
3. **Optional parameters**:
   - `max_threads`: Number of concurrent download threads (default: 5)
   - `chunk_size`: Download chunk size in bytes (default: 1MB)

## Example Usage

### Example 1: Interactive Dialog with Natural Language

**User Input:**
```
Help me download "https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/MOD13A1.061/MOD13A1.A2015225.h29v09.061.2021331155049/MOD13A1.A2015225.h29v09.061.2021331155049.hdfhttps://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/MOD13A1.061/MOD13A1.A2015241.h29v09.061.2021331193012/MOD13A1.A2015241.h29v09.061.2021331193012.hdf"
```

**AI Response:**
```
Detected two NASA Earth Data download links, starting nasa-earthdata-downloader skill.

=====================================
     NASA Earth Data Download Skill
=====================================
Detected 2 download links:
- https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/MOD13A1.061/MOD13A1.A2015225.h29v09.061.2021331155049/MOD13A1.A2015225.h29v09.061.2021331155049.hdf
- https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/MOD13A1.061/MOD13A1.A2015241.h29v09.061.2021331193012/MOD13A1.A2015241.h29v09.061.2021331193012.hdf

Please provide save directory (e.g., D:\ndvi\hdf):
```

**User Input:**
```
D:\ndvi\hdf
```

**AI Response:**
```
Save directory set to: D:\ndvi\hdf

Please set download thread count (default: 5):
```

**User Input:**
```
default
```

**AI Response:**
```
Thread count set to: 5

Preparing to download 2 files to directory: D:\ndvi\hdf

MOD13A1.A2015225.h29...: 100%|█████████████| 92.7M/92.7M [00:06<00:00, 14.8MB/s]
MOD13A1.A2015241.h29...: 100%|█████████████| 92.7M/92.7M [00:06<00:00, 14.9MB/s]

Download completed!
Success: 2, Failed: 0, Skipped: 0
Files saved to: D:\ndvi\hdf
```

## Execution Logic

### How the Skill Works Internally

When requested to download files using this skill, the following process is executed:

1. **Command Construction**: The system builds a Python command to run the downloader
2. **Environment Setup**: Uses the user's Python environment
3. **Path Configuration**: Adds the skill script path to Python's search path
4. **Skill Execution**: Calls the `run_skill` function with your parameters
5. **Download Process**: Handles multi-threaded downloading and error handling

```powershell
# Activate user's Python environment
conda activate geo_env  # Or use your preferred environment, this is only an example

# Run the downloader
python -c "
import sys
import os
from scripts.skill import run_skill

result = run_skill({
    'save_dir': 'path/to/save',
    'urls': ['https://example.com/file1.hdf', 'https://example.com/file2.hdf']
})
print('Result:', result)
"
```

### Execution Flow

1. **Parameter Validation**: Checks required parameters (save directory, URLs)
2. **Directory Preparation**: Ensures the save directory exists
3. **URL Processing**: Parses and validates download URLs
4. **Multi-threaded Download**: Starts concurrent download threads
5. **Progress Tracking**: Shows real-time download progress
6. **Result Compilation**: Collects and displays download results


## Technical Requirements

- **NASA Earth Data account**: You need to have a NASA Earth Data account and store your credentials in a .netrc file
- **Dependencies**: Python 3.6+, requests, tqdm

## Setup Instructions

1. **Create NASA Earth Data account**: Register at https://urs.earthdata.nasa.gov/users/new
2. **Configure .netrc file**: Add your NASA Earth Data credentials to your .netrc file:
   ```
   machine urs.earthdata.nasa.gov
   login your_username
   password your_password
   ```
3. **Install dependencies**: Ensure requests and tqdm are installed

## Troubleshooting

- **Authentication errors**: Check your .netrc file for correct NASA Earth Data credentials
- **Download failures**: Ensure you have a stable internet connection and sufficient disk space
- **File not found errors**: Verify the URLs are correct and accessible with your NASA Earth Data account

## References

For detailed analysis and troubleshooting steps when executing this skill in Trae terminal environment, refer to:

- `reference\Trae_Terminal_Python_Issue_Analysis.md` 


## Scripts
.trae\skills\nasa-earthdata-downloader\scripts\downloader.py
- `scripts/downloader.py` - downloader script
- `scripts/skill.py` - skill script



