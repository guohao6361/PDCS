package com.ecommerce.product.controller;

import com.ecommerce.common.ApiResponse;
import com.ecommerce.common.InternalApi;
import com.ecommerce.common.PageResponse;
import com.ecommerce.product.entity.Product;
import com.ecommerce.product.entity.Review;
import com.ecommerce.product.service.impl.ProductServiceImpl;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;
import java.util.Map;

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

    // 商品搜索（按名称或分类）
    @GetMapping("/products/search")
    public ResponseEntity<ApiResponse<PageResponse<Product>>> searchProducts(
            @RequestParam String keyword,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size) {
        PageResponse<Product> result = productService.searchProducts(keyword, page, size);
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
    @InternalApi
    public ResponseEntity<ApiResponse<Void>> deductStock(
            @PathVariable Integer id,
            @RequestParam Integer quantity) {
        productService.deductStock(id, quantity);
        return ResponseEntity.ok(ApiResponse.success("库存扣减成功"));
    }

    // 恢复库存（内部服务调用）
    @PutMapping("/products/{id}/restore-stock")
    @InternalApi
    public ResponseEntity<ApiResponse<Void>> restoreStock(
            @PathVariable Integer id,
            @RequestParam Integer quantity) {
        productService.restoreStock(id, quantity);
        return ResponseEntity.ok(ApiResponse.success("库存恢复成功"));
    }

    // 上传商品图片
    @PostMapping("/products/upload")
    public ResponseEntity<ApiResponse<Map<String, String>>> uploadProductImage(
            @RequestParam("file") MultipartFile file,
            HttpServletRequest httpRequest) {
        String role = (String) httpRequest.getAttribute("userRole");
        if (!"MERCHANT".equals(role) && !"ADMIN".equals(role)) {
            return ResponseEntity.ok(ApiResponse.error(403, "需要商家或管理员权限"));
        }
        try {
            String imageUrl = productService.uploadProductImage(file.getBytes(), file.getOriginalFilename(), file.getContentType());
            return ResponseEntity.ok(ApiResponse.success(Map.of("imageUrl", imageUrl)));
        } catch (Exception e) {
            return ResponseEntity.internalServerError().build();
        }
    }

    // 商家发布商品
    @PostMapping("/products")
    public ResponseEntity<ApiResponse<Product>> createProduct(
            @RequestBody Product product,
            HttpServletRequest httpRequest) {
        String role = (String) httpRequest.getAttribute("userRole");
        if (!"MERCHANT".equals(role) && !"ADMIN".equals(role)) {
            return ResponseEntity.ok(ApiResponse.error(403, "需要商家或管理员权限"));
        }
        Product saved = productService.createProduct(product);
        return ResponseEntity.ok(ApiResponse.success(saved));
    }

    // 修改商品
    @PutMapping("/products/{id}")
    public ResponseEntity<ApiResponse<Product>> updateProduct(
            @PathVariable Integer id,
            @RequestBody Product product,
            HttpServletRequest httpRequest) {
        String role = (String) httpRequest.getAttribute("userRole");
        Integer userId = (Integer) httpRequest.getAttribute("userId");
        if (!"MERCHANT".equals(role) && !"ADMIN".equals(role)) {
            return ResponseEntity.ok(ApiResponse.error(403, "需要商家或管理员权限"));
        }
        // 商家只能修改自己的商品，管理员可以修改所有商品
        if ("MERCHANT".equals(role)) {
            Product existing = productService.getProduct(id);
            if (existing.getMerchantId() == null || !existing.getMerchantId().equals(userId)) {
                return ResponseEntity.ok(ApiResponse.error(403, "无权修改此商品，只能管理自己发布的商品"));
            }
        }
        Product updated = productService.updateProduct(id, product);
        return ResponseEntity.ok(ApiResponse.success(updated));
    }

    // 删除商品
    @DeleteMapping("/products/{id}")
    public ResponseEntity<ApiResponse<Void>> deleteProduct(
            @PathVariable Integer id,
            HttpServletRequest httpRequest) {
        String role = (String) httpRequest.getAttribute("userRole");
        Integer userId = (Integer) httpRequest.getAttribute("userId");
        if (!"MERCHANT".equals(role) && !"ADMIN".equals(role)) {
            return ResponseEntity.ok(ApiResponse.error(403, "需要商家或管理员权限"));
        }
        // 商家只能删除自己的商品，管理员可以删除所有商品
        if ("MERCHANT".equals(role)) {
            Product existing = productService.getProduct(id);
            if (existing.getMerchantId() == null || !existing.getMerchantId().equals(userId)) {
                return ResponseEntity.ok(ApiResponse.error(403, "无权删除此商品，只能管理自己发布的商品"));
            }
        }
        productService.deleteProduct(id);
        return ResponseEntity.ok(ApiResponse.success("商品删除成功"));
    }

    // 商家商品列表
    @GetMapping("/products/merchant/{merchantId}")
    public ResponseEntity<ApiResponse<List<Product>>> getProductsByMerchant(@PathVariable Integer merchantId) {
        List<Product> products = productService.getProductsByMerchant(merchantId);
        return ResponseEntity.ok(ApiResponse.success(products));
    }

    // 删除商家所有商品（内部服务调用）
    @DeleteMapping("/products/merchant/{merchantId}")
    @InternalApi
    public ResponseEntity<ApiResponse<Void>> deleteProductsByMerchant(@PathVariable Integer merchantId) {
        productService.deleteProductsByMerchant(merchantId);
        return ResponseEntity.ok(ApiResponse.success("商家商品已删除"));
    }
}