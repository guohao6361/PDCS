package com.ecommerce.product.controller;

import com.ecommerce.product.entity.Product;
import com.ecommerce.product.entity.Review;
import com.ecommerce.product.service.impl.ProductServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@CrossOrigin
@RestController
public class ProductController {

    @Autowired
    private ProductServiceImpl productService;

    // 1. 获取商品详情 [1.1.2]
    @GetMapping("/products/{id}")
    public ResponseEntity<Product> getProduct(@PathVariable Integer id) {
        return ResponseEntity.ok(productService.getProduct(id));
    }

    // 2. 发表评价 [1.1.2]
    @PostMapping("/reviews")
    public ResponseEntity<Review> addReview(@RequestBody Review review) {
        return ResponseEntity.ok(productService.addReview(review));
    }

    // 3. 获取某商品下的所有评价
    @GetMapping("/reviews/{productId}")
    public ResponseEntity<List<Review>> getReviews(@PathVariable Integer productId) {
        return ResponseEntity.ok(productService.getReviews(productId));
    }
}