#!/bin/bash
POD=$(kubectl get pods -l app=product-service -o jsonpath='{.items[0].metadata.name}')
echo "Pod: $POD"
kubectl cp /root/ecommerce-project/product-service/target/product-service-0.0.1-SNAPSHOT.jar $POD:/app/app.jar
echo "JAR copied, restarting..."
kubectl exec $POD -- kill 1
echo "Done"
