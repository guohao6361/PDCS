#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将测试商品数据导入到 MongoDB 数据库
"""

import json
import sys
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError

def import_products_to_mongodb(json_file_path, mongo_uri="mongodb://localhost:27017/ecommerce"):
    """
    将商品数据从 JSON 文件导入到 MongoDB
    
    Args:
        json_file_path: JSON 文件路径
        mongo_uri: MongoDB 连接 URI
    """
    print(f"📖 正在读取数据文件: {json_file_path}")
    
    # 读取 JSON 文件
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            products = json.load(f)
        print(f"✅ 成功读取 {len(products)} 个商品数据")
    except FileNotFoundError:
        print(f"❌ 错误: 文件不存在 - {json_file_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ 错误: JSON 解析失败 - {e}")
        sys.exit(1)
    
    # 连接 MongoDB
    print(f"\n🔌 正在连接 MongoDB: {mongo_uri}")
    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        # 测试连接
        client.admin.command('ping')
        print("✅ MongoDB 连接成功")
    except ConnectionFailure as e:
        print(f"❌ 错误: 无法连接到 MongoDB - {e}")
        print("\n💡 提示:")
        print("  1. 确保 MongoDB 服务正在运行")
        print("  2. 检查连接 URI 是否正确")
        print("  3. 如果在 K8s 中运行，需要使用正确的服务地址")
        sys.exit(1)
    
    # 选择数据库和集合
    db = client['ecommerce']
    collection = db['products']
    
    print(f"\n📊 数据库: ecommerce")
    print(f"📋 集合: products")
    
    # 检查现有数据
    existing_count = collection.count_documents({})
    print(f"\n⚠️  当前集合中已有 {existing_count} 条数据")
    
    if existing_count > 0:
        print("\n请选择操作:")
        print("  1. 清空现有数据并导入新数据")
        print("  2. 追加数据（跳过重复ID）")
        print("  3. 取消操作")
        
        choice = input("\n请输入选项 (1/2/3): ").strip()
        
        if choice == '1':
            print("\n🗑️  正在清空现有数据...")
            collection.delete_many({})
            print("✅ 已清空数据")
        elif choice == '2':
            print("\n➕ 将追加数据，跳过重复ID")
        elif choice == '3':
            print("\n❌ 操作已取消")
            client.close()
            sys.exit(0)
        else:
            print("\n❌ 无效的选项")
            client.close()
            sys.exit(1)
    
    # 导入数据
    print(f"\n🚀 开始导入数据...")
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for product in products:
        try:
            # 尝试插入数据
            collection.insert_one(product)
            success_count += 1
            
            # 显示进度
            if success_count % 500 == 0:
                print(f"  已导入 {success_count} 条数据...")
                
        except DuplicateKeyError:
            skip_count += 1
            if skip_count <= 5:  # 只显示前5个重复的
                print(f"  ⚠️  跳过重复ID: {product.get('id')}")
        except Exception as e:
            error_count += 1
            if error_count <= 5:  # 只显示前5个错误
                print(f"  ❌ 导入失败: {product.get('id')} - {e}")
    
    # 显示结果
    print(f"\n{'='*50}")
    print(f"✅ 导入完成！")
    print(f"{'='*50}")
    print(f"📊 总商品数: {len(products)}")
    print(f"✅ 成功导入: {success_count}")
    print(f"⚠️  跳过重复: {skip_count}")
    print(f"❌ 导入失败: {error_count}")
    print(f"📊 集合现有数据: {existing_count}")
    print(f"📊 集合最终数据: {collection.count_documents({})}")
    print(f"{'='*50}\n")
    
    # 关闭连接
    client.close()
    print("🔌 已关闭 MongoDB 连接")

def main():
    """主函数"""
    # 默认配置
    json_file = "/root/test_products.json"
    mongo_uri = "mongodb://localhost:27017/ecommerce"
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
    if len(sys.argv) > 2:
        mongo_uri = sys.argv[2]
    
    print("="*50)
    print("🛒 电商商品数据导入工具")
    print("="*50)
    
    # 执行导入
    import_products_to_mongodb(json_file, mongo_uri)
    
    print("\n✨ 完成！您可以在应用中查询这些商品了。")
    print("\n💡 测试命令:")
    print("  curl http://localhost:8080/products/1")
    print("  curl http://localhost:8080/products/2")

if __name__ == "__main__":
    main()
