import os
import re
import sys
from downloader import download_files, parse_urls

def handle_nasa_earthdata_download(request):
    """
    处理NASA Earth Data下载请求
    
    Args:
        request (dict): 包含下载参数的请求字典
            - save_dir: 保存目录
            - urls: 下载URL（字符串或列表）
            - max_threads: 最大并发线程数（可选）
            - chunk_size: 下载块大小（可选）
    
    Returns:
        dict: 下载结果
    """
    try:
        # 解析请求参数
        save_dir = request.get('save_dir')
        urls = request.get('urls')
        max_threads = request.get('max_threads', 5)
        chunk_size = request.get('chunk_size', 1024 * 1024)
        
        # 验证必要参数
        if not save_dir:
            return {
                "status": "error",
                "message": "缺少必要参数: save_dir"
            }
        
        if not urls:
            return {
                "status": "error",
                "message": "缺少必要参数: urls"
            }
        
        # 确保保存目录存在
        os.makedirs(save_dir, exist_ok=True)
        print(f"保存目录: {save_dir}")
        
        # 处理URL参数
        if isinstance(urls, str):
            # 从字符串中解析URL
            download_urls = parse_urls(urls)
        elif isinstance(urls, list):
            # 直接使用URL列表
            download_urls = urls
        else:
            return {
                "status": "error",
                "message": "urls参数格式错误，应为字符串或列表"
            }
        
        if not download_urls:
            return {
                "status": "error",
                "message": "未找到有效的下载URL"
            }
        
        print(f"找到 {len(download_urls)} 个下载URL")
        for url in download_urls:
            print(f"- {url}")
        
        # 执行下载
        results = download_files(
            urls=download_urls,
            save_dir=save_dir,
            max_threads=max_threads,
            chunk_size=chunk_size
        )
        
        return {
            "status": "success",
            "message": f"下载完成！成功: {results['success']}, 失败: {results['failed']}, 跳过: {results['skipped']}",
            "results": results,
            "save_dir": save_dir
        }
    except Exception as e:
        print(f"错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "status": "error",
            "message": f"下载失败: {str(e)}"
        }


def run_skill(input_data):
    """
    技能主入口函数
    
    Args:
        input_data (dict): 输入数据
    
    Returns:
        dict: 处理结果
    """
    print("=====================================")
    print("     NASA Earth Data 下载技能")
    print("=====================================")
    
    # 处理不同格式的输入
    if isinstance(input_data, dict):
        # 直接处理字典格式输入
        print("处理字典格式输入...")
        result = handle_nasa_earthdata_download(input_data)
    elif isinstance(input_data, str):
        # 处理字符串格式输入
        print("处理字符串格式输入...")
        # 尝试解析字符串中的参数
        # 查找save_dir
        save_dir_match = re.search(r'save_dir\s*[:=]\s*("[^"]+"|\'[^\']+\'|[^,\n]+)', input_data)
        save_dir = None
        if save_dir_match:
            save_dir = save_dir_match.group(1).strip('"\'')
        
        # 提取URL
        urls = input_data
        
        result = handle_nasa_earthdata_download({
            'save_dir': save_dir,
            'urls': urls
        })
    else:
        result = {
            "status": "error",
            "message": "输入格式错误，应为字典或字符串"
        }
    
    print(f"\n结果: {result['status']}")
    print(f"消息: {result['message']}")
    print("=====================================")
    
    return result
