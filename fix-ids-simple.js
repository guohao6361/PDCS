db = db.getSiblingDB("ecommerce");

// 先清理残留
db.products_new.drop();
db.products_fixed.drop();

var total = db.products.countDocuments();
print("总商品数: " + total);

// 检查是否有 id 字段
var sample = db.products.findOne();
print("示例字段: " + Object.keys(sample).join(", "));
print("示例 _id: " + sample._id + " (type: " + typeof sample._id + ")");
print("示例 id: " + sample.id + " (type: " + typeof sample.id + ")");

// 分批更新：将 _id 从 ObjectId 改为 integer (使用 id 字段的值)
var batchSize = 500;
var processed = 0;
var hasIdField = (sample.id !== undefined);

if (hasIdField) {
    print("\n使用已有 id 字段更新 _id...");
    
    // 获取所有有 id 字段的文档的 _id 和 id 映射
    var cursor = db.products.find({}, {_id: 1, id: 1}).limit(total);
    var mappings = [];
    cursor.forEach(function(doc) {
        if (doc.id !== undefined) {
            mappings.push({oldId: doc._id, newId: NumberInt(doc.id)});
        }
    });
    
    print("需要更新: " + mappings.length + " 条");
    
    // 分批处理
    for (var i = 0; i < mappings.length; i += batchSize) {
        var batch = mappings.slice(i, i + batchSize);
        var ops = [];
        
        for (var j = 0; j < batch.length; j++) {
            // 先删除旧文档，再用新 _id 插入
            ops.push({
                updateOne: {
                    filter: { _id: batch[j].oldId },
                    update: { $set: { _id: batch[j].newId } }
                }
            });
        }
        
        // MongoDB 不允许更新 _id，需要用 delete + insert
        // 改用另一种方式
        for (var j = 0; j < batch.length; j++) {
            var oldDoc = db.products.findOne({_id: batch[j].oldId});
            if (oldDoc) {
                var newDoc = Object.assign({}, oldDoc);
                newDoc._id = batch[j].newId;
                db.products.deleteOne({_id: batch[j].oldId});
                db.products.insertOne(newDoc);
            }
        }
        
        processed += batch.length;
        if (processed % 2000 === 0 || processed === mappings.length) {
            print("已处理: " + processed + "/" + mappings.length);
        }
    }
}

print("\n修复完成！");
print("最终数量: " + db.products.countDocuments());
var doc = db.products.findOne();
print("_id: " + doc._id + " (type: " + typeof doc._id + ")");
var stats = db.products.stats();
print("数据大小: " + (stats.totalSize / 1024 / 1024).toFixed(2) + " MB");
