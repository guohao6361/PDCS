db = db.getSiblingDB("ecommerce");

// 获取总数
var total = db.products.countDocuments();
print("总商品数: " + total);

// 分批处理，每批1000条
var batchSize = 1000;
var processed = 0;
var id_counter = 1;

// 遍历所有文档，将 ObjectId _id 替换为 Integer _id
var cursor = db.products.find({});
var bulkOps = [];

cursor.forEach(function(doc) {
    // 删除旧的 ObjectId _id，设置新的 integer id
    bulkOps.push({
        deleteOne: { filter: { _id: doc._id } }
    });
    
    // 创建新文档，_id 为整数
    var newDoc = Object.assign({}, doc);
    delete newDoc._id;
    newDoc._id = id_counter;
    newDoc.id = id_counter;
    
    bulkOps.push({
        insertOne: { document: newDoc }
    });
    
    id_counter++;
    processed++;
    
    // 每1000条执行一次批量操作
    if (bulkOps.length >= 2000) {
        db.products.bulkWrite(bulkOps, { ordered: false });
        print("已处理: " + processed + "/" + total);
        bulkOps = [];
    }
});

// 处理剩余的
if (bulkOps.length > 0) {
    db.products.bulkWrite(bulkOps, { ordered: false });
}

print("修复完成！共处理: " + processed + " 条");
print("验证: " + db.products.countDocuments() + " 条");
printjson(db.products.findOne());
