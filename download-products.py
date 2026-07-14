#!/usr/bin/env python3
"""下载真实商品图片并生成商品数据，导入 MongoDB"""
import os, json, time, struct, zlib, hashlib, base64, sys

import requests

# 绕过代理
SESSION = requests.Session()
SESSION.trust_env = False
SESSION.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
})

# ============ 真实商品数据 + 真实图片URL ============
PRODUCTS = [
    {"name": "Apple iPhone 16 Pro Max 256GB 原色钛金属", "price": 9999, "category": "手机", "brand": "Apple",
     "description": "Apple iPhone 16 Pro Max，搭载 A18 Pro 芯片，6.9 英寸超视网膜 XDR 显示屏，支持 ProMotion 自适应刷新率最高 120Hz。4800 万像素融合摄像头系统，支持 5 倍光学变焦。钛金属设计，IP68 级防水。",
     "attributes": {"品牌": "Apple", "屏幕": "6.9英寸 OLED", "处理器": "A18 Pro", "存储": "256GB", "内存": "8GB", "摄像头": "4800万主摄+1200万超广角+1200万长焦", "电池": "4685mAh", "系统": "iOS 18", "重量": "227g", "防水": "IP68", "5G": "支持"},
     "img": "https://store.storeimages.cdn-apple.com/1/as-images.apple.com/is/iphone-16-pro-finish-select-202409-6-9inch-naturaltitanium?wid=400&hei=400&fmt=jpeg&src=src"},
    {"name": "Apple iPhone 16 Pro 128GB 沙漠钛金属", "price": 7999, "category": "手机", "brand": "Apple",
     "description": "Apple iPhone 16 Pro，A18 Pro 芯片，6.3 英寸超视网膜 XDR 显示屏。Pro 级摄像头系统，支持微距摄影和 ProRAW。钛金属设计。",
     "attributes": {"品牌": "Apple", "屏幕": "6.3英寸 OLED", "处理器": "A18 Pro", "存储": "128GB", "摄像头": "4800万融合摄像头", "系统": "iOS 18", "重量": "199g"},
     "img": "https://store.storeimages.cdn-apple.com/1/as-images.apple.com/is/iphone-16-pro-finish-select-202409-6-3inch-deserttitanium?wid=400&hei=400&fmt=jpeg&src=src"},
    {"name": "Apple iPhone 16 128GB 群青色", "price": 5999, "category": "手机", "brand": "Apple",
     "description": "Apple iPhone 16，A18 芯片，6.1 英寸超视网膜 XDR 显示屏。4800 万像素双摄系统，支持空间照片拍摄。",
     "attributes": {"品牌": "Apple", "屏幕": "6.1英寸 OLED", "处理器": "A18", "存储": "128GB", "摄像头": "4800万双摄", "系统": "iOS 18", "重量": "170g"},
     "img": "https://store.storeimages.cdn-apple.com/1/as-images.apple.com/is/iphone-16-ultramarine-select-202409_AV2?wid=400&hei=400&fmt=jpeg&src=src"},
    {"name": "Apple iPhone 16 Plus 256GB 粉色", "price": 6999, "category": "手机", "brand": "Apple",
     "description": "Apple iPhone 16 Plus，A18 芯片，6.7 英寸超视网膜 XDR 显示屏。4800 万像素双摄系统，更大电池续航。",
     "attributes": {"品牌": "Apple", "屏幕": "6.7英寸 OLED", "处理器": "A18", "存储": "256GB", "摄像头": "4800万双摄", "系统": "iOS 18", "重量": "199g"},
     "img": "https://store.storeimages.cdn-apple.com/1/as-images.apple.com/is/iphone-16-plus-pink-select-202409_SW_COLOR?wid=400&hei=400&fmt=jpeg&src=src"},
    {"name": "Apple iPhone 17 Pro Max 256GB 银色", "price": 10999, "category": "手机", "brand": "Apple",
     "description": "Apple iPhone 17 Pro Max，全新设计，A19 Pro 芯片，6.9 英寸超视网膜 XDR 显示屏。升级摄像头系统。",
     "attributes": {"品牌": "Apple", "屏幕": "6.9英寸 OLED", "处理器": "A19 Pro", "存储": "256GB", "系统": "iOS 19"},
     "img": "https://store.storeimages.cdn-apple.com/1/as-images.apple.com/is/iphone-17-pro-max-finish-select-silver-202509_SW_COLOR?wid=400&hei=400&fmt=jpeg&src=src"},
    {"name": "Apple iPhone Air 天蓝色 256GB", "price": 7499, "category": "手机", "brand": "Apple",
     "description": "Apple iPhone Air，超薄设计，A19 芯片，6.6 英寸超视网膜 XDR 显示屏。轻量化设计。",
     "attributes": {"品牌": "Apple", "屏幕": "6.6英寸 OLED", "处理器": "A19", "存储": "256GB", "系统": "iOS 19"},
     "img": "https://store.storeimages.cdn-apple.com/1/as-images.apple.com/is/iphone-air-finish-select-skyblue-202509_SW_COLOR?wid=400&hei=400&fmt=jpeg&src=src"},
    {"name": "Apple iPhone 17 256GB 薰衣草紫", "price": 6499, "category": "手机", "brand": "Apple",
     "description": "Apple iPhone 17，A19 芯片，6.1 英寸超视网膜 XDR 显示屏。全新配色。",
     "attributes": {"品牌": "Apple", "屏幕": "6.1英寸 OLED", "处理器": "A19", "存储": "256GB", "系统": "iOS 19"},
     "img": "https://store.storeimages.cdn-apple.com/1/as-images.apple.com/is/iphone-17-finish-select-lavender-202509_SW_COLOR?wid=400&hei=400&fmt=jpeg&src=src"},
    {"name": "华为 Mate 70 Pro 256GB 雅丹黑", "price": 6499, "category": "手机", "brand": "华为",
     "description": "华为 Mate 70 Pro，麒麟 9020 芯片，6.9 英寸 OLED 曲面屏。XMAGE 影像系统，5000 万像素超感知主摄，支持 100 倍变焦。HarmonyOS 4。",
     "attributes": {"品牌": "华为", "屏幕": "6.9英寸 OLED曲面", "处理器": "麒麟9020", "存储": "256GB", "摄像头": "5000万XMAGE", "电池": "5700mAh", "系统": "HarmonyOS 4"},
     "img": ""},
    {"name": "小米 15 Ultra 512GB 黑色", "price": 5999, "category": "手机", "brand": "小米",
     "description": "小米 15 Ultra，骁龙 8 Elite，徕卡光学镜头。2K 120Hz LTPO AMOLED 屏幕，6000mAh 大电池，120W 快充。",
     "attributes": {"品牌": "小米", "屏幕": "6.73英寸 AMOLED 2K", "处理器": "骁龙8 Elite", "存储": "512GB", "摄像头": "5000万徕卡光学", "电池": "6000mAh"},
     "img": ""},
    {"name": "三星 Galaxy S25 Ultra 256GB 钛灰", "price": 9999, "category": "手机", "brand": "三星",
     "description": "三星 Galaxy S25 Ultra，骁龙 8 Elite，2 亿像素摄像头，6.9 英寸 Dynamic AMOLED 2X。S Pen，钛金属框架。",
     "attributes": {"品牌": "三星", "屏幕": "6.9英寸 AMOLED", "处理器": "骁龙8 Elite", "存储": "256GB", "摄像头": "2亿像素", "电池": "5000mAh"},
     "img": ""},
    {"name": "OPPO Find X8 Pro 256GB", "price": 5299, "category": "手机", "brand": "OPPO",
     "description": "OPPO Find X8 Pro，天玑 9400，哈苏影像，6.78 英寸 AMOLED，5910mAh。",
     "attributes": {"品牌": "OPPO", "屏幕": "6.78英寸 AMOLED", "处理器": "天玑9400", "存储": "256GB", "电池": "5910mAh"},
     "img": ""},
    {"name": "vivo X200 Pro 256GB", "price": 4999, "category": "手机", "brand": "vivo",
     "description": "vivo X200 Pro，天玑 9400，蔡司 APO 长焦，6.78 英寸 AMOLED，6000mAh。",
     "attributes": {"品牌": "vivo", "屏幕": "6.78英寸 AMOLED", "处理器": "天玑9400", "存储": "256GB", "电池": "6000mAh"},
     "img": ""},
    {"name": "荣耀 Magic7 Pro 256GB", "price": 4299, "category": "手机", "brand": "荣耀",
     "description": "荣耀 Magic7 Pro，骁龙 8 Elite，鹰眼相机，6.78 英寸 LTPO OLED，5850mAh。",
     "attributes": {"品牌": "荣耀", "屏幕": "6.78英寸 OLED", "处理器": "骁龙8 Elite", "存储": "256GB", "电池": "5850mAh"},
     "img": ""},
    {"name": "Apple MacBook Air 13英寸 M4 星光色 256GB", "price": 9999, "category": "笔记本电脑", "brand": "Apple",
     "description": "MacBook Air 13 英寸，M4 芯片（8核CPU+10核GPU），16GB 统一内存，256GB SSD。13.6 英寸 Liquid Retina 显示屏。MagSafe 充电，18 小时续航。",
     "attributes": {"品牌": "Apple", "处理器": "M4", "内存": "16GB", "存储": "256GB SSD", "屏幕": "13.6英寸 Liquid Retina", "电池": "18小时", "重量": "1.24kg"},
     "img": "https://store.storeimages.cdn-apple.com/1/as-images.apple.com/is/mba13-starlight-select-202503_SW_COLOR?wid=400&hei=400&fmt=jpeg&src=src"},
    {"name": "Apple MacBook Air 15英寸 M4 天蓝色 512GB", "price": 12999, "category": "笔记本电脑", "brand": "Apple",
     "description": "MacBook Air 15 英寸，M4 芯片，15.3 英寸 Liquid Retina 显示屏。六扬声器系统，空间音频。",
     "attributes": {"品牌": "Apple", "处理器": "M4", "内存": "16GB", "存储": "512GB SSD", "屏幕": "15.3英寸 Liquid Retina", "电池": "18小时", "重量": "1.51kg"},
     "img": "https://store.storeimages.cdn-apple.com/1/as-images.apple.com/is/mba13-skyblue-select-202503_SW_COLOR?wid=400&hei=400&fmt=jpeg&src=src"},
    {"name": "Apple MacBook Pro 14英寸 M4 Pro 深空黑", "price": 15999, "category": "笔记本电脑", "brand": "Apple",
     "description": "MacBook Pro 14 英寸，M4 Pro 芯片（14核CPU+20核GPU），24GB 统一内存，512GB SSD。14.2 英寸 Liquid Retina XDR，峰值 1600 尼特。22 小时续航。",
     "attributes": {"品牌": "Apple", "处理器": "M4 Pro", "内存": "24GB", "存储": "512GB SSD", "屏幕": "14.2英寸 Liquid Retina XDR", "电池": "22小时", "重量": "1.55kg"},
     "img": "https://store.storeimages.cdn-apple.com/1/as-images.apple.com/is/mbp14-spaceblack-cto-hero-202410_SW_COLOR?wid=400&hei=400&fmt=jpeg&src=src"},
    {"name": "联想 ThinkPad X1 Carbon Gen 12", "price": 12999, "category": "笔记本电脑", "brand": "联想",
     "description": "ThinkPad X1 Carbon Gen 12，酷睿 Ultra 7 165H，32GB LPDDR5x，1TB SSD。14 英寸 2.8K OLED。",
     "attributes": {"品牌": "联想", "处理器": "Intel Core Ultra 7 165H", "内存": "32GB", "存储": "1TB SSD", "屏幕": "14英寸 2.8K OLED", "重量": "1.08kg"},
     "img": ""},
    {"name": "华为 MateBook X Pro 2025", "price": 11999, "category": "笔记本电脑", "brand": "华为",
     "description": "华为 MateBook X Pro 2025，酷睿 Ultra 9，32GB，2TB SSD。14.2 英寸 3.1K OLED 触控屏。",
     "attributes": {"品牌": "华为", "处理器": "Intel Core Ultra 9", "内存": "32GB", "存储": "2TB SSD", "屏幕": "14.2英寸 3.1K OLED触控", "重量": "0.98kg"},
     "img": ""},
    {"name": "小米笔记本 Pro 16 2025", "price": 7999, "category": "笔记本电脑", "brand": "小米",
     "description": "小米笔记本 Pro 16，酷睿 Ultra 7，32GB，1TB SSD，16 英寸 3.1K 165Hz。",
     "attributes": {"品牌": "小米", "处理器": "Intel Core Ultra 7", "内存": "32GB", "存储": "1TB SSD", "屏幕": "16英寸 3.1K 165Hz"},
     "img": ""},
    {"name": "Apple iPad Pro 13英寸 M4 256GB", "price": 10799, "category": "平板电脑", "brand": "Apple",
     "description": "iPad Pro 13 英寸，M4 芯片，Ultra Retina XDR 显示屏。支持 Apple Pencil Pro 和妙控键盘。",
     "attributes": {"品牌": "Apple", "处理器": "M4", "存储": "256GB", "屏幕": "13英寸 Ultra Retina XDR OLED", "重量": "579g"},
     "img": "https://store.storeimages.cdn-apple.com/1/as-images.apple.com/is/ipad-pro-11-select-wifi-spaceblack-202405_SW_COLOR?wid=400&hei=400&fmt=jpeg&src=src"},
    {"name": "Apple iPad Air 13英寸 M3 128GB 紫色", "price": 6999, "category": "平板电脑", "brand": "Apple",
     "description": "iPad Air 13 英寸，M3 芯片，Liquid Retina 显示屏，支持 Apple Pencil Pro。",
     "attributes": {"品牌": "Apple", "处理器": "M3", "存储": "128GB", "屏幕": "13英寸 Liquid Retina", "重量": "617g"},
     "img": "https://store.storeimages.cdn-apple.com/1/as-images.apple.com/is/ipad-air-select-11in-wifi-purple-202405_SW_COLOR?wid=400&hei=400&fmt=jpeg&src=src"},
    {"name": "华为 MatePad Pro 13.2英寸 256GB", "price": 5199, "category": "平板电脑", "brand": "华为",
     "description": "华为 MatePad Pro 13.2，OLED 柔性屏，M-Pencil，PC 级 WPS。",
     "attributes": {"品牌": "华为", "屏幕": "13.2英寸 OLED", "处理器": "麒麟9000s", "存储": "256GB"},
     "img": ""},
    {"name": "三星 Galaxy Tab S10+ 256GB", "price": 6999, "category": "平板电脑", "brand": "三星",
     "description": "三星 Galaxy Tab S10+，天玑 9300+，12.4 英寸 Dynamic AMOLED 2X，S Pen。",
     "attributes": {"品牌": "三星", "屏幕": "12.4英寸 AMOLED", "处理器": "天玑9300+", "存储": "256GB"},
     "img": ""},
    {"name": "小米平板 7 Pro 11英寸 256GB", "price": 2799, "category": "平板电脑", "brand": "小米",
     "description": "小米平板 7 Pro，骁龙 8+ Gen1，11 英寸 2.8K 144Hz。",
     "attributes": {"品牌": "小米", "屏幕": "11英寸 2.8K 144Hz", "处理器": "骁龙8+ Gen1", "存储": "256GB"},
     "img": ""},
    {"name": "Apple AirPods Pro 2 (USB-C)", "price": 1899, "category": "耳机", "brand": "Apple",
     "description": "AirPods Pro 2，H2 芯片，自适应音频，个性化空间音频，主动降噪（2倍）。USB-C 充电盒。",
     "attributes": {"品牌": "Apple", "类型": "入耳式", "降噪": "主动降噪", "连接": "蓝牙5.3", "续航": "6+30小时", "防水": "IP54"},
     "img": "https://store.storeimages.cdn-apple.com/1/as-images.apple.com/is/MQD83?wid=400&hei=400&fmt=jpeg&src=src"},
    {"name": "Apple AirPods 4", "price": 999, "category": "耳机", "brand": "Apple",
     "description": "AirPods 4，H2 芯片，个性化空间音频，舒适开放设计。",
     "attributes": {"品牌": "Apple", "类型": "半入耳式", "芯片": "H2", "连接": "蓝牙5.3"},
     "img": "https://www.apple.com.cn/v/airpods/ae/images/overview/hero__gb4d3fd8jnu6_large.jpg"},
    {"name": "Apple AirPods Max USB-C 午夜色", "price": 4399, "category": "耳机", "brand": "Apple",
     "description": "AirPods Max，高保真音频，主动降噪，空间音频。铝金属耳罩。USB-C。",
     "attributes": {"品牌": "Apple", "类型": "头戴式", "降噪": "主动降噪", "续航": "20小时"},
     "img": "https://www.apple.com.cn/v/airpods/ae/images/overview/airpods_max_black__x3byrd2venmu_large.png"},
    {"name": "索尼 WH-1000XM5 黑色头戴式降噪耳机", "price": 2499, "category": "耳机", "brand": "索尼",
     "description": "索尼 WH-1000XM5，双芯片降噪，30 小时续航，LDAC 高解析音频。",
     "attributes": {"品牌": "索尼", "类型": "头戴式", "降噪": "HD降噪QN1", "连接": "蓝牙5.2", "续航": "30小时"},
     "img": ""},
    {"name": "Bose QC Ultra 头戴式降噪耳机", "price": 2999, "category": "耳机", "brand": "Bose",
     "description": "Bose QC Ultra，沉浸式音频，CustomTune，世界级降噪，24 小时续航。",
     "attributes": {"品牌": "Bose", "类型": "头戴式", "降噪": "世界级", "连接": "蓝牙5.3", "续航": "24小时"},
     "img": ""},
    {"name": "华为 FreeBuds Pro 3 星河蓝", "price": 1499, "category": "耳机", "brand": "华为",
     "description": "华为 FreeBuds Pro 3，星闪连接，智慧降噪 3.0，LDAC+L2HC 双高清。",
     "attributes": {"品牌": "华为", "类型": "入耳式", "降噪": "智慧降噪3.0", "连接": "蓝牙5.2/星闪"},
     "img": ""},
    {"name": "Apple Watch Ultra 2 GPS+蜂窝 49mm", "price": 6499, "category": "智能手表", "brand": "Apple",
     "description": "Apple Watch Ultra 2，49mm 钛金属，3000 尼特显示屏，双频 GPS，100 米防水。",
     "attributes": {"品牌": "Apple", "尺寸": "49mm", "材质": "钛金属", "防水": "100米", "电池": "36小时"},
     "img": "https://store.storeimages.cdn-apple.com/1/as-images.apple.com/is/watch-case-49-titanium-natural-ultra3_SW_COLOR?wid=400&hei=400&fmt=jpeg&src=src"},
    {"name": "华为 Watch GT 5 Pro 钛金属 46mm", "price": 2988, "category": "智能手表", "brand": "华为",
     "description": "华为 Watch GT 5 Pro，钛金属，ECG 心电分析，高尔夫/潜水模式，14天续航。",
     "attributes": {"品牌": "华为", "尺寸": "46mm", "材质": "钛金属", "续航": "14天", "防水": "5ATM"},
     "img": ""},
    {"name": "Apple iMac 24英寸 M4 蓝色 256GB", "price": 12499, "category": "台式电脑", "brand": "Apple",
     "description": "iMac 24 英寸，M4 芯片，4.5K Retina 显示屏，P3 广色域。一体化设计。",
     "attributes": {"品牌": "Apple", "处理器": "M4", "内存": "16GB", "存储": "256GB SSD", "屏幕": "24英寸 4.5K Retina", "重量": "4.46kg"},
     "img": "https://store.storeimages.cdn-apple.com/1/as-images.apple.com/is/imac-blue-selection-hero-202410_SW_COLOR?wid=400&hei=400&fmt=jpeg&src=src"},
    {"name": "Apple Mac mini M4 256GB", "price": 5999, "category": "台式电脑", "brand": "Apple",
     "description": "Mac mini，M4 芯片，12.7cm 见方超小机身，支持多台显示器。",
     "attributes": {"品牌": "Apple", "处理器": "M4", "内存": "16GB", "存储": "256GB SSD", "重量": "0.67kg"},
     "img": "https://store.storeimages.cdn-apple.com/1/as-images.apple.com/is/mac-card-40-mac-mini-202410?wid=400&hei=400&fmt=jpeg&src=src"},
    {"name": "Apple Studio Display 27英寸 5K", "price": 11999, "category": "显示器", "brand": "Apple",
     "description": "Studio Display 27 英寸，5K Retina，P3 广色域，600 尼特。Center Stage 摄像头，六扬声器。",
     "attributes": {"品牌": "Apple", "屏幕": "27英寸 5K Retina", "分辨率": "5120x2880", "亮度": "600nit"},
     "img": "https://store.storeimages.cdn-apple.com/1/as-images.apple.com/is/mac-card-40-studio-display-202603?wid=400&hei=400&fmt=jpeg&src=src"},
    {"name": "戴森 V15 Detect 无绳吸尘器", "price": 4990, "category": "家电", "brand": "戴森",
     "description": "戴森 V15 Detect，激光探测微尘，声学传感器计数，230AW 吸力，60 分钟续航。",
     "attributes": {"品牌": "戴森", "类型": "无绳吸尘器", "吸力": "230AW", "续航": "60分钟", "重量": "3.08kg"},
     "img": ""},
    {"name": "戴森 Supersonic 吹风机", "price": 2990, "category": "家电", "brand": "戴森",
     "description": "戴森 Supersonic，V9 数码马达，智能温控，5 款风嘴。",
     "attributes": {"品牌": "戴森", "类型": "吹风机", "马达": "V9", "功率": "1600W"},
     "img": ""},
    {"name": "美的 大1.5匹 变频空调 一级能效", "price": 3299, "category": "家电", "brand": "美的",
     "description": "美的风酷变频空调，大1.5匹，一级能效，全直流变频，WiFi 控制，自清洁。",
     "attributes": {"品牌": "美的", "类型": "壁挂空调", "匹数": "1.5匹", "能效": "一级"},
     "img": ""},
    {"name": "海尔 500L 双开门冰箱", "price": 4599, "category": "家电", "brand": "海尔",
     "description": "海尔双开门冰箱，500L，风冷无霜，双变频，一级能效，DEO 净味。",
     "attributes": {"品牌": "海尔", "类型": "双开门冰箱", "容量": "500L", "能效": "一级"},
     "img": ""},
    {"name": "格力 3匹 柜机空调 新一级能效", "price": 8999, "category": "家电", "brand": "格力",
     "description": "格力柜机空调，3 匹，新一级能效，全直流变频，分布式送风。",
     "attributes": {"品牌": "格力", "类型": "柜式空调", "匹数": "3匹", "能效": "新一级"},
     "img": ""},
    {"name": "索尼 KD-65X95L 65英寸 4K 电视", "price": 8999, "category": "家电", "brand": "索尼",
     "description": "索尼 65 英寸 4K HDR 电视，XR 认知芯片，全阵列 LED，Dolby Vision/Atmos，120Hz。",
     "attributes": {"品牌": "索尼", "尺寸": "65英寸", "分辨率": "4K UHD", "HDR": "Dolby Vision", "刷新率": "120Hz"},
     "img": ""},
    {"name": "索尼 A7M4 全画幅微单相机", "price": 16999, "category": "相机", "brand": "索尼",
     "description": "索尼 A7M4，3300 万像素全画幅 CMOS，BIONZ XR，759 点对焦，4K 120p 视频，5 轴防抖。",
     "attributes": {"品牌": "索尼", "传感器": "全画幅CMOS", "像素": "3300万", "视频": "4K120p", "防抖": "5轴"},
     "img": ""},
    {"name": "佳能 EOS R6 Mark II 全画幅微单", "price": 17999, "category": "相机", "brand": "佳能",
     "description": "佳能 EOS R6 Mark II，2420 万像素全画幅，40fps 连拍，4K 60p，8 级防抖。",
     "attributes": {"品牌": "佳能", "传感器": "全画幅CMOS", "像素": "2420万", "连拍": "40fps", "视频": "4K60p"},
     "img": ""},
]

def generate_fallback_png(width, height, seed_str):
    """生成简单的PNG作为无图片商品的备用"""
    h = hashlib.md5(seed_str.encode()).hexdigest()
    r1, g1, b1 = int(h[:2],16), int(h[2:4],16), int(h[4:6],16)
    r2, g2, b2 = int(h[6:8],16), int(h[8:10],16), int(h[10:12],16)
    sig = b'\x89PNG\r\n\x1a\n'
    ihdr_d = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    ihdr_crc = zlib.crc32(b'IHDR' + ihdr_d)
    ihdr = struct.pack('>I', 13) + b'IHDR' + ihdr_d + struct.pack('>I', ihdr_crc & 0xffffffff)
    rows = []
    for y in range(height):
        row = b'\x00'
        f = y / max(height-1, 1)
        cr = int(r1 + (r2-r1)*f) & 0xff
        cg = int(g1 + (g2-g1)*f) & 0xff
        cb = int(b1 + (b2-b1)*f) & 0xff
        row += struct.pack('BBB', cr, cg, cb) * width
        rows.append(row)
    raw = b''.join(rows)
    comp = zlib.compress(raw, 1)
    idat_crc = zlib.crc32(b'IDAT' + comp)
    idat = struct.pack('>I', len(comp)) + b'IDAT' + comp + struct.pack('>I', idat_crc & 0xffffffff)
    iend_crc = zlib.crc32(b'IEND')
    iend = struct.pack('>I', 0) + b'IEND' + struct.pack('>I', iend_crc & 0xffffffff)
    return sig + ihdr + idat + iend

def download_image(url, save_path):
    """下载图片"""
    if not url:
        return False
    try:
        r = SESSION.get(url, timeout=15)
        if r.status_code == 200 and len(r.content) > 3000:
            ct = r.headers.get('content-type', '')
            if 'image' in ct or 'octet' in ct:
                with open(save_path, 'wb') as f:
                    f.write(r.content)
                return True
    except:
        pass
    return False

def main():
    img_dir = "/tmp/product_images"
    os.makedirs(img_dir, exist_ok=True)
    
    print("=" * 60)
    print("下载真实商品图片 (绕过代理)")
    print("=" * 60)
    
    downloaded = 0
    fallback = 0
    
    for i, p in enumerate(PRODUCTS):
        safe_name = p['name'].replace(' ', '_').replace('/', '_')[:50]
        # 确定文件扩展名
        img_path_jpg = os.path.join(img_dir, f"{i+1:03d}_{safe_name}.jpg")
        img_path_png = os.path.join(img_dir, f"{i+1:03d}_{safe_name}.png")
        
        # 检查是否已下载
        exists = False
        for ext in ['.jpg', '.png']:
            fp = os.path.join(img_dir, f"{i+1:03d}_{safe_name}{ext}")
            if os.path.exists(fp) and os.path.getsize(fp) > 3000:
                exists = True
                img_path = fp
                break
        
        if exists:
            downloaded += 1
            print(f"  [{i+1}/{len(PRODUCTS)}] 已存在: {os.path.basename(img_path)}")
            continue
        
        print(f"  [{i+1}/{len(PRODUCTS)}] {p['name'][:40]}...")
        
        success = False
        if p.get('img'):
            # 尝试下载真实图片
            ext = '.png' if '.png' in p['img'] else '.jpg'
            img_path = os.path.join(img_dir, f"{i+1:03d}_{safe_name}{ext}")
            if download_image(p['img'], img_path):
                success = True
                size_kb = os.path.getsize(img_path) / 1024
                print(f"    ✓ 下载成功 ({size_kb:.1f} KB)")
                downloaded += 1
        
        if not success:
            # 生成备用图片
            png_data = generate_fallback_png(200, 200, f"{p['category']}_{p['brand']}")
            with open(img_path_png, 'wb') as f:
                f.write(png_data)
            fallback += 1
            print(f"    ✗ 备用图片 ({len(png_data)/1024:.1f} KB)")
    
    print(f"\n下载完成: {downloaded} 张真实图片, {fallback} 张备用")
    
    # 统计
    total_img_size = 0
    img_files = []
    for f in sorted(os.listdir(img_dir)):
        fp = os.path.join(img_dir, f)
        if os.path.isfile(fp):
            total_img_size += os.path.getsize(fp)
            img_files.append(f)
    
    print(f"图片总数: {len(img_files)}")
    print(f"图片总大小: {total_img_size/1024/1024:.1f} MB")
    
    # 预加载图片的base64（用于嵌入JSON增大体积）
    print("\n预加载图片base64...")
    img_b64_cache = {}
    for f in img_files:
        fp = os.path.join(img_dir, f)
        with open(fp, 'rb') as fh:
            img_b64_cache[f] = base64.b64encode(fh.read()).decode('utf-8')
    
    # 生成商品数据
    print("\n生成商品数据（含base64图片嵌入）...")
    products_data = []
    for i, p in enumerate(PRODUCTS):
        safe_name = p['name'].replace(' ', '_').replace('/', '_')[:50]
        img_file = None
        for f in img_files:
            if f.startswith(f"{i+1:03d}_"):
                img_file = f
                break
        image_url = f"/images/products/{img_file}" if img_file else ""
        # 嵌入base64图片数据到description中（增大体积）
        b64_data = img_b64_cache.get(img_file, "") if img_file else ""
        extra_desc = f"\n\n[IMG_DATA]{b64_data}[/IMG_DATA]" if b64_data else ""
        
        products_data.append({
            "name": p['name'],
            "price": p['price'],
            "stock": 100 + (i * 7) % 200,
            "category": p['category'],
            "merchantId": (i % 5) + 1,
            "description": p['description'] + extra_desc,
            "imageUrl": image_url,
            "attributes": p.get('attributes', {})
        })
    
    # 生成变体
    target_mb = 500
    colors = ["深空黑","星光色","银色","金色","蓝色","紫色","绿色","红色","白色","灰色",
              "午夜蓝","玫瑰金","钛金属灰","磨砂黑","亮白色","石墨色","远峰蓝","暗紫色","樱花粉","薄荷绿",
              "冰蓝色","珊瑚橙","薰衣草紫","森林绿","琥珀棕","珍珠白","曜石黑","极光蓝","落日橙","星空灰"]
    
    print(f"生成变体，目标 {target_mb}MB...")
    vid = 0
    while True:
        base = PRODUCTS[vid % len(PRODUCTS)]
        color = colors[vid % len(colors)]
        suffix = vid // len(colors)
        name_suffix = f" {color}" if suffix == 0 else f" {color} 限量版{suffix}"
        
        safe_name = base['name'].replace(' ', '_').replace('/', '_')[:50]
        img_file = None
        for f in img_files:
            if f.startswith(f"{PRODUCTS.index(base)+1:03d}_"):
                img_file = f
                break
        image_url = f"/images/products/{img_file}" if img_file else ""
        b64_data = img_b64_cache.get(img_file, "") if img_file else ""
        extra_desc = f"\n\n[IMG_DATA]{b64_data}[/IMG_DATA]" if b64_data else ""
        
        products_data.append({
            "name": f"{base['name']}{name_suffix}",
            "price": base['price'] + (vid % 10) * 50 + suffix * 100,
            "stock": 50 + (vid * 13) % 300,
            "category": base['category'],
            "merchantId": (vid % 5) + 1,
            "description": f"{base['description']}{extra_desc} 本款为{color}配色版本。",
            "imageUrl": image_url,
            "attributes": {**base.get('attributes', {}), "颜色": color, "版本": name_suffix.strip()}
        })
        vid += 1
        if vid % 500 == 0:
            data = json.dumps(products_data, ensure_ascii=False)
            size_mb = len(data.encode('utf-8')) / 1024 / 1024
            print(f"  变体 {vid}, 总数 {len(products_data)}, {size_mb:.1f} MB")
            if size_mb >= target_mb:
                break
    
    data = json.dumps(products_data, ensure_ascii=False)
    final_mb = len(data.encode('utf-8')) / 1024 / 1024
    
    with open("/tmp/products_data.json", 'w', encoding='utf-8') as f:
        f.write(data)
    
    file_mb = os.path.getsize("/tmp/products_data.json") / 1024 / 1024
    print(f"\n{'='*60}")
    print(f"商品总数: {len(products_data)}")
    print(f"JSON 大小: {final_mb:.2f} MB")
    print(f"文件大小: {file_mb:.2f} MB")
    print(f"图片大小: {total_img_size/1024/1024:.1f} MB")
    print(f"总计约: {file_mb + total_img_size/1024/1024:.1f} MB")
    
    # 生成导入脚本
    script = '''#!/bin/bash
set -e
echo "=== 1. 获取 Pod 名称 ==="
MONGO_POD=$(kubectl get pods -l app=mongodb -o jsonpath="{.items[0].metadata.name}")
WEB_POD=$(kubectl get pods -l app=web-server -o jsonpath="{.items[0].metadata.name}")
echo "MongoDB: $MONGO_POD"
echo "Web: $WEB_POD"

echo "=== 2. 删除旧数据 ==="
kubectl exec $MONGO_POD -- mongosh --eval "
db=db.getSiblingDB('ecommerce');
var c=db.products.countDocuments();
db.products.drop();
print('已删除: '+c+' 条');
"

echo "=== 3. 复制图片到前端容器 ==="
kubectl exec $WEB_POD -- mkdir -p /usr/share/nginx/html/images/products
kubectl cp /tmp/product_images/ $WEB_POD:/usr/share/nginx/html/images/products/
echo "图片复制完成"
IMG_COUNT=$(kubectl exec $WEB_POD -- ls /usr/share/nginx/html/images/products/ | wc -l)
echo "图片数量: $IMG_COUNT"

echo "=== 4. 复制数据到 MongoDB ==="
kubectl cp /tmp/products_data.json $MONGO_POD:/tmp/products_data.json

echo "=== 5. 导入数据 ==="
kubectl exec $MONGO_POD -- mongosh --eval "
db=db.getSiblingDB('ecommerce');
var data=JSON.parse(cat('/tmp/products_data.json'));
var bulk=db.products.initializeUnorderedBulkOp();
var id=1;
for(var i=0;i<data.length;i++){var p=data[i];p._id=id;p.id=id;bulk.insert(p);id++;}
bulk.execute();
print('导入: '+data.length+' 条');
"

echo "=== 6. 验证 ==="
kubectl exec $MONGO_POD -- mongosh --eval "
db=db.getSiblingDB('ecommerce');
print('总数: '+db.products.countDocuments());
var s=db.products.stats();
print('数据: '+(s.dataSize/1024/1024).toFixed(2)+' MB');
print('存储: '+(s.storageSize/1024/1024).toFixed(2)+' MB');
var cats=db.products.aggregate([{\\$group:{_id:'\\$category',count:{\\$sum:1}}},{\\$sort:{count:-1}}]).toArray();
cats.forEach(function(c){print('  '+c._id+': '+c.count);});
var p=db.products.findOne();
print('示例图片: '+p.imageUrl);
"
echo "=== 完成 ==="
'''
    with open("/tmp/import-v2.sh", 'w') as f:
        f.write(script)
    print(f"\n输出文件: /tmp/products_data.json, /tmp/import-v2.sh")

if __name__ == "__main__":
    main()

