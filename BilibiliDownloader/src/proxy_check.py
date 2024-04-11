import urllib.request
from proxy_pool import get_proxies


def check_proxies():
    available_proxies = []
    for proxy in get_proxies():
        proxy_handler = urllib.request.ProxyHandler({'http': proxy})
        opener = urllib.request.build_opener(proxy_handler)
        try:
            response = opener.open(
                'https://api.bilibili.com/x/space/arc/search?mid=2052851329&ps=30&tid=0&order=pubdate&jsonp=json',
                timeout=5)
            if response.getcode() == 200:
                available_proxies.append(proxy)
        except Exception as e:
            pass
    return available_proxies


available_proxies = check_proxies()
total_proxies = len(get_proxies())
total_available_proxies = len(available_proxies)

print("IP: (是否可用)")
for proxy in get_proxies():
    print(f"{proxy}: {'可用' if proxy in available_proxies else '不可用'}")

print(f"总计ip数: {total_proxies}")
print(f"总计可用ip数: {total_available_proxies}")
