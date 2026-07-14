#!/usr/bin/env python3
"""生成商品数据（整数_id），分批输出JSON，然后导入MongoDB"""
import json, base64, time, struct, zlib, hashlib, sys, os, random

# ============ 真实商品数据 ============
PRODUCTS = [
    {"name": "Apple iPhone 16 Pro Max 256GB 原色钛金属", "price": 9999, "category": "手机", "brand": "Apple",
     "description": "Apple iPhone 16 Pro Max，搭载 A18 Pro 芯片，6.9 英寸超视网膜 XDR 显示屏，支持 ProMotion 自适应刷新率最高 120Hz。4800 万像素融合摄像头系统，支持 5 倍光学变焦。钛金属设计，IP68 级防水。",
     "attributes": {"品牌": "Apple", "屏幕": "6.9英寸 OLED", "处理器": "A18 Pro", "存储": "256GB", "内存": "8GB", "摄像头": "4800万主摄", "电池": "4685mAh", "系统": "iOS 18", "重量": "227g", "防水": "IP68"}},
    {"name": "Apple iPhone 16 Pro 128GB 沙漠钛金属", "price": 7999, "category": "手机", "brand": "Apple",
     "description": "Apple iPhone 16 Pro，A18 Pro 芯片，6.3 英寸超视网膜 XDR 显示屏。Pro 级摄像头系统，支持微距摄影和 ProRAW。钛金属设计。",
     "attributes": {"品牌": "Apple", "屏幕": "6.3英寸 OLED", "处理器": "A18 Pro", "存储": "128GB", "摄像头": "4800万融合", "电池": "3274mAh", "系统": "iOS 18"}},
    {"name": "Apple iPhone 16 128GB 群青色", "price": 5999, "category": "手机", "brand": "Apple",
     "description": "Apple iPhone 16，A18 芯片，6.1 英寸超视网膜 XDR 显示屏。4800 万像素双摄系统。",
     "attributes": {"品牌": "Apple", "屏幕": "6.1英寸 OLED", "处理器": "A18", "存储": "128GB", "系统": "iOS 18"}},
    {"name": "华为 Mate 70 Pro 256GB 雅丹黑", "price": 6499, "category": "手机", "brand": "华为",
     "description": "华为 Mate 70 Pro，麒麟 9020 芯片，6.9 英寸 OLED 曲面屏。XMAGE 影像系统，5000 万像素超感知主摄。HarmonyOS 4。",
     "attributes": {"品牌": "华为", "屏幕": "6.9英寸 OLED曲面", "处理器": "麒麟9020", "存储": "256GB", "摄像头": "5000万XMAGE", "系统": "HarmonyOS 4"}},
    {"name": "小米 15 Ultra 512GB 黑色", "price": 5999, "category": "手机", "brand": "小米",
     "description": "小米 15 Ultra，骁龙 8 Elite，徕卡光学镜头。2K 120Hz LTPO AMOLED 屏幕，6000mAh 大电池。",
     "attributes": {"品牌": "小米", "屏幕": "6.73英寸 AMOLED", "处理器": "骁龙8 Elite", "存储": "512GB", "电池": "6000mAh"}},
    {"name": "三星 Galaxy S25 Ultra 256GB 钛灰", "price": 9999, "category": "手机", "brand": "三星",
     "description": "三星 Galaxy S25 Ultra，骁龙 8 Elite，2 亿像素摄像头，6.9 英寸 Dynamic AMOLED 2X。S Pen 手写笔。",
     "attributes": {"品牌": "三星", "屏幕": "6.9英寸 AMOLED", "处理器": "骁龙8 Elite", "存储": "256GB", "摄像头": "2亿像素"}},
    {"name": "Apple MacBook Air 13英寸 M4 256GB", "price": 9999, "category": "笔记本电脑", "brand": "Apple",
     "description": "MacBook Air 13 英寸，Apple M4 芯片，16GB 统一内存，256GB SSD。13.6 英寸 Liquid Retina 显示屏。18 小时电池续航。",
     "attributes": {"品牌": "Apple", "处理器": "M4", "内存": "16GB", "存储": "256GB SSD", "屏幕": "13.6英寸", "电池": "18小时"}},
    {"name": "Apple MacBook Pro 14英寸 M4 Pro", "price": 15999, "category": "笔记本电脑", "brand": "Apple",
     "description": "MacBook Pro 14 英寸，M4 Pro 芯片，24GB 统一内存，512GB SSD。14.2 英寸 Liquid Retina XDR。22 小时续航。",
     "attributes": {"品牌": "Apple", "处理器": "M4 Pro", "内存": "24GB", "存储": "512GB SSD", "屏幕": "14.2英寸 XDR"}},
    {"name": "联想 ThinkPad X1 Carbon Gen 12", "price": 12999, "category": "笔记本电脑", "brand": "联想",
     "description": "ThinkPad X1 Carbon Gen 12，英特尔酷睿 Ultra 7，32GB LPDDR5x，1TB SSD。14 英寸 2.8K OLED。",
     "attributes": {"品牌": "联想", "处理器": "Intel Core Ultra 7", "内存": "32GB", "存储": "1TB SSD", "屏幕": "14英寸 2.8K OLED"}},
    {"name": "华为 MateBook X Pro 2025", "price": 11999, "category": "笔记本电脑", "brand": "华为",
     "description": "华为 MateBook X Pro 2025，酷睿 Ultra 9，32GB 内存，2TB SSD。14.2 英寸 3.1K OLED 触控屏。",
     "attributes": {"品牌": "华为", "处理器": "Intel Core Ultra 9", "内存": "32GB", "存储": "2TB SSD", "屏幕": "14.2英寸 3.1K OLED"}},
    {"name": "Apple iPad Pro 13英寸 M4 256GB", "price": 10799, "category": "平板电脑", "brand": "Apple",
     "description": "iPad Pro 13 英寸，M4 芯片，Ultra Retina XDR 显示屏。支持 Apple Pencil Pro 和妙控键盘。",
     "attributes": {"品牌": "Apple", "处理器": "M4", "存储": "256GB", "屏幕": "13英寸 OLED", "重量": "579g"}},
    {"name": "Apple iPad Air 13英寸 M3 128GB", "price": 6999, "category": "平板电脑", "brand": "Apple",
     "description": "iPad Air 13 英寸，M3 芯片，Liquid Retina 显示屏，支持 Apple Pencil Pro。",
     "attributes": {"品牌": "Apple", "处理器": "M3", "存储": "128GB", "屏幕": "13英寸 Liquid Retina"}},
    {"name": "Apple AirPods Pro 2 (USB-C)", "price": 1899, "category": "耳机", "brand": "Apple",
     "description": "AirPods Pro 2，H2 芯片，自适应音频，个性化空间音频，主动降噪。USB-C 充电盒。",
     "attributes": {"品牌": "Apple", "类型": "入耳式", "降噪": "主动降噪", "连接": "蓝牙5.3", "续航": "6+30小时"}},
    {"name": "索尼 WH-1000XM5 黑色头戴式降噪耳机", "price": 2499, "category": "耳机", "brand": "索尼",
     "description": "索尼 WH-1000XM5，双芯片降噪，30 小时续航，LDAC 高解析音频。",
     "attributes": {"品牌": "索尼", "类型": "头戴式", "降噪": "HD降噪QN1", "续航": "30小时"}},
    {"name": "Apple Watch Ultra 2 GPS+蜂窝 49mm", "price": 6499, "category": "智能手表", "brand": "Apple",
     "description": "Apple Watch Ultra 2，49mm 钛金属，3000 尼特显示屏，双频 GPS，100 米防水。",
     "attributes": {"品牌": "Apple", "尺寸": "49mm", "材质": "钛金属", "防水": "100米"}},
    {"name": "Apple iMac 24英寸 M4 蓝色 256GB", "price": 12499, "category": "台式电脑", "brand": "Apple",
     "description": "iMac 24 英寸，M4 芯片，4.5K Retina 显示屏，P3 广色域。一体化设计。",
     "attributes": {"品牌": "Apple", "处理器": "M4", "内存": "16GB", "存储": "256GB SSD", "屏幕": "24英寸 4.5K Retina"}},
    {"name": "戴森 V15 Detect 无绳吸尘器", "price": 4990, "category": "家电", "brand": "戴森",
     "description": "戴森 V15 Detect，激光探测微尘，声学传感器计数，230AW 吸力，60 分钟续航。",
     "attributes": {"品牌": "戴森", "类型": "无绳吸尘器", "吸力": "230AW", "续航": "60分钟"}},
    {"name": "戴森 Supersonic 吹风机", "price": 2990, "category": "家电", "brand": "戴森",
     "description": "戴森 Supersonic，V9 数码马达，智能温控，5 款风嘴。",
     "attributes": {"品牌": "戴森", "类型": "吹风机", "马达": "V9", "功率": "1600W"}},
    {"name": "索尼 A7M4 全画幅微单相机", "price": 16999, "category": "相机", "brand": "索尼",
     "description": "索尼 A7M4，3300 万像素全画幅 CMOS，BIONZ XR，759 点对焦，4K 120p 视频。",
     "attributes": {"品牌": "索尼", "传感器": "全画幅CMOS", "像素": "3300万", "视频": "4K120p"}},
    {"name": "佳能 EOS R6 Mark II 全画幅微单", "price": 17999, "category": "相机", "brand": "佳能",
     "description": "佳能 EOS R6 Mark II，2420 万像素全画幅，40fps 连拍，4K 60p，8 级防抖。",
     "attributes": {"品牌": "佳能", "传感器": "全画幅CMOS", "像素": "2420万", "连拍": "40fps"}},
    {"name": "OPPO Find X8 Pro 256GB", "price": 5299, "category": "手机", "brand": "OPPO",
     "description": "OPPO Find X8 Pro，天玑 9400，哈苏影像，6.78 英寸 AMOLED，5910mAh。",
     "attributes": {"品牌": "OPPO", "屏幕": "6.78英寸 AMOLED", "处理器": "天玑9400", "存储": "256GB"}},
    {"name": "vivo X200 Pro 256GB", "price": 4999, "category": "手机", "brand": "vivo",
     "description": "vivo X200 Pro，天玑 9400，蔡司 APO 长焦，6.78 英寸 AMOLED，6000mAh。",
     "attributes": {"品牌": "vivo", "屏幕": "6.78英寸 AMOLED", "处理器": "天玑9400", "存储": "256GB"}},
    {"name": "华为 MatePad Pro 13.2英寸 256GB", "price": 5199, "category": "平板电脑", "brand": "华为",
     "description": "华为 MatePad Pro 13.2，OLED 柔性屏，M-Pencil，PC 级 WPS。",
     "attributes": {"品牌": "华为", "屏幕": "13.2英寸 OLED", "处理器": "麒麟9000s", "存储": "256GB"}},
    {"name": "美的 大1.5匹 变频空调 一级能效", "price": 3299, "category": "家电", "brand": "美的",
     "description": "美的风酷变频空调，大1.5匹，一级能效，全直流变频，WiFi 控制，自清洁。",
     "attributes": {"品牌": "美的", "类型": "壁挂空调", "匹数": "1.5匹", "能效": "一级"}},
    {"name": "海尔 500L 双开门冰箱", "price": 4599, "category": "家电", "brand": "海尔",
     "description": "海尔双开门冰箱，500L，风冷无霜，双变频，一级能效，DEO 净味。",
     "attributes": {"品牌": "海尔", "类型": "双开门冰箱", "容量": "500L", "能效": "一级"}},
    {"name": "格力 云佳 1.5匹 变频空调", "price": 3599, "category": "家电", "brand": "格力",
     "description": "格力云佳变频空调，1.5匹，一级能效，全直流变频，静音设计。",
     "attributes": {"品牌": "格力", "类型": "壁挂空调", "匹数": "1.5匹", "能效": "一级"}},
    {"name": "Bose QuietComfort 消噪耳机", "price": 2299, "category": "耳机", "brand": "Bose",
     "description": "Bose QC 消噪耳机，10 级可控降噪，24 小时续航，Bose 音乐应用。",
     "attributes": {"品牌": "Bose", "类型": "头戴式", "降噪": "10级可控", "续航": "24小时"}},
    {"name": "荣耀 Magic7 Pro 256GB", "price": 4999, "category": "手机", "brand": "荣耀",
     "description": "荣耀 Magic7 Pro，骁龙 8 Elite，6.78 英寸 OLED，5850mAh，100W 快充。",
     "attributes": {"品牌": "荣耀", "屏幕": "6.78英寸 OLED", "处理器": "骁龙8 Elite", "存储": "256GB"}},
    {"name": "戴尔 XPS 15 笔记本电脑", "price": 13999, "category": "笔记本电脑", "brand": "戴尔",
     "description": "戴尔 XPS 15，Intel Core Ultra 9，32GB DDR5，1TB SSD，15.6英寸 3.5K OLED。",
     "attributes": {"品牌": "戴尔", "处理器": "Intel Core Ultra 9", "内存": "32GB", "存储": "1TB SSD", "屏幕": "15.6英寸 3.5K OLED"}},
    {"name": "Apple Mac mini M4 256GB", "price": 5999, "category": "台式电脑", "brand": "Apple",
     "description": "Mac mini，M4 芯片，12.7cm 见方超小机身，支持多台显示器。",
     "attributes": {"品牌": "Apple", "处理器": "M4", "内存": "16GB", "存储": "256GB SSD"}},
    {"name": "尼康 Z6III 全画幅微单", "price": 18999, "category": "相机", "brand": "尼康",
     "description": "尼康 Z6III，2450万像素，4K 120p，部分堆栈式CMOS，EXPEED 7。",
     "attributes": {"品牌": "尼康", "传感器": "全画幅CMOS", "像素": "2450万", "视频": "4K120p"}},
    {"name": "索尼 KD-65X95L 65英寸 4K 电视", "price": 8999, "category": "家电", "brand": "索尼",
     "description": "索尼 65英寸 4K HDR 电视，XR 认知芯片，全阵列 LED，120Hz 刷新率。",
     "attributes": {"品牌": "索尼", "尺寸": "65英寸", "分辨率": "4K", "刷新率": "120Hz"}},
    {"name": "Apple AirPods Max 银色", "price": 4399, "category": "耳机", "brand": "Apple",
     "description": "AirPods Max，H1 芯片，高保真音质，主动降噪，空间音频，20小时续航。",
     "attributes": {"品牌": "Apple", "类型": "头戴式", "降噪": "主动降噪", "续航": "20小时"}},
    {"name": "小米电视 S Pro 75英寸 Mini LED", "price": 5999, "category": "家电", "brand": "小米",
     "description": "小米电视 S Pro 75英寸，Mini LED 背光，144Hz 刷新率，4K HDR。",
     "attributes": {"品牌": "小米", "尺寸": "75英寸", "技术": "Mini LED", "刷新率": "144Hz"}},
    {"name": "华为 Watch GT 5 Pro", "price": 2988, "category": "智能手表", "brand": "华为",
     "description": "华为 Watch GT 5 Pro，钛金属表壳，AMOLED 屏幕，14天续航，高尔夫模式。",
     "attributes": {"品牌": "华为", "续航": "14天", "防水": "5ATM", "传感器": "心率+血氧"}},
    {"name": "三星 Galaxy Tab S10 Ultra", "price": 8999, "category": "平板电脑", "brand": "三星",
     "description": "三星 Galaxy Tab S10 Ultra，14.6英寸 AMOLED，骁龙 8 Gen 3，S Pen  included。",
     "attributes": {"品牌": "三星", "屏幕": "14.6英寸 AMOLED", "处理器": "骁龙8 Gen3", "存储": "256GB"}},
    {"name": "OPPO Watch 5 Pro", "price": 1999, "category": "智能手表", "brand": "OPPO",
     "description": "OPPO Watch 5 Pro，骁龙 W5+恒玄 2700 双芯，1.5英寸 AMOLED，eSIM 独立通话。",
     "attributes": {"品牌": "OPPO", "屏幕": "1.5英寸 AMOLED", "续航": "5天智能/10天轻智能"}},
    {"name": "美的 洗烘一体机 10KG", "price": 3999, "category": "家电", "brand": "美的",
     "description": "美的洗烘一体机，10KG洗涤+7KG烘干，BLDC变频电机，蒸汽除菌。",
     "attributes": {"品牌": "美的", "类型": "洗烘一体", "容量": "10KG", "电机": "BLDC变频"}},
    {"name": "佳能 EOS R50 微单相机", "price": 5999, "category": "相机", "brand": "佳能",
     "description": "佳能 EOS R50，2420万像素 APS-C，4K 30p 视频，眼部检测对焦。",
     "attributes": {"品牌": "佳能", "传感器": "APS-C CMOS", "像素": "2420万", "视频": "4K30p"}},
    {"name": "联想 拯救者 Y9000P 2025", "price": 10999, "category": "笔记本电脑", "brand": "联想",
     "description": "联想拯救者 Y9000P，i9-14900HX，RTX 4070，32GB DDR5，1TB SSD，16英寸 2.5K 240Hz。",
     "attributes": {"品牌": "联想", "处理器": "i9-14900HX", "显卡": "RTX 4070", "内存": "32GB", "屏幕": "16英寸 2.5K 240Hz"}},
]

def generate_png(width, height, r, g, b):
    """快速生成简单PNG图片"""
    def chunk(ctype, data):
        c = ctype + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
    
    raw = b''
    for y in range(height):
        raw += b'\x00'  # filter byte
        for x in range(width):
            # 简单渐变
            rr = min(255, (r + x * 80 // width) & 0xFF)
            gg = min(255, (g + y * 80 // height) & 0xFF)
            bb = b
            raw += bytes([rr, gg, bb])
    
    compressed = zlib.compress(raw, 1)
    
    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0))
    png += chunk(b'IDAT', compressed)
    png += chunk(b'IEND', b'')
    return png

# 颜色映射
COLORS = {
    "手机": (30, 60, 180), "笔记本电脑": (60, 30, 150), "平板电脑": (100, 50, 200),
    "耳机": (150, 30, 80), "智能手表": (30, 120, 60), "台式电脑": (80, 80, 80),
    "家电": (20, 100, 150), "相机": (120, 60, 30),
}

print("=" * 50)
print("商品数据生成器 v2 (整数 _id)")
print("=" * 50)

# 生成基础图片
print("\n生成商品图片...")
img_cache = {}
for p in PRODUCTS:
    cat = p['category']
    brand = p['brand']
    key = f"{cat}_{brand}"
    if key not in img_cache:
        color = COLORS.get(cat, (100, 100, 100))
        h = hashlib.md5(key.encode()).hexdigest()
        r = (color[0] + int(h[:2], 16) // 3) % 256
        g = (color[1] + int(h[2:4], 16) // 3) % 256
        b = (color[2] + int(h[4:6], 16) // 3) % 256
        img_cache[key] = generate_png(100, 100, r, g, b)
        print(f"  生成图片: {key} ({len(img_cache[key])} bytes)")

print(f"共生成 {len(img_cache)} 张图片")

# 生成商品数据，分批输出
BATCH_SIZE_MB = 40  # 每批40MB
MAX_SIZE_MB = 550   # 总共550MB
batch_num = 0
total_products = 0
total_size = 0

# 颜色变体
VARIANT_COLORS = [
    (255, 100, 100), (100, 255, 100), (100, 100, 255),
    (255, 255, 100), (255, 100, 255), (100, 255, 255),
    (200, 150, 50), (150, 50, 200), (50, 200, 150),
    (255, 150, 50), (150, 255, 50), (50, 150, 255),
    (200, 200, 200), (100, 100, 100), (50, 50, 50),
    (255, 200, 200), (200, 255, 200), (200, 200, 255),
    (180, 120, 60), (60, 180, 120),
]

product_id = 1
variant_idx = 0

while total_size < MAX_SIZE_MB * 1024 * 1024:
    batch_num += 1
    batch_docs = []
    batch_bytes = 0
    
    while batch_bytes < BATCH_SIZE_MB * 1024 * 1024 and total_size < MAX_SIZE_MB * 1024 * 1024:
        for base_p in PRODUCTS:
            if batch_bytes >= BATCH_SIZE_MB * 1024 * 1024:
                break
            if total_size >= MAX_SIZE_MB * 1024 * 1024:
                break
            
            cat = base_p['category']
            brand = base_p['brand']
            img_key = f"{cat}_{brand}"
            
            # 生成变体
            vc = VARIANT_COLORS[variant_idx % len(VARIANT_COLORS)]
            variant_img = generate_png(80, 80, vc[0], vc[1], vc[2])
            img_b64 = base64.b64encode(variant_img).decode('utf-8')
            
            suffix = f" {variant_idx + 1}号"
            price_var = base_p['price'] + random.randint(-500, 500)
            if price_var < 99:
                price_var = 99
            
            doc = {
                "_id": product_id,
                "id": product_id,
                "name": base_p['name'] + suffix,
                "price": price_var,
                "stock": random.randint(10, 500),
                "category": cat,
                "merchantId": (product_id % 5) + 1,
                "description": base_p['description'],
                "imageUrl": f"/images/products/{product_id}.jpg",
                "imageData": f"data:image/png;base64,{img_b64}",
                "attributes": dict(base_p['attributes']),
            }
            
            batch_docs.append(doc)
            batch_bytes += len(json.dumps(doc, ensure_ascii=False))
            product_id += 1
            variant_idx += 1
    
    # 写入批次文件
    filename = f"/tmp/products_batch_{batch_num}.json"
    print(f"\n写入批次 {batch_num}: {len(batch_docs)} 个商品...")
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(batch_docs, f, ensure_ascii=False)
    
    file_size = os.path.getsize(filename) / 1024 / 1024
    total_size += file_size * 1024 * 1024
    total_products += len(batch_docs)
    print(f"  文件大小: {file_size:.1f} MB")
    print(f"  累计: {total_products} 个商品, {total_size / 1024 / 1024:.1f} MB")
    
    if total_size >= MAX_SIZE_MB * 1024 * 1024:
        break

print(f"\n{'=' * 50}")
print(f"生成完成！")
print(f"总批次: {batch_num}")
print(f"总商品数: {total_products}")
print(f"总数据大小: {total_size / 1024 / 1024:.1f} MB")
print(f"{'=' * 50}")

# 生成导入脚本
import_script = """#!/bin/bash
echo "开始导入商品数据..."

# 删除旧数据
mongosh --quiet /tmp/run_js.js <<'EOF'
db = db.getSiblingDB("ecommerce");
db.products.drop();
print("旧数据已删除");
EOF

"""

for i in range(1, batch_num + 1):
    import_script += f"""
echo "导入批次 {i}..."
mongosh --quiet /tmp/run_js.js <<'EOF{i}'
db = db.getSiblingDB("ecommerce");
var data = JSON.parse(cat("/tmp/products_batch_{i}.json"));
db.products.insertMany(data);
print("批次 {i} 导入完成: " + data.length + " 条");
EOF{i}

"""

import_script += """
echo "导入完成！验证..."
mongosh --quiet /tmp/run_js.js <<'VERIFY'
db = db.getSiblingDB("ecommerce");
var count = db.products.countDocuments();
var stats = db.products.stats();
print("商品数量: " + count);
print("数据大小: " + (stats.totalSize / 1024 / 1024).toFixed(2) + " MB");
printjson(db.products.findOne());
VERIFY
"""

with open('/tmp/import_batches.sh', 'w') as f:
    f.write(import_script)

print(f"\n导入脚本已生成: /tmp/import_batches.sh")
