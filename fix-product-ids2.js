db = db.getSiblingDB("ecommerce");

print("开始修复 _id 类型...");
print("原始数量: " + db.products.countDocuments());

// 先检查是否有 id 字段
var sample = db.products.findOne();
print("示例文档字段: " + Object.keys(sample));

// 用聚合管道：用 setWindowFields 生成序号作为 _id
db.products.aggregate([
    {
        $setWindowFields: {
            sortBy: { _id: 1 },
            output: {
                rowNum: { $documentNumber: {} }
            }
        }
    },
    {
        $set: {
            _id: { $toInt: "$rowNum" },
            id: { $toInt: "$rowNum" }
        }
    },
    {
        $project: {
            rowNum: 0
        }
    },
    {
        $out: "products_new"
    }
]);

print("新集合 products_new 数量: " + db.products_new.countDocuments());

// 删除旧集合，重命名
db.products.drop();
db.products_new.renameCollection("products");

print("修复完成！");
print("最终数量: " + db.products.countDocuments());
var doc = db.products.findOne();
print("_id 类型: " + typeof doc._id);
print("id 类型: " + typeof doc.id);
printjson(doc);

// 验证大小
var stats = db.products.stats();
print("数据大小: " + (stats.totalSize / 1024 / 1024).toFixed(2) + " MB");
