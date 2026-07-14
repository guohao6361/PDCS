db = db.getSiblingDB("ecommerce");

// 检查前40个基础产品的图片情况
var results = [];
for (var i = 1; i <= 40; i++) {
    var doc = db.products.findOne({_id: NumberInt(i)});
    if (doc) {
        var imgLen = doc.imageData ? doc.imageData.length : 0;
        var isReal = imgLen > 10000; // 真实图片通常 > 10KB
        results.push({
            id: i,
            name: doc.name,
            category: doc.category,
            imgSize: imgLen,
            isReal: isReal
        });
    }
}

print("=== 基础产品图片状态 ===\n");
results.forEach(function(r) {
    var status = r.isReal ? "真实图片" : "占位图";
    print("[" + r.id + "] " + r.category + " | " + r.name + " | " + status + " (" + r.imgSize + " bytes)");
});

var realCount = results.filter(function(r){ return r.isReal; }).length;
print("\n真实图片: " + realCount + "/40");
print("占位图: " + (40 - realCount) + "/40");
