#!/bin/bash
MONGO_POD=$(kubectl get pods -l app=mongodb -o jsonpath='{.items[0].metadata.name}')
echo "MongoDB Pod: $MONGO_POD"

# Create directory in pod
kubectl exec $MONGO_POD -- mkdir -p /tmp/img-update

# Copy files
kubectl cp /tmp/img-update/images.json $MONGO_POD:/tmp/img-update/images.json
kubectl cp /tmp/img-update/update.js $MONGO_POD:/tmp/img-update/update.js

echo "Files copied. Running update..."
kubectl exec $MONGO_POD -- mongosh --quiet /tmp/img-update/update.js
