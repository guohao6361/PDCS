#!/bin/bash
MONGO_POD=$(kubectl get pods -l app=mongodb -o jsonpath='{.items[0].metadata.name}')
echo "MongoDB Pod: $MONGO_POD"

kubectl cp /tmp/img-update/images-compressed.json $MONGO_POD:/tmp/img-update/images-compressed.json
kubectl cp /tmp/img-update/update-compressed.js $MONGO_POD:/tmp/img-update/update-compressed.js

echo "Running update..."
kubectl exec $MONGO_POD -- mongosh --quiet /tmp/img-update/update-compressed.js
