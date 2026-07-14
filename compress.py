import gzip, shutil, os
print("压缩中...")
with open("D:/tmp/products_data.json", "rb") as f:
    with gzip.open("D:/tmp/products_data.json.gz", "wb", compresslevel=1) as o:
        shutil.copyfileobj(f, o, 10*1024*1024)
size = os.path.getsize("D:/tmp/products_data.json.gz") / 1024 / 1024
print(f"完成: {size:.1f} MB")
