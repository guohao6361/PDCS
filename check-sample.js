db = db.getSiblingDB("ecommerce");
printjson(db.products.findOne());
