package com.ecommerce.product.controller;

import com.ecommerce.common.ApiResponse;
import com.ecommerce.common.PageResponse;
import com.ecommerce.product.entity.Product;
import com.ecommerce.product.entity.Review;
import com.ecommerce.product.service.impl.ProductServiceImpl;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
public class ProductController {

    @Autowired
    private ProductServiceImpl productService;

    // 商品列表（分页）
    @GetMapping("/products")
    public ResponseEntity<ApiResponse<PageResponse<Product>>> getProducts(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size) {
        PageResponse<Product> result = productService.getAllProducts(page, size);
        return ResponseEntity.ok(ApiResponse.success(result));
    }

    // 商品详情
    @GetMapping("/products/{id}")
    public ResponseEntity<ApiResponse<Product>> getProduct(@PathVariable Integer id) {
        Product product = productService.getProduct(id);
        return ResponseEntity.ok(ApiResponse.success(product));
    }

    // 发表评价
    @PostMapping("/reviews")
    public ResponseEntity<ApiResponse<Review>> addReview(@Valid @RequestBody Review review) {
        Review saved = productService.addReview(review);
        return ResponseEntity.ok(ApiResponse.success(saved));
    }

    // 获取某商品下的所有评价
    @GetMapping("/reviews/{productId}")
    public ResponseEntity<ApiResponse<List<Review>>> getReviews(@PathVariable Integer productId) {
        List<Review> reviews = productService.getReviews(productId);
        return ResponseEntity.ok(ApiResponse.success(reviews));
    }

    // 扣减库存（内部服务调用）
    @PutMapping("/products/{id}/deduct-stock")
    public ResponseEntity<ApiResponse<Void>> deductStock(
            @PathVariable Integer id,
            @RequestParam Integer quantity) {
        productService.deductStock(id, quantity);
        return ResponseEntity.ok(ApiResponse.success("库存扣减成功"));
    }
}