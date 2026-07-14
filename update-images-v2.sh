#!/bin/bash
MONGO_POD=$(kubectl get pods -l app=mongodb -o jsonpath='{.items[0].metadata.name}')
echo "MongoDB Pod: $MONGO_POD"

# Copy files to pod
kubectl exec $MONGO_POD -- mkdir -p /tmp/img-update
kubectl cp /tmp/img-update/images-v2.json $MONGO_POD:/tmp/img-update/images-v2.json
kubectl cp /tmp/img-update/update-v2.js $MONGO_POD:/tmp/img-update/update-v2.js

echo "Running update..."
kubectl exec $MONGO_POD -- mongosh --quiet /tmp/img-update/update-v2.js
