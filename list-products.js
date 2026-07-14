db = db.getSiblingDB("ecommerce");
var products = db.products.find({}, {name:1}).limit(10).toArray();
products.forEach(function(p){ print(p.name); });
print("---");
print("Total: " + db.products.countDocuments());
