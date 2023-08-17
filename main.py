import requests
from bs4 import BeautifulSoup
from collections import deque
import time
from functools import wraps
from concurrent.futures import ThreadPoolExecutor
import threading

# 获取代理IP列表
def get_proxies():
    url = "https://sslproxies.org/"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    proxies = set()
    for i in soup.find_all('td')[::8]:
        proxies.add(i.get_text())
    return deque(proxies)

# 创建一个锁对象，用于确保线程安全地访问和修改代理池
proxy_pool_lock = threading.Lock()

# 重试装饰器，用于自动重试和更换代理IP
def retry(max_retries=3, retry_interval=5, max_ip_changes=10, max_ip_failures=3):
    def decorator(func):
        @wraps(func)
        def wrapper(url, proxy_pool, *args, **kwargs):
            retries = 0
            ip_changes = 0
            ip_failures = 0

            # 使用锁来确保线程安全地从代理池中移除一个代理
            with proxy_pool_lock:
                proxy = proxy_pool.popleft()

            while retries < max_retries:
                try:
                    return func(url, proxy, *args, **kwargs)
                except Exception as e:
                    print(f"Request failed with error {e}. Retrying...")
                    retries += 1
                    ip_failures += 1
                    time.sleep(retry_interval)
                    if ip_failures >= max_ip_failures:
                        print(f"IP {proxy} failed {max_ip_failures} times. Removing from pool...")
                        ip_failures = 0
                    else:
                        # 使用锁来确保线程安全地将代理放回代理池
                        with proxy_pool_lock:
                            proxy_pool.append(proxy)

                    if retries % max_retries == 0:
                        ip_changes += 1
                        if ip_changes > max_ip_changes:
                            raise Exception("Max IP changes reached. Exiting...")
                        print("Changing IP...")
                        # 使用锁来确保线程安全地从代理池中移除一个新的代理
                        with proxy_pool_lock:
                            proxy = proxy_pool.popleft()

            print("Max retries reached. Exiting...")
            return None
        return wrapper
    return decorator

@retry(max_retries=3, retry_interval=5, max_ip_changes=10, max_ip_failures=3)
def request_with_proxy(url, proxy):
    response = requests.get(url, proxies={"http": proxy, "https": proxy}, timeout=5)
    return response

# 使用ThreadPoolExecutor并发地处理URL列表
def process_urls(url_list, proxy_pool, max_workers=10):
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(request_with_proxy, url, proxy_pool) for url in url_list]
        for future in futures:
            results.append(future.result())
    return results

proxies = get_proxies()
proxy_pool = proxies
url_list = ["http://example.com"] * 50  # 示例URL列表，你可以替换为实际的URL列表

responses = process_urls(url_list, proxy_pool)
