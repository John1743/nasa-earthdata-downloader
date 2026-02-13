import os
import re
import requests
import threading
from tqdm import tqdm
from urllib.parse import unquote
from netrc import netrc
from requests.auth import HTTPBasicAuth

def download_file(url, save_dir, chunk_size=1024 * 1024):
    """
    Download single file
    
    Args:
        url (str): Download URL
        save_dir (str): Save directory
        chunk_size (int): Download chunk size
        
    Returns:
        bool: Whether download succeeded
    """
    try:
        os.makedirs(save_dir, exist_ok=True)
        filename = unquote(url.split('/')[-1].strip())
        filepath = os.path.join(save_dir, filename)

        if os.path.exists(filepath):
            print(f"File already exists, skipping: {filename}")
            return True

        # Get NASA Earth Data authentication info
        auth_info = netrc().authenticators('urs.earthdata.nasa.gov')
        if not auth_info:
            raise ValueError("Missing NASA Earthdata login credentials, please configure in .netrc file")
        auth = (auth_info[0], auth_info[2])  # (username, password)

        # Check if file is partially downloaded (resumable download)
        headers = {}
        if os.path.exists(filepath):
            headers = {'Range': f'bytes={os.path.getsize(filepath)}-'}

        with requests.get(url, stream=True, headers=headers, auth=auth) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))

            # Show download progress bar
            progress = tqdm(
                total=total_size,
                unit='B',
                unit_scale=True,
                desc=filename[:20] + (filename[20:] and '...'),
                ncols=80
            )

            # Open file in append mode (support resumable download)
            with open(filepath, 'ab') as f:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        progress.update(len(chunk))
            progress.close()
        return True
    except Exception as e:
        print(f"\nDownload failed [{url}]: {str(e)}")
        return False


def download_files(urls, save_dir, max_threads=5, chunk_size=1024 * 1024):
    """
    Batch download files
    
    Args:
        urls (list): List of download URLs
        save_dir (str): Save directory
        max_threads (int): Maximum concurrent threads
        chunk_size (int): Download chunk size
        
    Returns:
        dict: Download result statistics
    """
    print(f"Preparing to download {len(urls)} files to directory: {save_dir}")
    
    # Ensure save directory exists
    os.makedirs(save_dir, exist_ok=True)

    # Multi-threaded download
    threads = []
    results = {"success": 0, "failed": 0, "skipped": 0}

    for url in urls:
        # Control concurrent thread count
        while threading.active_count() > max_threads:
            threading.Event().wait(0.1)

        # Create and start download thread
        t = threading.Thread(
            target=lambda u: (
                results.update({"success": results["success"] + 1}) if download_file(u, save_dir, chunk_size) else results.update({"failed": results["failed"] + 1})
            ),
            args=(url,)
        )
        t.daemon = True
        t.start()
        threads.append(t)

    # Wait for all threads to complete
    for t in threads:
        t.join()

    print(f"\nDownload completed!")
    print(f"Success: {results['success']}, Failed: {results['failed']}, Skipped: {results['skipped']}")
    print(f"Files saved to: {save_dir}")
    
    return results


def parse_urls(input_str):
    """
    Parse URL list from input string
    
    Args:
        input_str (str): String containing URLs
        
    Returns:
        list: List of URLs
    """
    # Match HTTP and HTTPS URLs
    urls = re.findall(r'https?://[^,]+', input_str)
    return urls


if __name__ == "__main__":
    # Example usage
    save_dir = r"D:\data\ndvi"
    
    # Example download links
    raw_links = """
    https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/MOD13A1.061/MOD13A1.A2015225.h29v09.061.2021331155049/MOD13A1.A2015225.h29v09.061.2021331155049.hdf,
    https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/MOD13A1.061/MOD13A1.A2015241.h29v09.061.2021331193012/MOD13A1.A2015241.h29v09.061.2021331193012.hdf
    """
    
    download_urls = parse_urls(raw_links)
    download_files(download_urls, save_dir, max_threads=5)

