#!/usr/bin/env python3
"""快速生成大量商品数据（含图片），达到 500MB"""
import json, base64, time, sys, os, struct, zlib, hashlib, random
import requests

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
    {"name": "Apple iPhone 15 128GB 蓝色", "price": 4999, "category": "手机", "brand": "Apple",
     "description": "Apple iPhone 15，A16 Bionic 芯片，6.1 英寸超视网膜 XDR 显示屏。灵动岛，4800 万像素主摄，USB-C 接口。",
     "attributes": {"品牌": "Apple", "屏幕": "6.1英寸 OLED", "处理器": "A16 Bionic", "存储": "128GB", "摄像头": "4800万像素", "系统": "iOS 17"}},
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
    {"name": "Apple MacBook Air 15英寸 M4 天蓝色 512GB", "price": 12999, "category": "笔记本电脑", "brand": "Apple",
     "description": "MacBook Air 15 英寸，M4 芯片，15.3 英寸 Liquid Retina 显示屏。六扬声器系统，空间音频。更大屏幕，同样轻薄。",
     "attributes": {"品牌": "Apple", "处理器": "M4", "内存": "16GB", "存储": "512GB SSD", "屏幕": "15.3英寸 Liquid Retina", "电池": "18小时", "重量": "1.51kg"}},
    {"name": "Apple MacBook Pro 14英寸 M4 Pro 深空黑", "price": 15999, "category": "笔记本电脑", "brand": "Apple",
     "description": "MacBook Pro 14 英寸，M4 Pro 芯片（14核CPU+20核GPU），24GB 统一内存，512GB SSD。14.2 英寸 Liquid Retina XDR，峰值 1600 尼特。22 小时续航。",
     "attributes": {"品牌": "Apple", "处理器": "M4 Pro (14核CPU+20核GPU)", "内存": "24GB统一内存", "存储": "512GB SSD", "屏幕": "14.2英寸 Liquid Retina XDR", "电池": "22小时", "重量": "1.55kg", "接口": "3x雷雳4+HDMI+SD+MagSafe"}},
    {"name": "联想 ThinkPad X1 Carbon Gen 12", "price": 12999, "category": "笔记本电脑", "brand": "联想",
     "description": "ThinkPad X1 Carbon Gen 12，英特尔酷睿 Ultra 7 165H，32GB LPDDR5x，1TB SSD。14 英寸 2.8K OLED，400 尼特。碳纤维材质，1.08kg 超轻。",
     "attributes": {"品牌": "联想", "处理器": "Intel Core Ultra 7 165H", "内存": "32GB LPDDR5x", "存储": "1TB PCIe Gen4 SSD", "屏幕": "14英寸 2.8K OLED", "重量": "1.08kg"}},
    {"name": "华为 MateBook X Pro 2025", "price": 11999, "category": "笔记本电脑", "brand": "华为",
     "description": "华为 MateBook X Pro 2025，酷睿 Ultra 9，32GB 内存，2TB SSD。14.2 英寸 3.1K OLED 柔性触控屏，超级终端。",
     "attributes": {"品牌": "华为", "处理器": "Intel Core Ultra 9", "内存": "32GB", "存储": "2TB SSD", "屏幕": "14.2英寸 3.1K OLED触控", "重量": "0.98kg"}},
    {"name": "Apple iPad Pro 13英寸 M4 256GB", "price": 10799, "category": "平板电脑", "brand": "Apple",
     "description": "iPad Pro 13 英寸，M4 芯片，Ultra Retina XDR 显示屏（串联 OLED），ProMotion。支持 Apple Pencil Pro 和妙控键盘。",
     "attributes": {"品牌": "Apple", "处理器": "M4", "存储": "256GB", "屏幕": "13英寸 Ultra Retina XDR OLED", "重量": "579g", "接口": "USB-C雷雳"}},
    {"name": "Apple iPad Air 13英寸 M3 128GB 紫色", "price": 6999, "category": "平板电脑", "brand": "Apple",
     "description": "iPad Air 13 英寸，M3 芯片，Liquid Retina 显示屏，支持 Apple Pencil Pro。",
     "attributes": {"品牌": "Apple", "处理器": "M3", "存储": "128GB", "屏幕": "13英寸 Liquid Retina", "重量": "617g"}},
    {"name": "Apple AirPods Pro 2 (USB-C)", "price": 1899, "category": "耳机", "brand": "Apple",
     "description": "AirPods Pro 2，H2 芯片，自适应音频，个性化空间音频，主动降噪（2倍）。USB-C 充电盒，精确查找。",
     "attributes": {"品牌": "Apple", "类型": "入耳式", "降噪": "主动降噪", "连接": "蓝牙5.3", "充电": "USB-C/MagSafe", "续航": "6+30小时", "防水": "IP54"}},
    {"name": "索尼 WH-1000XM5 黑色头戴式降噪耳机", "price": 2499, "category": "耳机", "brand": "索尼",
     "description": "索尼 WH-1000XM5，双芯片降噪，30 小时续航，LDAC 高解析音频，30mm 驱动单元。",
     "attributes": {"品牌": "索尼", "类型": "头戴式", "降噪": "HD降噪QN1", "连接": "蓝牙5.2", "续航": "30小时", "重量": "250g"}},
    {"name": "Apple Watch Ultra 2 GPS+蜂窝 49mm", "price": 6499, "category": "智能手表", "brand": "Apple",
     "description": "Apple Watch Ultra 2，49mm 钛金属，3000 尼特显示屏，双频 GPS，100 米防水。",
     "attributes": {"品牌": "Apple", "尺寸": "49mm", "材质": "钛金属", "防水": "100米", "电池": "36小时"}},
    {"name": "Apple iMac 24英寸 M4 蓝色 256GB", "price": 12499, "category": "台式电脑", "brand": "Apple",
     "description": "iMac 24 英寸，M4 芯片，4.5K Retina 显示屏，P3 广色域。七种配色，一体化设计。",
     "attributes": {"品牌": "Apple", "处理器": "M4", "内存": "16GB", "存储": "256GB SSD", "屏幕": "24英寸 4.5K Retina", "重量": "4.46kg"}},
    {"name": "Apple Mac mini M4 256GB", "price": 5999, "category": "台式电脑", "brand": "Apple",
     "description": "Mac mini，M4 芯片，12.7cm 见方超小机身，支持多台显示器。",
     "attributes": {"品牌": "Apple", "处理器": "M4", "内存": "16GB", "存储": "256GB SSD", "重量": "0.67kg"}},
    {"name": "戴森 V15 Detect 无绳吸尘器", "price": 4990, "category": "家电", "brand": "戴森",
     "description": "戴森 V15 Detect，激光探测微尘，声学传感器计数，230AW 吸力，60 分钟续航。",
     "attributes": {"品牌": "戴森", "类型": "无绳吸尘器", "吸力": "230AW", "续航": "60分钟", "重量": "3.08kg"}},
    {"name": "戴森 Supersonic 吹风机", "price": 2990, "category": "家电", "brand": "戴森",
     "description": "戴森 Supersonic，V9 数码马达，智能温控，5 款风嘴。",
     "attributes": {"品牌": "戴森", "类型": "吹风机", "马达": "V9", "功率": "1600W"}},
    {"name": "索尼 A7M4 全画幅微单相机", "price": 16999, "category": "相机", "brand": "索尼",
     "description": "索尼 A7M4，3300 万像素全画幅 CMOS，BIONZ XR，759 点对焦，4K 120p 视频，5 轴防抖。",
     "attributes": {"品牌": "索尼", "传感器": "全画幅CMOS", "像素": "3300万", "视频": "4K120p", "防抖": "5轴"}},
    {"name": "佳能 EOS R6 Mark II 全画幅微单", "price": 17999, "category": "相机", "brand": "佳能",
     "description": "佳能 EOS R6 Mark II，2420 万像素全画幅，40fps 连拍，4K 60p，8 级防抖。",
     "attributes": {"品牌": "佳能", "传感器": "全画幅CMOS", "像素": "2420万", "连拍": "40fps", "视频": "4K60p"}},
    {"name": "OPPO Find X8 Pro 256GB", "price": 5299, "category": "手机", "brand": "OPPO",
     "description": "OPPO Find X8 Pro，天玑 9400，哈苏影像，6.78 英寸 AMOLED，5910mAh。",
     "attributes": {"品牌": "OPPO", "屏幕": "6.78英寸 AMOLED", "处理器": "天玑9400", "存储": "256GB", "电池": "5910mAh"}},
    {"name": "vivo X200 Pro 256GB", "price": 4999, "category": "手机", "brand": "vivo",
     "description": "vivo X200 Pro，天玑 9400，蔡司 APO 长焦，6.78 英寸 AMOLED，6000mAh。",
     "attributes": {"品牌": "vivo", "屏幕": "6.78英寸 AMOLED", "处理器": "天玑9400", "存储": "256GB", "电池": "6000mAh"}},
    {"name": "华为 MatePad Pro 13.2英寸 256GB", "price": 5199, "category": "平板电脑", "brand": "华为",
     "description": "华为 MatePad Pro 13.2，OLED 柔性屏，M-Pencil，PC 级 WPS。",
     "attributes": {"品牌": "华为", "屏幕": "13.2英寸 OLED", "处理器": "麒麟9000s", "存储": "256GB"}},
    {"name": "美的 大1.5匹 变频空调 一级能效", "price": 3299, "category": "家电", "brand": "美的",
     "description": "美的风酷变频空调，大1.5匹，一级能效，全直流变频，WiFi 控制，自清洁。",
     "attributes": {"品牌": "美的", "类型": "壁挂空调", "匹数": "1.5匹", "能效": "一级", "变频": "全直流"}},
    {"name": "海尔 500L 双开门冰箱", "price": 4599, "category": "家电", "brand": "海尔",
     "description": "海尔双开门冰箱，500L，风冷无霜，双变频，一级能效，DEO 净味。",
     "attributes": {"品牌": "海尔", "类型": "双开门冰箱", "容量": "500L", "能效": "一级"}},
    {"name": "索尼 KD-65X95L 65英寸 4K 电视", "price": 8999, "category": "家电", "brand": "索尼",
     "description": "索尼 65 英寸 4K HDR 电视，XR 认知芯片，全阵列 LED，Dolby Vision/Atmos，120Hz。",
     "attributes": {"品牌": "索尼", "尺寸": "65英寸", "分辨率": "4K UHD", "HDR": "Dolby Vision", "刷新率": "120Hz"}},
    {"name": "Bose QC Ultra 头戴式降噪耳机", "price": 2999, "category": "耳机", "brand": "Bose",
     "description": "Bose QC Ultra，沉浸式音频，CustomTune，世界级降噪，24 小时续航。",
     "attributes": {"品牌": "Bose", "类型": "头戴式", "降噪": "世界级", "连接": "蓝牙5.3", "续航": "24小时"}},
    {"name": "华为 Watch GT 5 Pro 钛金属 46mm", "price": 2988, "category": "智能手表", "brand": "华为",
     "description": "华为 Watch GT 5 Pro，钛金属，ECG 心电分析，高尔夫/潜水模式，14天续航。",
     "attributes": {"品牌": "华为", "尺寸": "46mm", "材质": "钛金属", "续航": "14天", "防水": "5ATM"}},
    {"name": "三星 Galaxy Tab S10+ 256GB", "price": 6999, "category": "平板电脑", "brand": "三星",
     "description": "三星 Galaxy Tab S10+，天玑 9300+，12.4 英寸 Dynamic AMOLED 2X，S Pen。",
     "attributes": {"品牌": "三星", "屏幕": "12.4英寸 AMOLED", "处理器": "天玑9300+", "存储": "256GB", "特色": "S Pen"}},
    {"name": "荣耀 Magic7 Pro 256GB", "price": 4299, "category": "手机", "brand": "荣耀",
     "description": "荣耀 Magic7 Pro，骁龙 8 Elite，鹰眼相机，6.78 英寸 LTPO OLED，5850mAh。",
     "attributes": {"品牌": "荣耀", "屏幕": "6.78英寸 OLED", "处理器": "骁龙8 Elite", "存储": "256GB", "电池": "5850mAh"}},
    {"name": "小米笔记本 Pro 16 2025", "price": 7999, "category": "笔记本电脑", "brand": "小米",
     "description": "小米笔记本 Pro 16，酷睿 Ultra 7，32GB，1TB SSD，16 英寸 3.1K 165Hz。",
     "attributes": {"品牌": "小米", "处理器": "Intel Core Ultra 7", "内存": "32GB", "存储": "1TB SSD", "屏幕": "16英寸 3.1K 165Hz"}},
    {"name": "格力 3匹 柜机空调 新一级能效", "price": 8999, "category": "家电", "brand": "格力",
     "description": "格力柜机空调，3 匹，新一级能效，全直流变频，分布式送风。",
     "attributes": {"品牌": "格力", "类型": "柜式空调", "匹数": "3匹", "能效": "新一级"}},
    {"name": "小米平板 7 Pro 11英寸 256GB", "price": 2799, "category": "平板电脑", "brand": "小米",
     "description": "小米平板 7 Pro，骁龙 8+ Gen1，11 英寸 2.8K 144Hz，MIUI Pad。",
     "attributes": {"品牌": "小米", "屏幕": "11英寸 2.8K 144Hz", "处理器": "骁龙8+ Gen1", "存储": "256GB"}},
    {"name": "华为 FreeBuds Pro 3 星河蓝", "price": 1499, "category": "耳机", "brand": "华为",
     "description": "华为 FreeBuds Pro 3，星闪连接，智慧降噪 3.0，LDAC+L2HC 双高清。",
     "attributes": {"品牌": "华为", "类型": "入耳式", "降噪": "智慧降噪3.0", "连接": "蓝牙5.2/星闪"}},
    {"name": "Apple AirPods 4", "price": 999, "category": "耳机", "brand": "Apple",
     "description": "AirPods 4，H2 芯片，个性化空间音频，舒适开放设计。",
     "attributes": {"品牌": "Apple", "类型": "半入耳式", "芯片": "H2", "连接": "蓝牙5.3"}},
    {"name": "Apple AirPods Max USB-C 午夜色", "price": 4399, "category": "耳机", "brand": "Apple",
     "description": "AirPods Max，H1 芯片，高保真音频，主动降噪，空间音频。铝金属耳罩。",
     "attributes": {"品牌": "Apple", "类型": "头戴式", "降噪": "主动降噪", "续航": "20小时"}},
    {"name": "Apple Studio Display 27英寸 5K", "price": 11999, "category": "显示器", "brand": "Apple",
     "description": "Studio Display 27 英寸，5K Retina，P3 广色域，600 尼特。Center Stage 摄像头，六扬声器。",
     "attributes": {"品牌": "Apple", "屏幕": "27英寸 5K Retina", "分辨率": "5120x2880", "亮度": "600nit"}},
]

def generate_fast_png(width, height, seed_str):
    """快速生成一个简单但有效的 PNG（纯色+渐变，非常快）"""
    h = hashlib.md5(seed_str.encode()).hexdigest()
    r1, g1, b1 = int(h[:2],16), int(h[2:4],16), int(h[4:6],16)
    r2, g2, b2 = int(h[6:8],16), int(h[8:10],16), int(h[10:12],16)
    
    sig = b'\x89PNG\r\n\x1a\n'
    ihdr_d = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    ihdr_crc = zlib.crc32(b'IHDR' + ihdr_d)
    ihdr = struct.pack('>I', 13) + b'IHDR' + ihdr_d + struct.pack('>I', ihdr_crc & 0xffffffff)
    
    # 生成行数据（水平渐变 + 垂直渐变混合）
    rows = []
    for y in range(height):
        row = b'\x00'  # filter: None
        fy = y / max(height-1, 1)
        for x in range(width):
            fx = x / max(width-1, 1)
            f = (fx + fy) / 2
            cr = int(r1 + (r2-r1) * f) & 0xff
            cg = int(g1 + (g2-g1) * f) & 0xff
            cb = int(b1 + (b2-b1) * f) & 0xff
            row += struct.pack('BBB', cr, cg, cb)
        rows.append(row)
    
    raw = b''.join(rows)
    comp = zlib.compress(raw, 1)  # 快速压缩
    idat_crc = zlib.crc32(b'IDAT' + comp)
    idat = struct.pack('>I', len(comp)) + b'IDAT' + comp + struct.pack('>I', idat_crc & 0xffffffff)
    
    iend_crc = zlib.crc32(b'IEND')
    iend = struct.pack('>I', 0) + b'IEND' + struct.pack('>I', iend_crc & 0xffffffff)
    
    return sig + ihdr + idat + iend

def main():
    print("=" * 60)
    print("真实商品数据导入工具 v3")
    print("=" * 60)
    print(f"基础商品: {len(PRODUCTS)} 个")
    
    # 为每个基础商品生成图片（150x150，快速）
    print("\n生成商品图片...")
    base_images = {}
    for i, p in enumerate(PRODUCTS):
        cat = p['category']
        if cat not in base_images:
            print(f"  生成 {cat} 类图片...")
            base_images[cat] = generate_fast_png(150, 150, cat)
        # 也生成品牌特有图片
        key = f"{cat}_{p['brand']}"
        if key not in base_images:
            base_images[key] = generate_fast_png(150, 150, key)
    
    print(f"  共生成 {len(base_images)} 张图片")
    
    # 构建基础商品列表
    products = []
    for i, p in enumerate(PRODUCTS):
        key = f"{p['category']}_{p['brand']}"
        img = base_images.get(key, base_images[p['category']])
        img_b64 = base64.b64encode(img).decode('utf-8')
        
        products.append({
            "name": p['name'],
            "price": p['price'],
            "stock": 100 + (i * 7) % 200,
            "category": p['category'],
            "merchantId": (i % 5) + 1,
            "description": p['description'],
            "imageUrl": f"data:image/png;base64,{img_b64}",
            "attributes": p.get('attributes', {})
        })
    
    json_data = json.dumps(products, ensure_ascii=False)
    size_mb = len(json_data.encode('utf-8')) / 1024 / 1024
    print(f"\n基础数据大小: {size_mb:.2f} MB")
    
    # 生成变体达到 500MB
    target = 500
    colors = ["深空黑","星光色","银色","金色","蓝色","紫色","绿色","红色","白色","灰色",
              "午夜蓝","玫瑰金","钛金属灰","磨砂黑","亮白色","石墨色","远峰蓝","暗紫色","樱花粉","薄荷绿"]
    
    print(f"\n生成变体达到 {target}MB...")
    vidx = 0
    while size_mb < target:
        base = PRODUCTS[vidx % len(PRODUCTS)]
        color = colors[vidx % len(colors)]
        key = f"{base['category']}_{base['brand']}"
        img = base_images.get(key, base_images[base['category']])
        img_b64 = base64.b64encode(img).decode('utf-8')
        
        products.append({
            "name": f"{base['name']} {color}",
            "price": base['price'] + (vidx % 10) * 50,
            "stock": 50 + (vidx * 13) % 300,
            "category": base['category'],
            "merchantId": (vidx % 5) + 1,
            "description": f"{base['description']} 本款为{color}配色版本，品质保证，正品行货。",
            "imageUrl": f"data:image/png;base64,{img_b64}",
            "attributes": {**base.get('attributes', {}), "颜色": color}
        })
        vidx += 1
        if vidx % 1000 == 0:
            json_data = json.dumps(products, ensure_ascii=False)
            size_mb = len(json_data.encode('utf-8')) / 1024 / 1024
            print(f"  变体 {vidx}, 总数 {len(products)}, {size_mb:.1f} MB")
    
    json_data = json.dumps(products, ensure_ascii=False)
    final_mb = len(json_data.encode('utf-8')) / 1024 / 1024
    
    print(f"\n{'=' * 60}")
    print(f"最终统计:")
    print(f"  商品总数: {len(products)}")
    print(f"  数据大小: {final_mb:.2f} MB")
    
    with open("/tmp/products_import.json", 'w', encoding='utf-8') as f:
        f.write(json_data)
    fsize = os.path.getsize("/tmp/products_import.json") / 1024 / 1024
    print(f"  文件大小: {fsize:.2f} MB")
    
    # 导入脚本
    script = '''#!/bin/bash
MONGO_POD=$(kubectl get pods -l app=mongodb -o jsonpath="{.items[0].metadata.name}")
echo "=== 删除旧数据 ==="
kubectl exec $MONGO_POD -- mongosh --eval "db=db.getSiblingDB('ecommerce');var c=db.products.countDocuments();db.products.drop();print('已删除: '+c+' 条');"
echo "=== 复制数据 ==="
kubectl cp /tmp/products_import.json $MONGO_POD:/tmp/products_import.json
echo "=== 导入数据 ==="
kubectl exec $MONGO_POD -- mongosh --eval "
db=db.getSiblingDB('ecommerce');
var data=JSON.parse(cat('/tmp/products_import.json'));
var bulk=db.products.initializeUnorderedBulkOp();
var id=1;
for(var i=0;i<data.length;i++){var p=data[i];p._id=id;p.id=id;bulk.insert(p);id++;}
bulk.execute();
print('导入完成: '+data.length+' 条');
print('大小: '+(db.products.storageSize()/1024/1024).toFixed(2)+' MB');
"
echo "=== 验证 ==="
kubectl exec $MONGO_POD -- mongosh --eval "
db=db.getSiblingDB('ecommerce');
print('总数: '+db.products.countDocuments());
print('大小: '+(db.products.storageSize()/1024/1024).toFixed(2)+' MB');
var cats=db.products.aggregate([{\\$group:{_id:'\\$category',count:{\\$sum:1}}},{\\$sort:{count:-1}}]).toArray();
cats.forEach(function(c){print('  '+c._id+': '+c.count);});
"
echo "=== 完成 ==="
'''
    with open("/tmp/import-products.sh", 'w') as f:
        f.write(script)
    print(f"\n导入脚本: /tmp/import-products.sh")

if __name__ == "__main__":
    main()

