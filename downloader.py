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
    下载单个文件
    
    Args:
        url (str): 下载URL
        save_dir (str): 保存目录
        chunk_size (int): 下载块大小
        
    Returns:
        bool: 下载是否成功
    """
    try:
        os.makedirs(save_dir, exist_ok=True)
        filename = unquote(url.split('/')[-1].strip())
        filepath = os.path.join(save_dir, filename)

        if os.path.exists(filepath):
            print(f"文件已存在，跳过: {filename}")
            return True

        # 获取NASA Earth Data认证信息
        auth_info = netrc().authenticators('urs.earthdata.nasa.gov')
        if not auth_info:
            raise ValueError("缺少NASA Earthdata登录凭证，请在.netrc文件中配置")
        auth = (auth_info[0], auth_info[2])  # (username, password)

        # 检查文件是否部分下载，支持断点续传
        headers = {}
        if os.path.exists(filepath):
            headers = {'Range': f'bytes={os.path.getsize(filepath)}-'}

        with requests.get(url, stream=True, headers=headers, auth=auth) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))

            # 显示下载进度条
            progress = tqdm(
                total=total_size,
                unit='B',
                unit_scale=True,
                desc=filename[:20] + (filename[20:] and '...'),
                ncols=80
            )

            # 以追加模式打开文件（支持断点续传）
            with open(filepath, 'ab') as f:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        progress.update(len(chunk))
            progress.close()
        return True
    except Exception as e:
        print(f"\n下载失败 [{url}]: {str(e)}")
        return False


def download_files(urls, save_dir, max_threads=5, chunk_size=1024 * 1024):
    """
    批量下载文件
    
    Args:
        urls (list): 下载URL列表
        save_dir (str): 保存目录
        max_threads (int): 最大并发线程数
        chunk_size (int): 下载块大小
        
    Returns:
        dict: 下载结果统计
    """
    print(f"准备下载 {len(urls)} 个文件到目录: {save_dir}")
    
    # 确保保存目录存在
    os.makedirs(save_dir, exist_ok=True)

    # 多线程下载
    threads = []
    results = {"success": 0, "failed": 0, "skipped": 0}

    for url in urls:
        # 控制并发线程数
        while threading.active_count() > max_threads:
            threading.Event().wait(0.1)

        # 创建并启动下载线程
        t = threading.Thread(
            target=lambda u: (
                results.update({"success": results["success"] + 1}) if download_file(u, save_dir, chunk_size) else results.update({"failed": results["failed"] + 1})
            ),
            args=(url,)
        )
        t.daemon = True
        t.start()
        threads.append(t)

    # 等待所有线程完成
    for t in threads:
        t.join()

    print(f"\n下载完成！")
    print(f"成功: {results['success']}, 失败: {results['failed']}, 跳过: {results['skipped']}")
    print(f"文件保存在: {save_dir}")
    
    return results


def parse_urls(input_str):
    """
    从输入字符串中解析URL列表
    
    Args:
        input_str (str): 包含URL的字符串
        
    Returns:
        list: URL列表
    """
    # 匹配HTTP和HTTPS URL
    urls = re.findall(r'https?://[^,]+', input_str)
    return urls


if __name__ == "__main__":
    # 示例用法
    save_dir = r"D:\Study\毕业论文\data\ndvi"
    
    # 示例下载链接
    raw_links = """
    https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/MOD13A1.061/MOD13A1.A2015225.h29v09.061.2021331155049/MOD13A1.A2015225.h29v09.061.2021331155049.hdf,
    https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/MOD13A1.061/MOD13A1.A2015241.h29v09.061.2021331193012/MOD13A1.A2015241.h29v09.061.2021331193012.hdf
    """
    
    download_urls = parse_urls(raw_links)
    download_files(download_urls, save_dir, max_threads=5)
