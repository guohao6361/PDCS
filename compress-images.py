#!/usr/bin/env python3
"""压缩 MongoDB 中的商品图片到更小尺寸"""
import base64
import json
import subprocess
import os

def compress_image_b64(b64_data, max_size=400):
    """压缩 base64 图片到指定最大边长"""
    try:
        # 移除 data:image/xxx;base64, 前缀
        if ',' in b64_data:
            prefix, img_b64 = b64_data.split(',', 1)
        else:
            prefix = "data:image/jpeg;base64,"
            img_b64 = b64_data
        
        img_data = base64.b64decode(img_b64)
        
        # 使用 Python PIL 压缩（如果可用）
        try:
            from PIL import Image
            import io
            img = Image.open(io.BytesIO(img_data))
            # 缩放
            img.thumbnail((max_size, max_size), Image.LANCZOS)
            # 保存为 JPEG
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=75)
            compressed = base64.b64encode(buffer.getvalue()).decode('ascii')
            return prefix.split(';')[0] + ';base64,' + compressed
        except ImportError:
            # 没有 PIL，使用原始数据
            return b64_data
    except Exception as e:
        print(f"  压缩失败: {e}")
        return b64_data

def main():
    print("=== 压缩商品图片 ===\n")
    
    # 读取当前图片数据
    images_path = "/tmp/img-update/images-v2.json"
    if not os.path.exists(images_path):
        print("图片文件不存在!")
        return
    
    with open(images_path, "r") as f:
        images = json.load(f)
    
    print(f"加载了 {len(images)} 个图片\n")
    
    # 压缩每个图片
    compressed = {}
    for pid_str, img_data in images.items():
        pid = int(pid_str)
        original_size = len(img_data)
        compressed_img = compress_image_b64(img_data, max_size=150)  # 压缩到 150x150
        compressed_size = len(compressed_img)
        ratio = compressed_size / original_size * 100
        compressed[pid_str] = compressed_img
        print(f"[{pid:2d}] {original_size//1024:4d}KB -> {compressed_size//1024:4d}KB ({ratio:.0f}%)")
    
    # 保存压缩后的图片
    compressed_json = json.dumps(compressed, ensure_ascii=False)
    with open("/tmp/img-update/images-compressed.json", "w") as f:
        f.write(compressed_json)
    
    print(f"\n压缩后总大小: {len(compressed_json)//1024}KB (原 {os.path.getsize(images_path)//1024}KB)")
    
    # 生成更新脚本
    script = '''
db = db.getSiblingDB("ecommerce");
var fs = require("fs");
var images = JSON.parse(fs.readFileSync("/tmp/img-update/images-compressed.json", "utf8"));
print("加载了 " + Object.keys(images).length + " 个压缩图片");

var maxId = 84327;
var updated = 0;

for (var baseId = 1; baseId <= 40; baseId++) {
    var imgData = images[baseId.toString()];
    if (!imgData) continue;
    
    var ids = [];
    for (var id = baseId; id <= maxId; id += 40) {
        ids.push(NumberInt(id));
    }
    
    if (ids.length > 0) {
        var result = db.products.updateMany(
            { _id: { $in: ids } },
            { $set: { imageData: imgData } }
        );
        updated += result.modifiedCount;
        print("基础产品 " + baseId + ": 更新 " + result.modifiedCount + " 条");
    }
}

print("\\n完成！共更新 " + updated + " 条商品图片");
'''
    
    with open("/tmp/img-update/update-compressed.js", "w") as f:
        f.write(script)
    
    print("脚本: /tmp/img-update/update-compressed.js")

if __name__ == "__main__":
    main()
