#!/usr/bin/env python3
"""生成轻量商品数据（不含base64嵌入），图片通过URL引用容器内文件"""
import os, json, time

# 读取已有的完整数据，去掉base64嵌入
print("读取原始数据...")
with open("D:/tmp/products_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"原始商品数: {len(data)}")

# 清理description中的[IMG_DATA]...[/IMG_DATA]部分
import re
pattern = re.compile(r'\n\n\[IMG_DATA\].*?\[/IMG_DATA\]', re.DOTALL)

for p in data:
    desc = p.get("description", "")
    p["description"] = pattern.sub("", desc)

# 保存轻量版
print("保存轻量版...")
out_path = "D:/tmp/products_data_lite.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)

size_mb = os.path.getsize(out_path) / 1024 / 1024
print(f"轻量版大小: {size_mb:.1f} MB")
print(f"商品数: {len(data)}")
print(f"输出: {out_path}")
