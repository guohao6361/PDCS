package com.ecommerce.cart.service;

import com.ecommerce.cart.dto.CartResponse;
import java.util.List;

public interface CartService {
    void addToCart(Long userId, Long productId, Integer quantity);
    CartResponse getCart(Long userId);
    void removeFromCart(Long userId, Long productId);
    void clearCart(Long userId);
    void updateQuantity(Long userId, Long productId, Integer quantity);
    void removeSelected(Long userId, List<Long> productIds);
}