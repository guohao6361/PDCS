package com.ecommerce.product.repository;

import com.ecommerce.product.entity.Review;
import org.springframework.data.mongodb.repository.MongoRepository;
import java.util.List;

public interface ReviewRepository extends MongoRepository<Review, String> {
    List<Review> findByProductId(Integer productId); // 按商品 ID 查找所有评论
}