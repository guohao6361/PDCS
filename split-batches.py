#!/usr/bin/env python3
"""将大JSON拆分为多个小文件"""
import json, os

print("读取商品数据...")
with open("/tmp/products_full.json", "r", encoding="utf-8") as f:
    products = json.load(f)

print(f"总商品数: {len(products)}")

# 拆分为每个文件约5000个商品
batch_size = 5000
batches = []
for i in range(0, len(products), batch_size):
    batch = products[i:i+batch_size]
    batch_file = f"/tmp/products_batch_{len(batches)}.json"
    data = json.dumps(batch, ensure_ascii=False)
    with open(batch_file, "w", encoding="utf-8") as f:
        f.write(data)
    size_mb = os.path.getsize(batch_file) / 1024 / 1024
    batches.append((batch_file, len(batch), size_mb))
    print(f"  批次 {len(batches)-1}: {len(batch)} 商品, {size_mb:.1f} MB")

print(f"\n共 {len(batches)} 个批次")
# 保存批次信息
with open("/tmp/batch_info.json", "w") as f:
    json.dump(batches, f)
print("完成")
