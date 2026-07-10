package com.ecommerce.cart.service;

import java.util.Map;

public interface CartService {
    void addToCart(Long userId, Long productId, Integer quantity);
    Map<Object, Object> getCart(Long userId);
    void removeFromCart(Long userId, Long productId);
    void clearCart(Long userId);
}