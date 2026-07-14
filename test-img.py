import requests

urls = [
    "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-16-pro-finish-select-202409-6-9inch-naturaltitanium?wid=400&hei=400&fmt=jpeg&src=src",
    "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-16-pro-hero-select-202409?wid=400&hei=400&fmt=jpeg&src=src",
    "https://www.apple.com/v/iphone/home/bx/images/overview/hero/hero_iphone16pro__bsmnx0k0f7qu_large.png",
    "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/MQD83?wid=400&hei=400&fmt=jpeg&src=src",
    "https://m.media-amazon.com/images/I/51aX23mWVML._AC_SL1000_.jpg",
    "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mac-mini-select-202411?wid=400&hei=400&fmt=jpeg&src=src",
]

for url in urls:
    try:
        r = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        ct = r.headers.get('content-type', '?')
        print(f"Status: {r.status_code}, Size: {len(r.content)}, Type: {ct}, URL: {url[:80]}")
    except Exception as e:
        print(f"ERROR: {e}, URL: {url[:80]}")
