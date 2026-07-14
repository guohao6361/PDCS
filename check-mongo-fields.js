db = db.getSiblingDB("ecommerce");
var doc = db.products.findOne();
print("字段列表: " + Object.keys(doc).join(", "));
print("has imageData: " + ("imageData" in doc));
print("has imageUrl: " + ("imageUrl" in doc));
