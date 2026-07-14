import requests
import os

# 清除代理
os.environ.pop('HTTP_PROXY', None)
os.environ.pop('HTTPS_PROXY', None)
os.environ.pop('http_proxy', None)
os.environ.pop('https_proxy', None)
os.environ.pop('ALL_PROXY', None)
os.environ.pop('all_proxy', None)

session = requests.Session()
session.trust_env = False  # 不使用系统代理
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})

urls = [
    "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-16-pro-finish-select-202409-6-9inch-naturaltitanium?wid=400&hei=400&fmt=jpeg&src=src",
    "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/MQD83?wid=400&hei=400&fmt=jpeg&src=src",
    "https://m.media-amazon.com/images/I/51aX23mWVML._AC_SL1000_.jpg",
    "https://www.apple.com/v/iphone/home/bx/images/overview/hero/hero_iphone16pro__bsmnx0k0f7qu_large.png",
    "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mac-mini-select-202411?wid=400&hei=400&fmt=jpeg&src=src",
]

for url in urls:
    try:
        r = session.get(url, timeout=15)
        ct = r.headers.get('content-type', '?')
        print(f"Status: {r.status_code}, Size: {len(r.content)}, Type: {ct}, URL: {url[:80]}")
    except Exception as e:
        print(f"ERROR: {str(e)[:100]}, URL: {url[:80]}")
