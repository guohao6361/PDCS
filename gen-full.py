#!/usr/bin/env python3
"""在服务器上直接生成带base64图片的大JSON并导入MongoDB"""
import json, base64, os, struct, zlib, hashlib, sys

# 图片目录
IMG_DIR = "/tmp/product_images"

# 读取现有JSON获取商品结构
print("读取商品数据...")
with open("/tmp/products_data.json", "r", encoding="utf-8") as f:
    products = json.load(f)

print(f"商品数: {len(products)}")

# 加载图片并生成base64
print("加载图片base64...")
img_b64 = {}
for fname in sorted(os.listdir(IMG_DIR)):
    if fname.endswith(('.jpg', '.png')):
        fpath = os.path.join(IMG_DIR, fname)
        with open(fpath, 'rb') as f:
            data = f.read()
            if len(data) > 3000:  # 只使用有效图片
                img_b64[fname] = base64.b64encode(data).decode('utf-8')

print(f"有效图片: {len(img_b64)} 张")

# 为每个商品匹配图片base64
print("嵌入图片数据到商品中...")
for p in products:
    img_url = p.get("imageUrl", "")
    if img_url:
        fname = img_url.split("/")[-1]
        b64 = img_b64.get(fname, "")
        if b64:
            # 在描述中嵌入图片数据
            p["imageData"] = f"data:image/png;base64,{b64}"

# 检查大小
data = json.dumps(products, ensure_ascii=False)
size_mb = len(data.encode('utf-8')) / 1024 / 1024
print(f"当前大小: {size_mb:.1f} MB")

# 如果不够500MB，通过复制图片数据来扩展
if size_mb < 500:
    print(f"需要扩展到 500MB...")
    # 获取所有base64数据列表
    all_b64 = list(img_b64.values())
    
    # 为每个商品添加额外的图片数据字段
    idx = 0
    while size_mb < 500:
        for p in products:
            # 添加额外的图片数据
            extra_idx = idx % len(all_b64)
            p[f"img_{idx % 5}"] = f"data:image/png;base64,{all_b64[extra_idx]}"
            idx += 1
            if idx % 5000 == 0:
                data = json.dumps(products, ensure_ascii=False)
                size_mb = len(data.encode('utf-8')) / 1024 / 1024
                print(f"  扩展 {idx}, 大小: {size_mb:.1f} MB")
                if size_mb >= 500:
                    break

# 保存
print(f"\n最终大小: {size_mb:.1f} MB")
with open("/tmp/products_full.json", "w", encoding="utf-8") as f:
    f.write(data)

fsize = os.path.getsize("/tmp/products_full.json") / 1024 / 1024
print(f"文件大小: {fsize:.1f} MB")
print("完成: /tmp/products_full.json")
