#!/bin/bash
MONGO_POD=$(kubectl get pods -l app=mongodb -o jsonpath='{.items[0].metadata.name}')
echo "MongoDB Pod: $MONGO_POD"

kubectl cp /tmp/img-update/images-final.json $MONGO_POD:/tmp/img-update/images-final.json
kubectl cp /tmp/img-update/update-final.js $MONGO_POD:/tmp/img-update/update-final.js

echo "Running update..."
kubectl exec $MONGO_POD -- mongosh --quiet /tmp/img-update/update-final.js
