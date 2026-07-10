package com.ecommerce.cart.service;

import com.ecommerce.cart.dto.CartResponse;

public interface CartService {
    void addToCart(Long userId, Long productId, Integer quantity);
    CartResponse getCart(Long userId);
    void removeFromCart(Long userId, Long productId);
    void clearCart(Long userId);
}