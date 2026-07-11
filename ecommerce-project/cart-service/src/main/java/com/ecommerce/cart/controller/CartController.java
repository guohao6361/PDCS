package com.ecommerce.cart.controller;

import com.ecommerce.cart.dto.CartItemRequest;
import com.ecommerce.cart.dto.CartResponse;
import com.ecommerce.cart.service.CartService;
import com.ecommerce.common.ApiResponse;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/cart")
public class CartController {

    @Autowired
    private CartService cartService;

    @PostMapping("/add")
    public ResponseEntity<ApiResponse<Void>> add(@Valid @RequestBody CartItemRequest request) {
        cartService.addToCart(request.getUserId(), request.getProductId(), request.getQuantity());
        return ResponseEntity.ok(ApiResponse.success("添加成功"));
    }

    @GetMapping("/{userId}")
    public ResponseEntity<ApiResponse<CartResponse>> get(@PathVariable Long userId) {
        CartResponse cart = cartService.getCart(userId);
        return ResponseEntity.ok(ApiResponse.success(cart));
    }

    @DeleteMapping("/{userId}/{productId}")
    public ResponseEntity<ApiResponse<Void>> delete(
            @PathVariable Long userId, @PathVariable Long productId) {
        cartService.removeFromCart(userId, productId);
        return ResponseEntity.ok(ApiResponse.success("移除成功"));
    }

    @DeleteMapping("/{userId}")
    public ResponseEntity<ApiResponse<Void>> clear(@PathVariable Long userId) {
        cartService.clearCart(userId);
        return ResponseEntity.ok(ApiResponse.success("清空成功"));
    }

    // 更新购物车商品数量
    @PutMapping("/{userId}/{productId}")
    public ResponseEntity<ApiResponse<Void>> updateQuantity(
            @PathVariable Long userId,
            @PathVariable Long productId,
            @RequestBody Map<String, Integer> body) {
        Integer quantity = body.get("quantity");
        cartService.updateQuantity(userId, productId, quantity);
        return ResponseEntity.ok(ApiResponse.success("数量更新成功"));
    }

    // 移除勾选商品
    @PostMapping("/{userId}/remove-selected")
    public ResponseEntity<ApiResponse<Void>> removeSelected(
            @PathVariable Long userId,
            @RequestBody Map<String, List<Long>> body) {
        List<Long> productIds = body.get("productIds");
        cartService.removeSelected(userId, productIds);
        return ResponseEntity.ok(ApiResponse.success("勾选商品移除成功"));
    }
}