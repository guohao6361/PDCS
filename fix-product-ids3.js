db = db.getSiblingDB("ecommerce");

print("开始修复 _id 类型...");
print("原始数量: " + db.products.countDocuments());

// 检查示例
var sample = db.products.findOne();
print("示例 _id: " + sample._id + " (类型: " + typeof sample._id + ")");
print("示例 id: " + sample.id + " (类型: " + typeof sample.id + ")");

// 简单方案：直接用 id 字段作为 _id
// 先创建新集合，用 id 字段作为 _id
db.products.aggregate([
    {
        $project: {
            _id: { $toInt: "$id" },
            name: 1,
            price: 1,
            stock: 1,
            category: 1,
            merchantId: 1,
            description: 1,
            imageUrl: 1,
            attributes: 1,
            imageData: 1,
            img_3: 1
        }
    },
    {
        $out: "products_fixed"
    }
]);

print("新集合数量: " + db.products_fixed.countDocuments());

// 替换旧集合
db.products.drop();
db.products_fixed.renameCollection("products");

print("修复完成！");
print("最终数量: " + db.products.countDocuments());

var doc = db.products.findOne();
print("_id: " + doc._id + " (类型: " + typeof doc._id + ")");
print("name: " + doc.name);

var stats = db.products.stats();
print("数据大小: " + (stats.totalSize / 1024 / 1024).toFixed(2) + " MB");
