#!/bin/bash
MONGO_POD=$(kubectl get pods -l app=mongodb -o jsonpath="{.items[0].metadata.name}")
echo "MongoDB Pod: $MONGO_POD"

# Check MongoDB connection info
kubectl exec $MONGO_POD -- env | grep -i mongo

# Check if pymongo is available inside the pod
kubectl exec $MONGO_POD -- python3 --version 2>/dev/null || echo "No python3 in mongo pod"

# Check mongosh capabilities
kubectl exec $MONGO_POD -- mongosh --version 2>/dev/null

# Check pip availability in the pod
kubectl exec $MONGO_POD -- pip3 --version 2>/dev/null || echo "No pip3 in mongo pod"

# Check disk space
kubectl exec $MONGO_POD -- df -h /data/db 2>/dev/null || kubectl exec $MONGO_POD -- df -h / 2>/dev/null
