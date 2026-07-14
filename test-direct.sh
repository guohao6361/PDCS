#!/bin/bash
PRODUCT_POD=$(kubectl get pods -l app=product-service -o jsonpath='{.items[0].metadata.name}')
echo "Product Pod: $PRODUCT_POD"
echo "Testing direct API..."
kubectl exec $PRODUCT_POD -- curl -s --max-time 10 'http://localhost:8082/products?page=1&size=1' | head -c 300
echo ""
echo "---"
echo "Testing via nginx..."
curl -s --max-time 10 'http://localhost:30080/products?page=1&size=1' | head -c 300
