db = db.getSiblingDB("ecommerce");
// 清理残留集合
db.products_new.drop();
db.products_fixed.drop();
print("清理完成");
print("products 数量: " + db.products.countDocuments());
