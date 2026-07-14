db = db.getSiblingDB("ecommerce");

// 删除所有戴尔 XPS 15 相关商品 (baseId=25, 即 25, 65, 105, 145, ...)
var ids = [];
for (var id = 25; id <= 84327; id += 40) {
    ids.push(NumberInt(id));
}

print("待删除商品ID数量: " + ids.length);

var result = db.products.deleteMany({ _id: { $in: ids } });
print("已删除: " + result.deletedCount + " 条");

// 验证
var remaining = db.products.countDocuments();
print("剩余商品总数: " + remaining);

// 确认戴尔 XPS 15 已被删除
var check = db.products.findOne({ _id: NumberInt(25) });
print("ID=25 是否存在: " + (check ? "是" : "否"));

