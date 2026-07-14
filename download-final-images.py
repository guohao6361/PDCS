#!/usr/bin/env python3
"""重新下载并适当压缩所有商品图片"""
import base64
import json
import urllib.request
import ssl
import os
from PIL import Image
import io

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 所有产品的图片 URL
PRODUCT_IMAGES = {
    # Apple 产品 - Apple CDN
    1: "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-16-pro-finish-select-202409-6-3inch-naturaltitanium?wid=960&hei=960&fmt=jpeg&qlt=90&.v=1726099978945",
    2: "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-16-pro-finish-select-202409-6-3inch-deserttitanium?wid=960&hei=960&fmt=jpeg&qlt=90&.v=1726099978945",
    3: "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-16-finish-select-202409-6-1inch-ultramarine?wid=960&hei=960&fmt=jpeg&qlt=90&.v=1726099963904",
    7: "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/macbook-air-og-202503?wid=960&hei=960&fmt=jpeg&qlt=90&.v=1741309128737",
    9: "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/ipad-pro-model-select-gallery-1-202405?wid=960&hei=960&fmt=jpeg&qlt=90&.v=1713821703584",
    10: "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/airpods-pro-2-hero-select-202409?wid=976&hei=1000&fmt=jpeg&qlt=90&.v=1724040710360",
    12: "https://img14.360buyimg.com/n1/jfs/t1/454725/3/380/106714/6a23f2adFa5a713a3/00833203202f0528.jpg!q70.dpg",
    13: "https://img14.360buyimg.com/n1/jfs/t1/465410/11/12318/60676/6a43602eFf37578fb/00833203200b77ad.jpg!q70.dpg",
    30: "https://img14.360buyimg.com/n1/jfs/t1/461177/36/18777/59661/6a44893aF2a61652d/008332032003f1a5.png!q70.dpg",
    35: "https://img14.360buyimg.com/n1/jfs/t1/374785/25/18770/369654/6944f1ecF3c069e58/02584ff4fff7ec74.jpg!q70.dpg",
    40: "https://img14.360buyimg.com/n1/jfs/t1/424547/5/15195/51344/69f1a6efF4a718cb0/008332032083b459.png!q70.dpg",
    # 京东产品
    4: "https://img14.360buyimg.com/n1/jfs/t1/439831/21/10116/375137/6a1531c5F4008b639/0083320320a3a41e.png!q70.dpg",
    5: "https://img14.360buyimg.com/n1/jfs/t1/457364/32/15134/82964/6a3a5dd1F639d5834/0083320320ac53d0.jpg!q70.dpg",
    6: "https://img14.360buyimg.com/n1/jfs/t1/476217/2/3990/137991/6a4ccd18Fc8f95839/0083320320099457.jpg!q70.dpg",
    8: "https://img14.360buyimg.com/n1/jfs/t1/461417/25/12190/33205/6a3f9629Fe3f28221/0083320320f5a5eb.png!q70.dpg",
    11: "https://img14.360buyimg.com/n1/jfs/t1/146808/16/27291/56467/627897dbE57495d32/c1e27109b41e1d8c.jpg!q70.dpg",
    14: "https://img14.360buyimg.com/n1/jfs/t1/471522/21/9556/235411/6a4e1608Faf5f3806/0083320320474307.png!q70.dpg",
    15: "https://img14.360buyimg.com/n1/jfs/t1/433362/37/10133/356030/6a056811Fabe07dd5/025832032003221b.jpg!q70.dpg",
    16: "https://img14.360buyimg.com/n1/jfs/t1/477024/11/7596/201804/6a54b287F46dc837b/0083320320f9f86e.jpg!q70.dpg",
    17: "https://img14.360buyimg.com/n1/jfs/t1/444357/31/9218/125848/6a1d3c10Fab873644/008332032096ec2c.jpg!q70.dpg",
    18: "https://img14.360buyimg.com/n1/jfs/t1/457517/33/9699/113857/6a38a313Ff59e970a/00833203202a455e.jpg!q70.dpg",
    19: "https://img14.360buyimg.com/n1/jfs/t1/468213/5/5585/174237/6a42252fF7d16ddd5/0083320320d9159f.jpg!q70.dpg",
    20: "https://img14.360buyimg.com/n1/jfs/t1/412041/39/7703/93718/69cdd8ebF21d9596d/008332032070c415.png!q70.dpg",
    21: "https://img14.360buyimg.com/n1/jfs/t1/470662/25/11694/140583/6a4b6ec9F096938d6/0083320320fb7edd.jpg!q70.dpg",
    22: "https://img14.360buyimg.com/n1/jfs/t1/470363/26/5161/146622/6a4638a0Fbd2084eb/0083320320cf4b1e.jpg!q70.dpg",
    23: "https://img14.360buyimg.com/n1/jfs/t1/472645/10/729/163583/6a446f3fFb71ebaf1/0083320320992abd.jpg!q70.dpg",
    24: "https://img14.360buyimg.com/n1/jfs/t1/421617/16/12340/26984/69e6ebf9F61223006/0083320320dbb2ea.jpg!q70.dpg",
    25: "https://img14.360buyimg.com/n1/jfs/t1/424636/27/15042/2167529/69f1c666Ff6b308b6/008332032083b459.png!q70.dpg",
    26: "https://img14.360buyimg.com/n1/jfs/t1/327531/40/17337/30624/68bd4e8aF3330d1c3/90cf3b234483b15e.png!q70.dpg",
    27: "https://img14.360buyimg.com/n1/jfs/t1/482456/37/1182/127466/6a54a706F129b9eee/00835a05a0b702c4.jpg!q70.dpg",
    28: "https://img14.360buyimg.com/n1/jfs/t1/465963/4/16690/330191/6a487d41F11081215/0083320320e6e552.png!q70.dpg",
    29: "https://img14.360buyimg.com/n1/jfs/t1/447910/5/2631/105878/6a1ec09eFa0910806/0083320320b853a2.jpg!q70.dpg",
    31: "https://img14.360buyimg.com/n1/jfs/t1/464166/21/15466/145740/6a43c689F4419dc91/0083320320df2791.jpg!q70.dpg",
    32: "https://img14.360buyimg.com/n1/jfs/t1/472057/22/13232/151487/6a4f5077F668bf221/0083320320197ffb.jpg!q70.dpg",
    33: "https://img14.360buyimg.com/n1/jfs/t1/474343/25/360/109225/6a45c125F9bacdbc6/008332032003dd7a.jpg!q70.dpg",
    34: "https://img14.360buyimg.com/n1/jfs/t1/407765/37/9398/89850/69c1f470F3f55d3e0/00833203207b6bf1.jpg!q70.dpg",
    36: "https://img14.360buyimg.com/n1/jfs/t1/470377/29/16341/171222/6a50baa7F3e4548a3/0083320320c0233f.png!q70.dpg",
    37: "https://img14.360buyimg.com/n1/jfs/t1/421220/33/5078/113441/69e32058Fb4228218/00833203204d04b9.jpg!q70.dpg",
    38: "https://img14.360buyimg.com/n1/jfs/t1/470895/24/16807/116866/6a50e446F8c7990e1/00833203209f7941.jpg!q70.dpg",
    39: "https://img14.360buyimg.com/n1/jfs/t1/479513/34/3411/143211/6a520157Fc0d91cd5/00833203209cce8f.jpg!q70.dpg",
}

def download_and_compress(url, max_size=200, quality=80, timeout=15):
    """下载图片并压缩到合适大小"""
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://www.jd.com/"
        })
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            data = resp.read()
            if len(data) < 1000:
                return None
            
            img = Image.open(io.BytesIO(data))
            # 转换 RGBA 到 RGB
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if 'A' in img.mode else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 缩放到合适大小
            img.thumbnail((max_size, max_size), Image.LANCZOS)
            
            # 保存为 JPEG
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=quality)
            return base64.b64encode(buffer.getvalue()).decode('ascii')
    except Exception as e:
        print(f"  失败: {e}")
        return None

def main():
    print("=== 下载并压缩所有商品图片 ===\n")
    
    images = {}
    for pid in sorted(PRODUCT_IMAGES.keys()):
        url = PRODUCT_IMAGES[pid]
        print(f"[{pid:2d}] 下载压缩中...", end=" ")
        b64 = download_and_compress(url, max_size=200, quality=80)
        if b64:
            images[pid] = "data:image/jpeg;base64," + b64
            print(f"OK ({len(b64)//1024}KB)")
        else:
            print("失败")
    
    print(f"\n成功: {len(images)}/{len(PRODUCT_IMAGES)}\n")
    
    # 保存
    images_json = json.dumps({str(k): v for k, v in images.items()}, ensure_ascii=False)
    with open("/tmp/img-update/images-final.json", "w") as f:
        f.write(images_json)
    print(f"总大小: {len(images_json)//1024}KB")
    
    # 生成更新脚本
    script = '''
db = db.getSiblingDB("ecommerce");
var fs = require("fs");
var images = JSON.parse(fs.readFileSync("/tmp/img-update/images-final.json", "utf8"));
print("加载了 " + Object.keys(images).length + " 个图片");

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
    
    with open("/tmp/img-update/update-final.js", "w") as f:
        f.write(script)
    
    print("脚本: /tmp/img-update/update-final.js")

if __name__ == "__main__":
    main()
