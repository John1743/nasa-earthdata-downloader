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

• Error handling: Gracefully handles download errors with detailed logging

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

Execute skill with single file download:

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

### Python API Usage

```python
from skill import run_skill

# Download single file
result = run_skill({
    'save_dir': r'D:\Study\thesis\data\ndvi',
    'urls': 'https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/MOD13Q1.061/MOD13Q1.A2024161.h29v09.061.2024181211247/MOD13Q1.A2024161.h29v09.061.2024181211247.hdf'
})

print('Download result:', result)
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

This skill supports downloading from NASA Earth Data Cloud, including:

• MODIS products: MOD13A1, MOD13Q1, MYD13A1, MYD13Q1, etc.

• Other NASA Earth Data Cloud products: Any file accessible through NASA Earth Data authentication

• Vegetation indices: NDVI, EVI, and related vegetation products

• Time series data: Multiple years of data for temporal analysis


## TRAE Terminal Issues

If you encounter Python execution issues in TRAE terminal, see the detailed troubleshooting guide in `SKILL.md` or refer to `Trae_Terminal_Python_Issue_Analysis.md`.

Quick fix: Use full Python path:
```powershell
D:\software\anaconda\envs\geo_env\python.exe -c "[Python code]"
```

## Troubleshooting

### Authentication Errors

Problem: `Missing NASA Earthdata login credentials, please configure in .netrc file`

Solution:
1. Verify your .netrc file exists and contains correct credentials
2. Check that the machine name is exactly `urs.earthdata.nasa.gov`
3. Ensure your NASA Earth Data account is active

### Download Failures

Problem: `Download failed [URL]: Connection timeout`

Solution:
1. Check your internet connection
2. Verify the URL is correct and accessible
3. Ensure you have sufficient disk space
4. Try downloading again (resumable download will continue from where it left off)

### File Not Found Errors

Problem: `404 Client Error: Not Found`

Solution:
1. Verify the URL is correct
2. Check if the file is still available on NASA Earth Data
3. Ensure your NASA Earth Data account has access to the requested data

### Module Import Errors

Problem: `ImportError: attempted relative import with no known parent package`

Solution:
1. Ensure you're using the correct Python environment (geo_env)
2. Verify the skill files are in the correct directory structure
3. Use the full Python path when executing in TRAE terminal

## Advanced Usage

### Custom Thread Count

```python
result = run_skill({
    'save_dir': r'D:\ndvi\hdf',
    'urls': 'https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/MOD13Q1.061/MOD13Q1.A2024161.h29v09.061.2024181211247/MOD13Q1.A2024161.h29v09.061.2024181211247.hdf',
    'max_threads': 10  # Increase to 10 concurrent downloads
})
```

### Custom Chunk Size

```python
result = run_skill({
    'save_dir': r'D:\ndvi\hdf',
    'urls': 'https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/MOD13Q1.061/MOD13Q1.A2024161.h29v09.061.2024181211247/MOD13Q1.A2024161.h29v09.061.2024181211247.hdf',
    'chunk_size': 2 * 1024 * 1024  # 2MB chunks
})
```

## Documentation

For detailed documentation, see:
• SKILL.md: Complete skill documentation with examples

• TRAE_Terminal_Python_Issue_Analysis.md: Troubleshooting guide for TRAE terminal issues


## Contributing

Contributions are welcome! If you find bugs or want to add features:

1. Fork this repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - feel free to use this skill for personal and commercial projects.

## Acknowledgments

• NASA Earth Data for providing access to MODIS and other datasets

• LP DAAC for hosting MODIS data products

• The TRAE IDE team for providing the skill framework


## Version History

• v1.0.0 (2026-02-11): Initial release

  • Basic download functionality

  • Multi-threading support

  • Resumable downloads

  • NASA Earth Data authentication

  • TRAE terminal compatibility


## Contact

For issues, questions, or suggestions, please:
• Open an issue on GitHub

• Check existing documentation in SKILL.md


---

Note: This skill is designed for use with TRAE IDE and requires proper configuration of NASA Earth Data credentials. Always ensure you have permission to download the requested data from NASA Earth Data.
