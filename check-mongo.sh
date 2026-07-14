#!/bin/bash
MONGO_POD=$(kubectl get pods -l app=mongodb -o jsonpath="{.items[0].metadata.name}")
echo "MongoDB pod: $MONGO_POD"

echo ""
echo "1. Count products in ecommerce db:"
kubectl exec -it $MONGO_POD -- mongosh --quiet --eval "db = db.getSiblingDB('ecommerce'); db.products.countDocuments()"

echo ""
echo "2. Sample 5 products:"
kubectl exec -it $MONGO_POD -- mongosh --quiet --eval "db = db.getSiblingDB('ecommerce'); db.products.find({}, {id: 1, merchantId: 1, name: 1}).limit(5).toArray()"

echo ""
echo "3. Products by merchantId:"
kubectl exec -it $MONGO_POD -- mongosh --quiet --eval "db = db.getSiblingDB('ecommerce'); db.products.aggregate([{\$group: {_id: '\$merchantId', count: {\$sum: 1}}}, {\$limit: 10}]).toArray()"
