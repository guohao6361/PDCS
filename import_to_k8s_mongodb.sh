#!/bin/bash
# 将商品数据导入到 K8s 中的 MongoDB

echo "=========================================="
echo "🛒 电商商品数据导入工具 (K8s MongoDB)"
echo "=========================================="

# 获取 MongoDB Pod 名称
MONGO_POD=$(kubectl get pods -l app=mongodb -o jsonpath='{.items[0].metadata.name}')
echo "📍 MongoDB Pod: $MONGO_POD"

# 检查 Pod 是否运行
if [ -z "$MONGO_POD" ]; then
    echo "❌ 错误: 未找到运行中的 MongoDB Pod"
    exit 1
fi

echo "✅ MongoDB Pod 运行中"

# 将 JSON 文件复制到 MongoDB Pod
echo ""
echo "📤 正在上传数据文件到 MongoDB Pod..."
echo "文件大小约 330MB，上传可能需要几分钟..."
kubectl cp /root/test_products_large.json $MONGO_POD:/tmp/test_products_large.json

if [ $? -ne 0 ]; then
    echo "❌ 错误: 文件上传失败"
    exit 1
fi

echo "✅ 文件上传成功"

# 在 MongoDB Pod 中执行导入
echo ""
echo "🚀 开始导入数据到 MongoDB..."
echo ""

kubectl exec -i $MONGO_POD -- mongosh --eval '
// 读取文件内容
const fs = require("fs");
const data = fs.readFileSync("/tmp/test_products_large.json", "utf8");
const products = JSON.parse(data);

// 选择数据库和集合
const db = connect("mongodb://localhost:27017/ecommerce");
const collection = db.getCollection("products");

// 检查现有数据
const existingCount = collection.countDocuments({});
print("\n⚠️  当前集合中已有 " + existingCount + " 条数据");

if (existingCount > 0) {
    print("\n🗑️  清空现有数据...");
    collection.deleteMany({});
    print("✅ 已清空数据\n");
}

// 导入数据
print("🚀 开始导入 " + products.length + " 个商品...\n");

let successCount = 0;
let errorCount = 0;

products.forEach(product => {
    try {
        // 将 id 字段设置为 _id，这样 Spring Data MongoDB 才能正确识别
        product._id = product.id;
        delete product.id;  // 删除原来的 id 字段
        
        collection.insertOne(product);
        successCount++;
        
        if (successCount % 1000 === 0) {
            print("  已导入 " + successCount + " 条数据...");
        }
    } catch (e) {
        errorCount++;
        if (errorCount <= 5) {
            print("  ❌ 导入失败 ID " + product._id + ": " + e.message);
        }
    }
});

// 显示结果
print("\n==========================================");
print("✅ 导入完成！");
print("==========================================");
print("📊 总商品数: " + products.length);
print("✅ 成功导入: " + successCount);
print("❌ 导入失败: " + errorCount);
print("📊 集合最终数据: " + collection.countDocuments({}));
print("==========================================\n");

// 清理临时文件
fs.unlinkSync("/tmp/test_products_large.json");
print("🧹 已清理临时文件\n");
'

if [ $? -eq 0 ]; then
    echo ""
    echo "✨ 导入成功！您可以在应用中查询这些商品了。"
    echo ""
    echo "💡 测试命令:"
    echo "  curl http://localhost:8080/products/1"
    echo "  curl http://localhost:8080/products/2"
    echo ""
else
    echo ""
    echo "❌ 导入失败，请检查错误信息"
    exit 1
fi
