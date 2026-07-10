package com.ecommerce.cart.service.impl;

import com.ecommerce.cart.service.CartService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;
import java.util.Map;

@Service
public class CartServiceImpl implements CartService {

    private static final String CART_PREFIX = "cart:user:";

    @Autowired
    private RedisTemplate<String, Object> redisTemplate;

    @Override
    public void addToCart(Long userId, Long productId, Integer quantity) {
        String key = CART_PREFIX + userId;
        redisTemplate.opsForHash().put(key, productId.toString(), quantity);
    }

    @Override
    public Map<Object, Object> getCart(Long userId) {
        String key = CART_PREFIX + userId;
        return redisTemplate.opsForHash().entries(key);
    }

    @Override
    public void removeFromCart(Long userId, Long productId) {
        String key = CART_PREFIX + userId;
        redisTemplate.opsForHash().delete(key, productId.toString());
    }

    @Override
    public void clearCart(Long userId) {
        String key = CART_PREFIX + userId;
        redisTemplate.delete(key);
    }
}