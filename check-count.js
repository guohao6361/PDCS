db = db.getSiblingDB("ecommerce");
print("总数: " + db.products.countDocuments());
print("ObjectId数量: " + db.products.countDocuments({_id: {$type: "objectId"}}));
print("Integer数量: " + db.products.countDocuments({_id: {$type: "int"}}));
