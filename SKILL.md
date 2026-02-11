---
name: nasa-earthdata-downloader
description: Triggered when you provide earthdata download links
---

---
name: nasa-earthdata-downloader
description: "Triggered when users need to download earthdata scientific data, such as when users provide links like https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/MOD13A1.061/MOD13A1.A2015225.h29v09.061.2021331155049/MOD13A1.A2015225.h29v09.061.2021331155049.hdf
---

# nasa-earthdata-downloader

**Description:** A skill for downloading data from NASA Earth Data, specifically designed for MODIS and other NASA datasets. Supports batch downloading with multi-threading, resumable downloads, and NASA Earth Data authentication.

**Details:**

## When to Use

Use this skill when you need to:
- Download MODIS NDVI data or other NASA Earth Data products
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

### Example 1: Download MODIS NDVI data

```python
# Example: Download MODIS NDVI data
save_dir = r"D:\Study\毕业论文\data\ndvi"
download_urls = [
    "https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/MOD13A1.061/MOD13A1.A2015225.h29v09.061.2021331155049/MOD13A1.A2015225.h29v09.061.2021331155049.hdf",
    "https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/MOD13A1.061/MOD13A1.A2015241.h29v09.061.2021331193012/MOD13A1.A2015241.h29v09.061.2021331193012.hdf"
]

# Call the download function with the provided parameters
download_files(download_urls, save_dir, max_threads=5)
```

### Example 2: Execute Skill in Trae Terminal (geo_env)

**Command:**

```powershell
D:\software\anaconda\envs\geo_env\python.exe -c "
import sys
import os
skill_path = os.path.join('.trae', 'skills', 'nasa-earthdata-downloader')
sys.path.insert(0, skill_path)
from skill import run_skill
result = run_skill({
    'save_dir': r'D:\ndvi\hdf',
    'urls': 'https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/MOD13Q1.061/MOD13Q1.A2024161.h29v09.061.2024181211247/MOD13Q1.A2024161.h29v09.061.2024181211247.hdf'
})
print('Result:', result)
"
```

**Output:**

```
=====================================
     NASA Earth Data Download Skill
=====================================
Processing dictionary input...
Save directory: D:\ndvi\hdf
Found 1 download URL
- https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/MOD13Q1.061/MOD13Q1.A2024161.h29v09.061.2024181211247/MOD13Q1.A2024161.h29v09.061.2024181211247.hdf
Preparing to download 1 file to directory: D:\ndvi\hdf
File already exists, skipping: MOD13Q1.A2024161.h29v09.061.2024181211247.hdf

Download completed!
Success: 1, Failed: 0, Skipped: 0
Files saved to: D:\ndvi\hdf

Result: success
Message: Download completed! Success: 1, Failed: 0, Skipped: 0
=====================================
Result: {'status': 'success', 'message': 'Download completed! Success: 1, Failed: 0, Skipped: 0', 'results': {'success': 1, 'failed': 0, 'skipped': 0}, 'save_dir': 'D:\ndvi\hdf'}
```

### Example 3: Download Multiple Years of Data

**Command:**

```powershell
D:\software\anaconda\envs\geo_env\python.exe -c "
import sys
import os
skill_path = os.path.join('.trae', 'skills', 'nasa-earthdata-downloader')
sys.path.insert(0, skill_path)
from skill import run_skill
result = run_skill({
    'save_dir': r'D:\ndvi\hdf',
    'urls': 'https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/MOD13Q1.061/MOD13Q1.A2023161.h29v09.061.2023177233537/MOD13Q1.A2023161.h29v09.061.2023177233537.hdf'
})
print('Result:', result)
"
```

**Output:**

```
=====================================
     NASA Earth Data Download Skill
=====================================
Processing dictionary input...
Save directory: D:\ndvi\hdf
Found 1 download URL
- https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/MOD13Q1.061/MOD13Q1.A2023161.h29v09.061.2023177233537/MOD13Q1.A2023161.h29v09.061.2023177233537.hdf
Preparing to download 1 file to directory: D:\ndvi\hdf
MOD13Q1.A2023161.h29...: 100%|█████████████| 92.7M/92.7M [00:05<00:00, 15.6MB/s]

Download completed!
Success: 1, Failed: 0, Skipped: 0
Files saved to: D:\ndvi\hdf

Result: success
Message: Download completed! Success: 1, Failed: 0, Skipped: 0
=====================================
Result: {'status': 'success', 'message': 'Download completed! Success: 1, Failed: 0, Skipped: 0', 'results': {'success': 1, 'failed': 0, 'skipped': 0}, 'save_dir': 'D:\ndvi\hdf'}
```

## Features

- **Multi-threaded downloads**: Increases download speed by using multiple threads
- **Resumable downloads**: Continues from where it left off if download is interrupted
- **NASA Earth Data authentication**: Uses .netrc file for NASA Earth Data login credentials
- **File existence check**: Skips already downloaded files
- **Progress bars**: Shows download progress for each file
- **Error handling**: Gracefully handles download errors

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

## Supported Data Types

- MODIS products (MOD13A1, MOD13Q1, etc.)
- Other NASA Earth Data Cloud products
- Any file accessible through NASA Earth Data authentication

## Troubleshooting

- **Authentication errors**: Check your .netrc file for correct NASA Earth Data credentials
- **Download failures**: Ensure you have a stable internet connection and sufficient disk space
- **File not found errors**: Verify the URLs are correct and accessible with your NASA Earth Data account

## Trae Terminal Execution Issues

### Problem Description

When executing this skill in Trae terminal environment, you may encounter the following issues:

1. **Python command no response** - `python --version` shows no output
2. **Command execution failure** - Python commands exit with code 1
3. **Environment variable issues** - `echo %PATH%` outputs `%PATH%` instead of actual paths

### Root Causes

1. **Environment variable configuration issue** - Trae terminal cannot access system environment variables
2. **Python interpreter not found** - Terminal cannot locate Python executable
3. **Module import issues** - Relative import syntax fails when executed directly

### Solution

#### 1. Use Full Python Path

Execute Python using the full path to Anaconda's Python executable:

```powershell
D:\software\anaconda\envs\geo_env\python.exe -c "[Python code]"
```

#### 2. Execute Skill in geo_env Environment

```powershell
D:\software\anaconda\envs\geo_env\python.exe -c "
import sys
import os
skill_path = os.path.join('.trae', 'skills', 'nasa-earthdata-downloader')
sys.path.insert(0, skill_path)
from skill import run_skill
request = {
    'save_dir': r'D:\ndvi\hdf',
    'urls': 'https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/MOD13Q1.061/MOD13Q1.A2024161.h29v09.061.2024181211247/MOD13Q1.A2024161.h29v09.061.2024181211247.hdf'
}
result = run_skill(request)
print('Result:', result)
"
```

#### 3. Reference Documentation

For detailed analysis and troubleshooting steps, refer to:

**File**: `D:\Study\毕业论文\VOL_SELECT\Trae_Terminal_Python_Issue_Analysis.md`

**Key Sections**:
- Root cause analysis of Trae terminal Python execution issues
- Step-by-step troubleshooting guide
- Technical principles and best practices
- Environment configuration recommendations

### Verification Steps

1. **Check Python executable existence**:
   ```powershell
   dir D:\software\anaconda\envs\geo_env\python.exe
   ```

2. **Verify Python version**:
   ```powershell
   D:\software\anaconda\envs\geo_env\python.exe --version
   ```

3. **Test skill execution**:
   ```powershell
   D:\software\anaconda\envs\geo_env\python.exe -c "import sys; import os; skill_path = os.path.join('.trae', 'skills', 'nasa-earthdata-downloader'); sys.path.insert(0, skill_path); from skill import run_skill; result = run_skill({'save_dir': r'D:\ndvi\hdf', 'urls': 'https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/MOD13Q1.061/MOD13Q1.A2024161.h29v09.061.2024181211247/MOD13Q1.A2024161.h29v09.061.2024181211247.hdf'}); print('Result:', result)"
   ```

### Expected Output

```
=====================================
     NASA Earth Data Download Skill
=====================================
Processing dictionary input...
Save directory: D:\ndvi\hdf
Found 1 download URL
- https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/MOD13Q1.061/MOD13Q1.A2024161.h29v09.061.2024181211247/MOD13Q1.A2024161.h29v09.061.2024181211247.hdf
Preparing to download 1 file to directory: D:\ndvi\hdf
MOD13Q1.A2024161.h29...: 100%|██████████| 94.2M/94.2M [00:26<00:00, 3.55MB/s]

Download completed!
Success: 1, Failed: 0, Skipped: 0
Files saved to: D:\ndvi\hdf

Result: success
Message: Download completed! Success: 1, Failed: 0, Skipped: 0
=====================================
```
