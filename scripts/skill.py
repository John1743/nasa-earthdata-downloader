import os
import re
import sys
from downloader import download_files, parse_urls

def handle_nasa_earthdata_download(request):
    """
    Handle NASA Earth Data download request
    
    Args:
        request (dict): Request dictionary containing download parameters
            - save_dir: Save directory
            - urls: Download URLs (string or list)
            - max_threads: Maximum concurrent threads (optional)
            - chunk_size: Download chunk size (optional)
    
    Returns:
        dict: Download result
    """
    try:
        # Parse request parameters
        save_dir = request.get('save_dir')
        urls = request.get('urls')
        max_threads = request.get('max_threads', 5)
        chunk_size = request.get('chunk_size', 1024 * 1024)
        
        # Validate required parameters
        if not save_dir:
            return {
                "status": "error",
                "message": "Missing required parameter: save_dir"
            }
        
        if not urls:
            return {
                "status": "error",
                "message": "Missing required parameter: urls"
            }
        
        # Ensure save directory exists
        os.makedirs(save_dir, exist_ok=True)
        print(f"Save directory: {save_dir}")
        
        # Handle URL parameter
        if isinstance(urls, str):
            # Parse URLs from string
            download_urls = parse_urls(urls)
        elif isinstance(urls, list):
            # Use URL list directly
            download_urls = urls
        else:
            return {
                "status": "error",
                "message": "Invalid urls parameter format, should be string or list"
            }
        
        if not download_urls:
            return {
                "status": "error",
                "message": "No valid download URLs found"
            }
        
        print(f"Found {len(download_urls)} download URLs")
        for url in download_urls:
            print(f"- {url}")
        
        # Execute download
        results = download_files(
            urls=download_urls,
            save_dir=save_dir,
            max_threads=max_threads,
            chunk_size=chunk_size
        )
        
        return {
            "status": "success",
            "message": f"Download completed! Success: {results['success']}, Failed: {results['failed']}, Skipped: {results['skipped']}",
            "results": results,
            "save_dir": save_dir
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "status": "error",
            "message": f"Download failed: {str(e)}"
        }


def run_skill(input_data):
    """
    Skill main entry function
    
    Args:
        input_data (dict): Input data
    
    Returns:
        dict: Processing result
    """
    print("=====================================")
    print("     NASA Earth Data Download Skill")
    print("=====================================")
    
    # Handle different input formats
    if isinstance(input_data, dict):
        # Directly handle dictionary input
        print("Processing dictionary input...")
        result = handle_nasa_earthdata_download(input_data)
    elif isinstance(input_data, str):
        # Handle string input
        print("Processing string input...")
        # Try to parse parameters from string
        # Find save_dir
        save_dir_match = re.search(r'save_dir\s*[:=]\s*("[^"]+"|\'[^\']+\'|[^,\n]+)', input_data)
        save_dir = None
        if save_dir_match:
            save_dir = save_dir_match.group(1).strip('"\'')
        
        # Extract URLs
        urls = input_data
        
        result = handle_nasa_earthdata_download({
            'save_dir': save_dir,
            'urls': urls
        })
    else:
        result = {
            "status": "error",
            "message": "Invalid input format, should be dictionary or string"
        }
    
    print(f"\nResult: {result['status']}")
    print(f"Message: {result['message']}")
    print("=====================================")
    
    return result
