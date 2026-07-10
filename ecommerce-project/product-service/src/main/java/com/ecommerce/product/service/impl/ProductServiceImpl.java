package com.ecommerce.product.service.impl;

import com.ecommerce.product.entity.Product;
import com.ecommerce.product.entity.Review;
import com.ecommerce.product.repository.ProductRepository;
import com.ecommerce.product.repository.ReviewRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Service;
import java.math.BigDecimal;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class ProductServiceImpl implements CommandLineRunner {

    @Autowired
    private ProductRepository productRepository;

    @Autowired
    private ReviewRepository reviewRepository;

    // 获取单条商品详情
    public Product getProduct(Integer id) {
        return productRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Product not found"));
    }

    // 发表评价
    public Review addReview(Review review) {
        return reviewRepository.save(review);
    }

    // 查询某商品的所有评价
    public List<Review> getReviews(Integer productId) {
        return reviewRepository.findByProductId(productId);
    }

    // ==========================================================
    // 自动初始化 MongoDB 实验数据 [1.1.2]
    // ==========================================================
    @Override
    public void run(String... args) throws Exception {
        if (productRepository.count() == 0) {
            // 1. 初始化华为 Mate 60 (带手机特有动态属性) [1.1.2]
            Product p1 = new Product();
            p1.setId(1);
            p1.setName("华为 Mate 60");
            p1.setPrice(new BigDecimal("6999.00"));
            p1.setStock(50);
            p1.setCategory("Electronics");
            Map<String, Object> attr1 = new HashMap<>();
            attr1.put("color", "雅川青");
            attr1.put("storage", "512GB");
            attr1.put("network", "5G");
            p1.setAttributes(attr1);
            productRepository.save(p1);

            // 2. 初始化机械键盘 (带键盘特有动态属性) [1.1.2]
            Product p2 = new Product();
            p2.setId(2);
            p2.setName("机械键盘");
            p2.setPrice(new BigDecimal("499.00"));
            p2.setStock(100);
            p2.setCategory("Accessories");
            Map<String, Object> attr2 = new HashMap<>();
            attr2.put("switchType", "红轴");
            attr2.put("backlight", "RGB");
            p2.setAttributes(attr2);
            productRepository.save(p2);

            // 3. 初始化降噪耳机 (带耳机特有动态属性) [1.1.2]
            Product p3 = new Product();
            p3.setId(3);
            p3.setName("降噪耳机");
            p3.setPrice(new BigDecimal("1299.00"));
            p3.setStock(30);
            p3.setCategory("Accessories");
            Map<String, Object> attr3 = new HashMap<>();
            attr3.put("ancDepth", "40dB");
            attr3.put("batteryLife", "30h");
            p3.setAttributes(attr3);
            productRepository.save(p3);

            System.out.println("🎉 MongoDB 商品实验数据初始化成功！");
        }
    }
}