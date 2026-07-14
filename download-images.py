#!/usr/bin/env python3
"""在服务器上运行：下载真实商品图片并批量更新 MongoDB"""
import base64
import json
import urllib.request
import ssl
import subprocess
import os
import sys

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 真实产品图片 URL
PRODUCT_IMAGES = {
    1: "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-16-pro-finish-select-202409-6-3inch-naturaltitanium?wid=960&hei=960&fmt=jpeg&qlt=90&.v=1726099978945",
    2: "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-16-pro-finish-select-202409-6-3inch-deserttitanium?wid=960&hei=960&fmt=jpeg&qlt=90&.v=1726099978945",
    3: "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-16-finish-select-202409-6-1inch-ultramarine?wid=960&hei=960&fmt=jpeg&qlt=90&.v=1726099963904",
    7: "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/macbook-air-og-202503?wid=960&hei=960&fmt=jpeg&qlt=90&.v=1741309128737",
    8: "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mbp-og-202410?wid=960&hei=960&fmt=jpeg&qlt=90&.v=1729239899580",
    9: "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/ipad-pro-model-select-gallery-1-202405?wid=960&hei=960&fmt=jpeg&qlt=90&.v=1713821703584",
    10: "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/airpods-pro-2-hero-select-202409?wid=976&hei=1000&fmt=jpeg&qlt=90&.v=1724040710360",
}

# 类别映射
CATEGORIES = {
    1: "手机", 2: "手机", 3: "手机", 4: "手机", 5: "手机", 6: "手机",
    7: "笔记本电脑", 8: "笔记本电脑", 9: "平板电脑", 10: "耳机",
    11: "手机", 12: "手机", 13: "手机", 14: "手机", 15: "手机", 16: "手机",
    17: "笔记本电脑", 18: "笔记本电脑", 19: "笔记本电脑", 20: "笔记本电脑",
    21: "平板电脑", 22: "平板电脑", 23: "耳机", 24: "耳机", 25: "耳机", 26: "耳机",
    27: "智能手表", 28: "智能手表", 29: "智能手表", 30: "智能手表",
    31: "台式电脑", 32: "台式电脑", 33: "家电", 34: "家电", 35: "家电", 36: "家电",
    37: "相机", 38: "相机", 39: "相机", 40: "相机",
}

def download_image(url, timeout=15):
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        })
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            data = resp.read()
            if len(data) > 1000:
                return base64.b64encode(data).decode("ascii")
    except Exception as e:
        print(f"  下载失败: {e}")
    return None

def generate_colored_png(product_id, category):
    """生成好看的渐变占位 PNG"""
    import zlib, struct
    colors = {
        "手机": [(30, 60, 114), (180, 50, 50), (50, 120, 80)],
        "笔记本电脑": [(40, 40, 40), (180, 180, 180), (60, 80, 120)],
        "平板电脑": [(50, 100, 150), (150, 50, 100), (80, 120, 60)],
        "耳机": [(30, 30, 30), (200, 200, 200), (60, 60, 120)],
        "智能手表": [(40, 40, 40), (180, 160, 100), (60, 100, 120)],
        "台式电脑": [(50, 50, 50), (160, 160, 160), (80, 60, 100)],
        "家电": [(60, 100, 60), (160, 80, 40), (80, 80, 120)],
        "相机": [(30, 30, 30), (180, 180, 180), (100, 60, 60)],
    }
    color_list = colors.get(category, [(100, 100, 100)])
    r, g, b = color_list[product_id % len(color_list)]
    w, h = 200, 200
    
    raw = b""
    for y in range(h):
        raw += b"\x00"
        for x in range(w):
            factor = 1.0 - (abs(x - w//2) + abs(y - h//2)) / (w + h) * 0.5
            raw += bytes([max(0, min(255, int(r*factor))), max(0, min(255, int(g*factor))), max(0, min(255, int(b*factor)))])
    
    def chunk(ct, data):
        c = ct + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xffffffff)
    
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(raw, 6))
    png += chunk(b"IEND", b"")
    return base64.b64encode(png).decode("ascii")

def main():
    print("=== 下载商品图片 ===\n")
    
    # 1. 下载真实图片
    images = {}
    for pid in range(1, 41):
        cat = CATEGORIES.get(pid, "手机")
        if pid in PRODUCT_IMAGES:
            print(f"[{pid:2d}] {cat:8s} 下载真实图片...", end=" ")
            b64 = download_image(PRODUCT_IMAGES[pid])
            if b64:
                images[pid] = "data:image/jpeg;base64," + b64
                print(f"OK ({len(b64)//1024}KB)")
            else:
                print("失败，用占位图")
                png_b64 = generate_colored_png(pid, cat)
                images[pid] = "data:image/png;base64," + png_b64
        else:
            png_b64 = generate_colored_png(pid, cat)
            images[pid] = "data:image/png;base64," + png_b64
            print(f"[{pid:2d}] {cat:8s} 占位图 ({len(png_b64)//1024}KB)")
    
    print(f"\n准备完成: {len(images)} 个基础产品图片\n")
    
    # 2. 生成 mongosh 更新脚本（分批写入临时文件）
    print("=== 生成更新脚本 ===\n")
    
    tmp_dir = "/tmp/img-update"
    os.makedirs(tmp_dir, exist_ok=True)
    
    # 写入图片数据文件（JSON）
    images_json = json.dumps(images, ensure_ascii=False)
    with open(os.path.join(tmp_dir, "images.json"), "w") as f:
        f.write(images_json)
    print(f"图片数据: {len(images_json)//1024}KB")
    
    # 生成 mongosh 脚本
    script = f'''
db = db.getSiblingDB("ecommerce");
var fs = require("fs");
var images = JSON.parse(fs.readFileSync("{tmp_dir}/images.json", "utf8"));
print("加载了 " + Object.keys(images).length + " 个基础图片");

var maxId = {84327};
var updated = 0;

for (var baseId = 1; baseId <= 40; baseId++) {{
    var imgData = images[baseId.toString()];
    if (!imgData) continue;
    
    var ids = [];
    for (var id = baseId; id <= maxId; id += 40) {{
        ids.push(NumberInt(id));
    }}
    
    if (ids.length > 0) {{
        var result = db.products.updateMany(
            {{ _id: {{ $in: ids }} }},
            {{ $set: {{ imageData: imgData }} }}
        );
        updated += result.modifiedCount;
        print("基础产品 " + baseId + ": 更新 " + result.modifiedCount + " 条");
    }}
}}

print("\\n完成！共更新 " + updated + " 条商品图片");
var sample = db.products.findOne();
print("样本 imageData 长度: " + (sample.imageData ? sample.imageData.length : 0));
'''
    
    script_path = os.path.join(tmp_dir, "update.js")
    with open(script_path, "w") as f:
        f.write(script)
    
    print(f"脚本: {script_path}")
    print("\n=== 完成 ===")
    print("下一步: kubectl cp 到 MongoDB Pod 并执行")

if __name__ == "__main__":
    main()
