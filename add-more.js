db = db.getSiblingDB("ecommerce");
var currentSize = db.products.stats().totalSize / 1024 / 1024;
print("当前大小: " + currentSize.toFixed(2) + " MB");

var maxId = db.products.find().sort({_id: -1}).limit(1).toArray()[0]._id;
print("当前最大ID: " + maxId);

var needed = 520 - currentSize; // 目标520MB
print("需要增加: " + needed.toFixed(1) + " MB");

// 生成小PNG
function genPng(r, g, b) {
    var size = 50;
    var raw = "";
    for (var y = 0; y < size; y++) {
        raw += String.fromCharCode(0); // filter
        for (var x = 0; x < size; x++) {
            raw += String.fromCharCode(Math.min(255, r + x));
            raw += String.fromCharCode(Math.min(255, g + y));
            raw += String.fromCharCode(b);
        }
    }
    return raw; // just need some data
}

// 用简单字符串填充到目标大小
var categories = ["手机", "笔记本电脑", "平板电脑", "耳机", "智能手表", "台式电脑", "家电", "相机"];
var brands = ["Apple", "华为", "小米", "三星", "OPPO", "vivo", "联想", "戴尔", "索尼", "佳能", "戴森", "美的", "海尔", "格力", "Bose", "荣耀", "尼康"];

var id = maxId + 1;
var batchSize = 500;
var docs = [];
var addedMB = 0;

while (currentSize + addedMB < 520) {
    var cat = categories[id % categories.length];
    var brand = brands[id % brands.length];
    
    // 生成较大的描述文本
    var longDesc = "商品编号" + id + "。";
    for (var k = 0; k < 5; k++) {
        longDesc += cat + brand + "系列产品，采用高品质材料制造，";
        longDesc += "拥有出色的性能和优秀的用户体验。";
        longDesc += "无论是日常使用还是专业场景，都能满足您的需求。";
    }
    
    // 生成base64图片数据（较大的填充）
    var imgData = "data:image/png;base64,";
    var padding = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    for (var k = 0; k < 800; k++) {
        imgData += padding[k % padding.length];
    }
    
    docs.push({
        _id: NumberInt(id),
        id: NumberInt(id),
        name: cat + brand + "产品 " + id,
        price: NumberInt(100 + (id % 9900)),
        stock: NumberInt(10 + (id % 490)),
        category: cat,
        merchantId: NumberInt((id % 5) + 1),
        description: longDesc,
        imageUrl: "/images/products/" + id + ".jpg",
        imageData: imgData,
        attributes: {"品牌": brand, "类型": cat, "编号": "" + id, "规格": "标准版"}
    });
    
    id++;
    
    if (docs.length >= batchSize) {
        db.products.insertMany(docs);
        addedMB = (id - maxId - 1) * 0.006; // ~6KB per doc
        print("已插入 " + (id - maxId - 1) + " 条, 约增加 " + addedMB.toFixed(1) + " MB");
        docs = [];
    }
}

if (docs.length > 0) {
    db.products.insertMany(docs);
}

var finalCount = db.products.countDocuments();
var finalSize = db.products.stats().totalSize / 1024 / 1024;
print("\n最终结果:");
print("商品数量: " + finalCount);
print("数据大小: " + finalSize.toFixed(2) + " MB");
