#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成电商商品测试数据集
符合项目中的 Product 实体格式
"""

import json
import random
from decimal import Decimal

# 商品类别
CATEGORIES = [
    "手机", "电脑", "平板", "耳机", "相机",
    "电视", "冰箱", "洗衣机", "空调", "微波炉",
    "书籍", "服装", "鞋子", "包包", "手表",
    "食品", "饮料", "化妆品", "玩具", "运动器材"
]

# 商品名称模板
PRODUCT_NAMES = {
    "手机": ["华为 Mate {} Pro", "小米 {} Ultra", "iPhone {}", "OPPO Find {}", "vivo X{}"],
    "电脑": ["联想 ThinkPad {}", "戴尔 XPS {}", "MacBook Pro {}寸", "华为 MateBook {}", "华硕 ROG {}"],
    "平板": ["iPad Pro {}寸", "华为 MatePad {}", "小米平板 {}", "Surface Pro {}", "三星 Tab {}"],
    "耳机": ["AirPods Pro {}", "索尼 WH-{}XM4", "华为 FreeBuds {}", "小米耳机 {}", "Bose QC{}"],
    "相机": ["佳能 EOS {}D", "尼康 Z{}", "索尼 A{}", "富士 X-T{}", "松下 GH{}"],
    "电视": ["小米电视 {}寸", "海信 TV{}", "TCL {}寸", "创维 {}K电视", "索尼 BRAVIA {}"],
    "冰箱": ["海尔冰箱 {}L", "美的冰箱 {}", "西门子 {}L", "容声冰箱 {}", "松下冰箱 {}"],
    "洗衣机": ["小天鹅洗衣机 {}kg", "美的洗衣机 {}", "海尔 {}kg", "西门子洗烘一体 {}", "松下洗衣机 {}"],
    "空调": ["格力空调 {}匹", "美的空调 {}", "海尔 {}匹", "TCL空调 {}", "奥克斯 {}匹"],
    "微波炉": ["美的微波炉 {}L", "格兰仕 {}L", "松下微波炉 {}", "海尔微波炉 {}", "西门子 {}L"],
    "书籍": ["Python编程 {}版", "Java核心技术 {}", "算法导论 {}版", "设计模式 {}", "数据结构 {}"],
    "服装": ["优衣库T恤 {}", "ZARA衬衫 {}", "H&M外套 {}", "Gap牛仔裤 {}", "Nike运动服 {}"],
    "鞋子": ["Nike Air Max {}", "Adidas Ultra {}", "New Balance {}", "Converse {}", "Vans {}"],
    "包包": ["Coach托特包 {}", "MK手提包 {}", "稻草人背包 {}", "小米双肩包 {}", "华为电脑包 {}"],
    "手表": ["卡西欧 G-Shock {}", "天梭手表 {}", "浪琴 {}系列", "华为 Watch {}", "Apple Watch {}"],
    "食品": ["三只松鼠零食 {}", "良品铺子 {}", "百草味 {}", "来伊份 {}", "洽洽 {}"],
    "饮料": ["农夫山泉 {}ml", "可口可乐 {}ml", "百事可乐 {}", "红牛 {}", "脉动 {}"],
    "化妆品": ["兰蔻面霜 {}", "雅诗兰黛 {}ml", "SK-II神仙水 {}", "资生堂 {}", "欧莱雅 {}"],
    "玩具": ["乐高 {}系列", "芭比娃娃 {}", "变形金刚 {}", "迪士尼 {}系列", "高达模型 {}"],
    "运动器材": ["迪卡侬瑜伽垫 {}", "李宁羽毛球拍 {}", "红双喜乒乓球拍 {}", "Keep健身器材 {}", "小米运动手环 {}"]
}

# 品牌
BRANDS = ["华为", "小米", "苹果", "三星", "OPPO", "vivo", "联想", "戴尔", "索尼", "尼康", "佳能", "美的", "海尔", "格力", "TCL"]

# 商品描述模板
DESCRIPTIONS = [
    "高性能处理器，流畅体验",
    "优质材料，经久耐用",
    "时尚设计，引领潮流",
    "智能科技，便捷生活",
    "超大容量，满足需求",
    "高清显示，视觉盛宴",
    "静音设计，舒适享受",
    "节能环保，绿色生活",
    "多功能一体，性价比高",
    "品牌保证，质量可靠"
]

# 动态属性模板
ATTRIBUTES_TEMPLATES = {
    "手机": {"屏幕尺寸": "{}寸", "电池容量": "{}mAh", "摄像头": "{}MP", "存储": "{}GB", "颜色": ["黑色", "白色", "蓝色", "金色"]},
    "电脑": {"CPU": "Intel i{}", "内存": "{}GB", "硬盘": "{}TB SSD", "显卡": "RTX {}", "屏幕": "{}寸"},
    "平板": {"屏幕": "{}寸", "存储": "{}GB", "电池": "{}mAh", "重量": "{}g", "系统": ["iOS", "Android", "HarmonyOS"]},
    "耳机": {"类型": ["入耳式", "头戴式", "半入耳式"], "降噪": ["主动降噪", "被动降噪"], "续航": "{}小时", "防水": ["IPX4", "IPX5", "IPX7"]},
    "相机": {"像素": "{}MP", "传感器": ["全画幅", "APS-C", "M4/3"], "对焦": ["相位对焦", "反差对焦"], "连拍": "{}张/秒"},
    "电视": {"分辨率": ["4K", "8K", "1080P"], "刷新率": ["60Hz", "120Hz", "144Hz"], "尺寸": "{}寸", "HDR": ["HDR10", "HDR10+", "Dolby Vision"]},
    "冰箱": {"容量": "{}L", "能效": ["一级", "二级", "三级"], "门数": ["单门", "双门", "三门", "对开门"], "制冷": ["直冷", "风冷"]},
    "洗衣机": {"容量": "{}kg", "类型": ["波轮", "滚筒", "洗烘一体"], "转速": ["1000转", "1200转", "1400转"], "能效": ["一级", "二级"]},
    "空调": {"匹数": ["1匹", "1.5匹", "2匹", "3匹"], "类型": ["挂机", "柜机", "中央空调"], "能效": ["一级", "二级", "三级"], "变频": ["定频", "变频"]},
    "微波炉": {"容量": "{}L", "功率": "{}W", "加热": ["微波", "光波", "蒸汽"], "控制": ["机械", "电脑"]},
    "书籍": {"页数": "{}页", "出版社": ["人民邮电", "机械工业", "电子工业", "清华大学"], "语言": ["中文", "英文"], "版次": ["第1版", "第2版", "第3版"]},
    "服装": {"尺码": ["S", "M", "L", "XL", "XXL"], "材质": ["纯棉", "涤纶", "混纺"], "季节": ["春", "夏", "秋", "冬"], "风格": ["休闲", "商务", "运动"]},
    "鞋子": {"尺码": ["38", "39", "40", "41", "42", "43", "44"], "材质": ["真皮", "网面", "帆布"], "功能": ["透气", "防水", "减震"]},
    "包包": {"容量": "{}L", "材质": ["真皮", "PU", "帆布"], "颜色": ["黑色", "棕色", "蓝色", "红色"]},
    "手表": {"表盘": ["圆形", "方形"], "防水": ["30米", "50米", "100米"], "表带": ["钢带", "皮带", "硅胶"]},
    "食品": {"重量": "{}g", "口味": ["原味", "辣味", "甜味", "咸味"], "保质期": "{}天"},
    "饮料": {"容量": "{}ml", "口味": ["原味", "柠檬味", "草莓味"], "糖分": ["无糖", "低糖", "正常"]},
    "化妆品": {"容量": "{}ml", "功效": ["保湿", "美白", "抗皱", "控油"], "肤质": ["干性", "油性", "混合性", "敏感性"]},
    "玩具": {"材质": ["塑料", "金属", "木质"], "年龄": ["3-6岁", "6-12岁", "12岁以上"], "电池": ["无需电池", "AA电池", "充电式"]},
    "运动器材": {"材质": ["TPE", "PVC", "橡胶"], "承重": "{}kg", "尺寸": ["标准", "加大", "迷你"]}
}

def generate_product(product_id):
    """生成单个商品数据"""
    category = random.choice(CATEGORIES)
    name_template = random.choice(PRODUCT_NAMES[category])
    model_num = random.randint(1, 999)
    name = name_template.format(model_num)
    
    # 生成价格（根据类别调整范围）
    price_ranges = {
        "手机": (1999, 9999), "电脑": (3999, 19999), "平板": (1999, 7999),
        "耳机": (99, 2999), "相机": (2999, 29999), "电视": (1999, 9999),
        "冰箱": (999, 7999), "洗衣机": (999, 5999), "空调": (1999, 8999),
        "微波炉": (299, 1999), "书籍": (29, 199), "服装": (99, 999),
        "鞋子": (199, 1299), "包包": (199, 2999), "手表": (299, 9999),
        "食品": (9, 99), "饮料": (3, 29), "化妆品": (99, 1999),
        "玩具": (49, 999), "运动器材": (99, 1999)
    }
    min_price, max_price = price_ranges[category]
    price = Decimal(str(round(random.uniform(min_price, max_price), 2)))
    
    stock = random.randint(0, 500)
    merchant_id = random.randint(1, 20)
    # 生成更长的描述（增加数据量）
    base_desc = random.choice(DESCRIPTIONS)
    extra_desc = f"这款{category}采用优质材料制作，具有{random.choice(['轻便', '耐用', '时尚', '高性能', '经典'])}的特点。"
    extra_desc += f"适合{random.choice(['家庭', '办公', '户外', '旅行', '日常'])}使用。"
    extra_desc += f"品牌保证，质量可靠，售后无忧。"
    description = f"{name} - {base_desc} {extra_desc}"
    image_url = f"https://example.com/images/{category}/{product_id}.jpg"
    
    # 生成更多动态属性（增加数据量）
    attr_template = ATTRIBUTES_TEMPLATES[category]
    attributes = {}
    for key, value_template in attr_template.items():
        if isinstance(value_template, list):
            attributes[key] = random.choice(value_template)
        elif "{}" in str(value_template):
            num = random.randint(1, 100)
            attributes[key] = value_template.format(num)
        else:
            attributes[key] = value_template
    
    # 添加额外的通用属性
    attributes["品牌"] = random.choice(BRANDS)
    attributes["产地"] = random.choice(["中国大陆", "日本", "韩国", "美国", "德国"])
    attributes["保修期"] = random.choice(["6个月", "12个月", "24个月", "36个月"])
    attributes["包装清单"] = f"{name} x1, 说明书 x1, 保修卡 x1"
    
    return {
        "id": product_id,
        "name": name,
        "price": float(price),
        "stock": stock,
        "category": category,
        "merchantId": merchant_id,
        "description": description,
        "imageUrl": image_url,
        "attributes": attributes
    }

def main():
    """主函数：生成大量商品数据（约500MB）"""
    products = []
    num_products = 500000  # 生成50万个商品，约500MB
    
    print(f"正在生成 {num_products} 个商品数据（目标大小约500MB）...")
    print("这可能需要几分钟时间，请耐心等待...")
    
    for i in range(1, num_products + 1):
        product = generate_product(i)
        products.append(product)
        
        if i % 10000 == 0:
            print(f"已生成 {i} 个商品...")
    
    # 保存为JSON文件
    output_file = "/root/test_products_large.json"
    print(f"\n正在写入文件...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
    
    # 计算文件大小
    import os
    file_size = os.path.getsize(output_file)
    file_size_mb = file_size / (1024 * 1024)
    
    print(f"\n✅ 生成完成！")
    print(f"📁 文件路径: {output_file}")
    print(f"📊 商品数量: {num_products:,}")
    print(f"💾 文件大小: {file_size_mb:.2f} MB")

if __name__ == "__main__":
    main()
