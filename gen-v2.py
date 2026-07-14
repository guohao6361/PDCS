#!/usr/bin/env python3
"""生成商品数据（整数_id），不含base64图片，分批导入"""
import json, random, os, sys, struct, zlib, hashlib, base64

# ============ 真实商品数据 ============
PRODUCTS = [
    {"name": "Apple iPhone 16 Pro Max 256GB 原色钛金属", "price": 9999, "category": "手机", "brand": "Apple",
     "description": "Apple iPhone 16 Pro Max，搭载 A18 Pro 芯片，6.9 英寸超视网膜 XDR 显示屏，支持 ProMotion 自适应刷新率最高 120Hz。4800 万像素融合摄像头系统，支持 5 倍光学变焦。钛金属设计，IP68 级防水。支持 USB-C 接口和 Wi-Fi 7。Face ID 面部识别，激光雷达扫描仪。",
     "attributes": {"品牌": "Apple", "屏幕": "6.9英寸 OLED", "处理器": "A18 Pro", "存储": "256GB", "内存": "8GB", "摄像头": "4800万主摄+1200万超广角+1200万长焦", "电池": "4685mAh", "系统": "iOS 18", "重量": "227g", "防水": "IP68", "5G": "支持", "充电": "USB-C/ MagSafe无线", "生物识别": "Face ID"}},
    {"name": "Apple iPhone 16 Pro 128GB 沙漠钛金属", "price": 7999, "category": "手机", "brand": "Apple",
     "description": "Apple iPhone 16 Pro，A18 Pro 芯片，6.3 英寸超视网膜 XDR 显示屏。Pro 级摄像头系统，支持微距摄影和 ProRAW。钛金属设计，轻薄耐用。相机控制按钮，一键启动相机。",
     "attributes": {"品牌": "Apple", "屏幕": "6.3英寸 OLED", "处理器": "A18 Pro", "存储": "128GB", "摄像头": "4800万融合摄像头", "电池": "3274mAh", "系统": "iOS 18", "重量": "199g", "防水": "IP68"}},
    {"name": "Apple iPhone 16 128GB 群青色", "price": 5999, "category": "手机", "brand": "Apple",
     "description": "Apple iPhone 16，A18 芯片，6.1 英寸超视网膜 XDR 显示屏。4800 万像素双摄系统，支持空间照片拍摄。操作按钮和相机控制按钮。",
     "attributes": {"品牌": "Apple", "屏幕": "6.1英寸 OLED", "处理器": "A18", "存储": "128GB", "摄像头": "4800万双摄", "系统": "iOS 18", "重量": "170g"}},
    {"name": "华为 Mate 70 Pro 256GB 雅丹黑", "price": 6499, "category": "手机", "brand": "华为",
     "description": "华为 Mate 70 Pro，麒麟 9020 芯片，6.9 英寸 OLED 曲面屏。XMAGE 影像系统，5000 万像素超感知主摄，支持 100 倍变焦。HarmonyOS 4，灵犀通信，卫星消息。",
     "attributes": {"品牌": "华为", "屏幕": "6.9英寸 OLED曲面", "处理器": "麒麟9020", "存储": "256GB", "摄像头": "5000万XMAGE", "电池": "5700mAh", "系统": "HarmonyOS 4", "快充": "100W有线+80W无线"}},
    {"name": "小米 15 Ultra 512GB 黑色", "price": 5999, "category": "手机", "brand": "小米",
     "description": "小米 15 Ultra，骁龙 8 Elite，徕卡光学镜头。2K 120Hz LTPO AMOLED 屏幕，6000mAh 大电池，120W 有线快充+50W 无线快充。",
     "attributes": {"品牌": "小米", "屏幕": "6.73英寸 AMOLED 2K", "处理器": "骁龙8 Elite", "存储": "512GB", "摄像头": "5000万徕卡光学", "电池": "6000mAh", "快充": "120W"}},
    {"name": "三星 Galaxy S25 Ultra 256GB 钛灰", "price": 9999, "category": "手机", "brand": "三星",
     "description": "三星 Galaxy S25 Ultra，骁龙 8 Elite，2 亿像素摄像头，6.9 英寸 Dynamic AMOLED 2X。S Pen 手写笔，钛金属框架，Galaxy AI。",
     "attributes": {"品牌": "三星", "屏幕": "6.9英寸 AMOLED", "处理器": "骁龙8 Elite", "存储": "256GB", "摄像头": "2亿像素", "电池": "5000mAh", "特色": "S Pen+Galaxy AI"}},
    {"name": "Apple MacBook Air 13英寸 M4 星光色 256GB", "price": 9999, "category": "笔记本电脑", "brand": "Apple",
     "description": "MacBook Air 13 英寸，Apple M4 芯片（8核CPU+10核GPU），16GB 统一内存，256GB SSD。13.6 英寸 Liquid Retina 显示屏，500 尼特亮度，P3 广色域。MagSafe 充电，两个雷雳 4 端口。18 小时电池续航，无风扇设计。",
     "attributes": {"品牌": "Apple", "处理器": "M4 (8核CPU+10核GPU)", "内存": "16GB统一内存", "存储": "256GB SSD", "屏幕": "13.6英寸 Liquid Retina 500nit", "电池": "18小时", "重量": "1.24kg", "接口": "MagSafe+2x雷雳4+3.5mm耳机"}},
    {"name": "Apple MacBook Pro 14英寸 M4 Pro 深空黑", "price": 15999, "category": "笔记本电脑", "brand": "Apple",
     "description": "MacBook Pro 14 英寸，M4 Pro 芯片（14核CPU+20核GPU），24GB 统一内存，512GB SSD。14.2 英寸 Liquid Retina XDR，峰值 1600 尼特。22 小时续航。",
     "attributes": {"品牌": "Apple", "处理器": "M4 Pro (14核CPU+20核GPU)", "内存": "24GB统一内存", "存储": "512GB SSD", "屏幕": "14.2英寸 Liquid Retina XDR", "电池": "22小时", "重量": "1.55kg"}},
    {"name": "Apple iPad Pro 13英寸 M4 256GB", "price": 10799, "category": "平板电脑", "brand": "Apple",
     "description": "iPad Pro 13 英寸，M4 芯片，Ultra Retina XDR 显示屏（串联 OLED），ProMotion。支持 Apple Pencil Pro 和妙控键盘。",
     "attributes": {"品牌": "Apple", "处理器": "M4", "存储": "256GB", "屏幕": "13英寸 Ultra Retina XDR OLED", "重量": "579g"}},
    {"name": "Apple AirPods Pro 2 (USB-C)", "price": 1899, "category": "耳机", "brand": "Apple",
     "description": "AirPods Pro 2，H2 芯片，自适应音频，个性化空间音频，主动降噪（2倍）。USB-C 充电盒，精确查找。",
     "attributes": {"品牌": "Apple", "类型": "入耳式", "降噪": "主动降噪", "连接": "蓝牙5.3", "续航": "6+30小时", "防水": "IP54"}},
    {"name": "索尼 WH-1000XM5 黑色头戴式降噪耳机", "price": 2499, "category": "耳机", "brand": "索尼",
     "description": "索尼 WH-1000XM5，双芯片降噪，30 小时续航，LDAC 高解析音频，30mm 驱动单元。",
     "attributes": {"品牌": "索尼", "类型": "头戴式", "降噪": "HD降噪QN1", "续航": "30小时", "重量": "250g"}},
    {"name": "Apple Watch Ultra 2 GPS+蜂窝 49mm", "price": 6499, "category": "智能手表", "brand": "Apple",
     "description": "Apple Watch Ultra 2，49mm 钛金属，3000 尼特显示屏，双频 GPS，100 米防水。",
     "attributes": {"品牌": "Apple", "尺寸": "49mm", "材质": "钛金属", "防水": "100米", "电池": "36小时"}},
    {"name": "Apple iMac 24英寸 M4 蓝色 256GB", "price": 12499, "category": "台式电脑", "brand": "Apple",
     "description": "iMac 24 英寸，M4 芯片，4.5K Retina 显示屏，P3 广色域。七种配色，一体化设计。",
     "attributes": {"品牌": "Apple", "处理器": "M4", "内存": "16GB", "存储": "256GB SSD", "屏幕": "24英寸 4.5K Retina"}},
    {"name": "戴森 V15 Detect 无绳吸尘器", "price": 4990, "category": "家电", "brand": "戴森",
     "description": "戴森 V15 Detect，激光探测微尘，声学传感器计数，230AW 吸力，60 分钟续航。",
     "attributes": {"品牌": "戴森", "类型": "无绳吸尘器", "吸力": "230AW", "续航": "60分钟"}},
    {"name": "索尼 A7M4 全画幅微单相机", "price": 16999, "category": "相机", "brand": "索尼",
     "description": "索尼 A7M4，3300 万像素全画幅 CMOS，BIONZ XR，759 点对焦，4K 120p 视频，5 轴防抖。",
     "attributes": {"品牌": "索尼", "传感器": "全画幅CMOS", "像素": "3300万", "视频": "4K120p", "防抖": "5轴"}},
    {"name": "佳能 EOS R6 Mark II 全画幅微单", "price": 17999, "category": "相机", "brand": "佳能",
     "description": "佳能 EOS R6 Mark II，2420 万像素全画幅，40fps 连拍，4K 60p，8 级防抖。",
     "attributes": {"品牌": "佳能", "传感器": "全画幅CMOS", "像素": "2420万", "连拍": "40fps", "视频": "4K60p"}},
    {"name": "OPPO Find X8 Pro 256GB", "price": 5299, "category": "手机", "brand": "OPPO",
     "description": "OPPO Find X8 Pro，天玑 9400，哈苏影像，6.78 英寸 AMOLED，5910mAh。",
     "attributes": {"品牌": "OPPO", "屏幕": "6.78英寸 AMOLED", "处理器": "天玑9400", "存储": "256GB", "电池": "5910mAh"}},
    {"name": "美的 大1.5匹 变频空调 一级能效", "price": 3299, "category": "家电", "brand": "美的",
     "description": "美的风酷变频空调，大1.5匹，一级能效，全直流变频，WiFi 控制，自清洁。",
     "attributes": {"品牌": "美的", "类型": "壁挂空调", "匹数": "1.5匹", "能效": "一级", "变频": "全直流"}},
    {"name": "海尔 500L 双开门冰箱", "price": 4599, "category": "家电", "brand": "海尔",
     "description": "海尔双开门冰箱，500L，风冷无霜，双变频，一级能效，DEO 净味。",
     "attributes": {"品牌": "海尔", "类型": "双开门冰箱", "容量": "500L", "能效": "一级"}},
    {"name": "联想 ThinkPad X1 Carbon Gen 12", "price": 12999, "category": "笔记本电脑", "brand": "联想",
     "description": "ThinkPad X1 Carbon Gen 12，英特尔酷睿 Ultra 7 165H，32GB LPDDR5x，1TB SSD。14 英寸 2.8K OLED，400 尼特。碳纤维材质，1.08kg 超轻。",
     "attributes": {"品牌": "联想", "处理器": "Intel Core Ultra 7 165H", "内存": "32GB LPDDR5x", "存储": "1TB PCIe Gen4 SSD", "屏幕": "14英寸 2.8K OLED", "重量": "1.08kg"}},
    {"name": "华为 MateBook X Pro 2025", "price": 11999, "category": "笔记本电脑", "brand": "华为",
     "description": "华为 MateBook X Pro 2025，酷睿 Ultra 9，32GB 内存，2TB SSD。14.2 英寸 3.1K OLED 柔性触控屏，超级终端。",
     "attributes": {"品牌": "华为", "处理器": "Intel Core Ultra 9", "内存": "32GB", "存储": "2TB SSD", "屏幕": "14.2英寸 3.1K OLED触控", "重量": "0.98kg"}},
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
    {"name": "vivo X200 Pro 256GB", "price": 4999, "category": "手机", "brand": "vivo",
     "description": "vivo X200 Pro，天玑 9400，蔡司 APO 长焦，6.78 英寸 AMOLED，6000mAh。",
     "attributes": {"品牌": "vivo", "屏幕": "6.78英寸 AMOLED", "处理器": "天玑9400", "存储": "256GB", "电池": "6000mAh"}},
    {"name": "华为 MatePad Pro 13.2英寸 256GB", "price": 5199, "category": "平板电脑", "brand": "华为",
     "description": "华为 MatePad Pro 13.2，OLED 柔性屏，M-Pencil，PC 级 WPS。",
     "attributes": {"品牌": "华为", "屏幕": "13.2英寸 OLED", "处理器": "麒麟9000s", "存储": "256GB"}},
    {"name": "戴森 Supersonic 吹风机", "price": 2990, "category": "家电", "brand": "戴森",
     "description": "戴森 Supersonic，V9 数码马达，智能温控，5 款风嘴。",
     "attributes": {"品牌": "戴森", "类型": "吹风机", "马达": "V9", "功率": "1600W"}},
    {"name": "索尼 KD-65X95L 65英寸 4K 电视", "price": 8999, "category": "家电", "brand": "索尼",
     "description": "索尼 65英寸 4K HDR 电视，XR 认知芯片，全阵列 LED，120Hz 刷新率。",
     "attributes": {"品牌": "索尼", "尺寸": "65英寸", "分辨率": "4K", "刷新率": "120Hz"}},
    {"name": "Apple Mac mini M4 256GB", "price": 5999, "category": "台式电脑", "brand": "Apple",
     "description": "Mac mini，M4 芯片，12.7cm 见方超小机身，支持多台显示器。",
     "attributes": {"品牌": "Apple", "处理器": "M4", "内存": "16GB", "存储": "256GB SSD", "重量": "0.67kg"}},
    {"name": "尼康 Z6III 全画幅微单", "price": 18999, "category": "相机", "brand": "尼康",
     "description": "尼康 Z6III，2450万像素，4K 120p，部分堆栈式CMOS，EXPEED 7。",
     "attributes": {"品牌": "尼康", "传感器": "全画幅CMOS", "像素": "2450万", "视频": "4K120p"}},
    {"name": "小米电视 S Pro 75英寸 Mini LED", "price": 5999, "category": "家电", "brand": "小米",
     "description": "小米电视 S Pro 75英寸，Mini LED 背光，144Hz 刷新率，4K HDR。",
     "attributes": {"品牌": "小米", "尺寸": "75英寸", "技术": "Mini LED", "刷新率": "144Hz"}},
    {"name": "华为 Watch GT 5 Pro", "price": 2988, "category": "智能手表", "brand": "华为",
     "description": "华为 Watch GT 5 Pro，钛金属表壳，AMOLED 屏幕，14天续航，高尔夫模式。",
     "attributes": {"品牌": "华为", "续航": "14天", "防水": "5ATM"}},
    {"name": "三星 Galaxy Tab S10 Ultra", "price": 8999, "category": "平板电脑", "brand": "三星",
     "description": "三星 Galaxy Tab S10 Ultra，14.6英寸 AMOLED，骁龙 8 Gen 3，S Pen。",
     "attributes": {"品牌": "三星", "屏幕": "14.6英寸 AMOLED", "处理器": "骁龙8 Gen3", "存储": "256GB"}},
    {"name": "Apple AirPods Max 银色", "price": 4399, "category": "耳机", "brand": "Apple",
     "description": "AirPods Max，H1 芯片，高保真音质，主动降噪，空间音频，20小时续航。",
     "attributes": {"品牌": "Apple", "类型": "头戴式", "降噪": "主动降噪", "续航": "20小时"}},
    {"name": "美的 洗烘一体机 10KG", "price": 3999, "category": "家电", "brand": "美的",
     "description": "美的洗烘一体机，10KG洗涤+7KG烘干，BLDC变频电机，蒸汽除菌。",
     "attributes": {"品牌": "美的", "类型": "洗烘一体", "容量": "10KG", "电机": "BLDC变频"}},
    {"name": "OPPO Watch 5 Pro", "price": 1999, "category": "智能手表", "brand": "OPPO",
     "description": "OPPO Watch 5 Pro，骁龙 W5+恒玄 2700 双芯，1.5英寸 AMOLED，eSIM。",
     "attributes": {"品牌": "OPPO", "屏幕": "1.5英寸 AMOLED", "续航": "5天智能"}},
    {"name": "联想 拯救者 Y9000P 2025", "price": 10999, "category": "笔记本电脑", "brand": "联想",
     "description": "联想拯救者 Y9000P，i9-14900HX，RTX 4070，32GB DDR5，1TB SSD，16英寸 2.5K 240Hz。",
     "attributes": {"品牌": "联想", "处理器": "i9-14900HX", "显卡": "RTX 4070", "内存": "32GB", "屏幕": "16英寸 2.5K 240Hz"}},
    {"name": "佳能 EOS R50 微单相机", "price": 5999, "category": "相机", "brand": "佳能",
     "description": "佳能 EOS R50，2420万像素 APS-C，4K 30p 视频，眼部检测对焦。",
     "attributes": {"品牌": "佳能", "传感器": "APS-C CMOS", "像素": "2420万", "视频": "4K30p"}},
    {"name": "Apple MacBook Air 15英寸 M4 天蓝色 512GB", "price": 12999, "category": "笔记本电脑", "brand": "Apple",
     "description": "MacBook Air 15 英寸，M4 芯片，15.3 英寸 Liquid Retina 显示屏。六扬声器系统，空间音频。",
     "attributes": {"品牌": "Apple", "处理器": "M4", "内存": "16GB", "存储": "512GB SSD", "屏幕": "15.3英寸 Liquid Retina"}},
]

def gen_small_png(r, g, b, size=50):
    """生成小PNG"""
    def chunk(ct, d):
        c = ct + d
        return struct.pack('>I', len(d)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
    raw = b''
    for y in range(size):
        raw += b'\x00'
        for x in range(size):
            raw += bytes([min(255, r + x), min(255, g + y), b])
    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0))
    png += chunk(b'IDAT', zlib.compress(raw, 1))
    png += chunk(b'IEND', b'')
    return png

# 生成每种分类的默认图片
print("生成商品图片...")
cat_colors = {
    "手机": (30, 60, 180), "笔记本电脑": (60, 30, 150), "平板电脑": (100, 50, 200),
    "耳机": (150, 30, 80), "智能手表": (30, 120, 60), "台式电脑": (80, 80, 80),
    "家电": (20, 100, 150), "相机": (120, 60, 30),
}
cat_imgs = {}
for cat, color in cat_colors.items():
    cat_imgs[cat] = base64.b64encode(gen_small_png(*color, 50)).decode()
    print(f"  {cat}: {len(cat_imgs[cat])} chars base64")

# 目标大小
TARGET_MB = 550
BATCH_MB = 20  # 每批20MB

product_id = 1
batch_num = 0
total_size = 0
total_count = 0
random.seed(42)

print(f"\n目标: {TARGET_MB}MB, 每批: {BATCH_MB}MB")
print("=" * 50)

while total_size < TARGET_MB * 1024 * 1024:
    batch_num += 1
    batch_docs = []
    batch_bytes = 0
    
    while batch_bytes < BATCH_MB * 1024 * 1024:
        for p in PRODUCTS:
            if batch_bytes >= BATCH_MB * 1024 * 1024:
                break
            
            cat = p['category']
            img_b64 = cat_imgs.get(cat, cat_imgs.get("手机", ""))
            price_var = p['price'] + random.randint(-200, 200)
            if price_var < 99:
                price_var = 99
            
            doc = {
                "_id": product_id,
                "id": product_id,
                "name": f"{p['name']} [{product_id}]",
                "price": price_var,
                "stock": random.randint(10, 500),
                "category": cat,
                "merchantId": (product_id % 5) + 1,
                "description": p['description'],
                "imageUrl": f"/images/products/{product_id}.jpg",
                "imageData": f"data:image/png;base64,{img_b64}",
                "attributes": dict(p['attributes']),
            }
            
            batch_docs.append(doc)
            doc_size = len(json.dumps(doc, ensure_ascii=False))
            batch_bytes += doc_size
            product_id += 1
    
    # 写文件
    fname = f"/tmp/batch_{batch_num}.json"
    with open(fname, 'w', encoding='utf-8') as f:
        json.dump(batch_docs, f, ensure_ascii=False)
    
    fsize = os.path.getsize(fname)
    total_size += fsize
    total_count += len(batch_docs)
    print(f"批次 {batch_num}: {len(batch_docs)} 条, {fsize/1024/1024:.1f}MB | 累计: {total_count} 条, {total_size/1024/1024:.1f}MB")

print(f"\n{'='*50}")
print(f"完成! {batch_num} 批次, {total_count} 个商品, {total_size/1024/1024:.1f}MB")

# 生成导入脚本
with open('/tmp/do_import.sh', 'w') as f:
    f.write("#!/bin/bash\n")
    f.write("echo '=== 删除旧数据 ==='\n")
    f.write("cat > /tmp/clean.js << 'JSEOF'\ndb = db.getSiblingDB(\"ecommerce\");\ndb.products.drop();\nprint(\"deleted\");\nJSEOF\n")
    f.write("mongosh --quiet /tmp/clean.js\n\n")
    
    for i in range(1, batch_num + 1):
        f.write(f"echo '=== 导入批次 {i}/{batch_num} ==='\n")
        f.write(f"cat > /tmp/imp{i}.js << 'JSEOF'\n")
        f.write(f'db = db.getSiblingDB("ecommerce");\n')
        f.write(f'var data = JSON.parse(cat("/tmp/batch_{i}.json"));\n')
        f.write(f'db.products.insertMany(data);\n')
        f.write(f'print("batch {i}: " + data.length + " imported");\n')
        f.write(f"JSEOF\n")
        f.write(f"mongosh --quiet /tmp/imp{i}.js\n\n")
    
    f.write("echo '=== 验证 ==='\n")
    f.write("cat > /tmp/verify.js << 'JSEOF'\n")
    f.write('db = db.getSiblingDB("ecommerce");\n')
    f.write("var c = db.products.countDocuments();\n")
    f.write("var s = db.products.stats();\n")
    f.write('print("count: " + c);\n')
    f.write('print("size: " + (s.totalSize/1024/1024).toFixed(2) + " MB");\n')
    f.write("printjson(db.products.findOne());\n")
    f.write("JSEOF\n")
    f.write("mongosh --quiet /tmp/verify.js\n")

print(f"导入脚本: /tmp/do_import.sh")
