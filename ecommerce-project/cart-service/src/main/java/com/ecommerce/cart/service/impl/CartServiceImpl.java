package com.ecommerce.cart.service.impl;

import com.ecommerce.cart.dto.CartItem;
import com.ecommerce.cart.dto.CartResponse;
import com.ecommerce.cart.service.CartService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;

@Service
public class CartServiceImpl implements CartService {

    @Value("${app.cart.key-prefix:cart:user:}")
    private String cartKeyPrefix;

    @Value("${app.cart.ttl-days:7}")
    private long cartTtlDays;

    @Autowired
    private RedisTemplate<String, Object> redisTemplate;

    private String buildKey(Long userId) {
        return cartKeyPrefix + userId;
    }

    @Override
    public void addToCart(Long userId, Long productId, Integer quantity) {
        String key = buildKey(userId);
        redisTemplate.opsForHash().put(key, productId.toString(), quantity);
        redisTemplate.expire(key, cartTtlDays, TimeUnit.DAYS);
    }

    @Override
    public CartResponse getCart(Long userId) {
        String key = buildKey(userId);
        Map<Object, Object> entries = redisTemplate.opsForHash().entries(key);
        List<CartItem> items = entries.entrySet().stream()
                .map(e -> new CartItem(
                        Long.parseLong(e.getKey().toString()),
                        Integer.parseInt(e.getValue().toString())))
                .toList();
        return new CartResponse(userId, items);
    }

    @Override
    public void removeFromCart(Long userId, Long productId) {
        String key = buildKey(userId);
        redisTemplate.opsForHash().delete(key, productId.toString());
    }

    @Override
    public void clearCart(Long userId) {
        String key = buildKey(userId);
        redisTemplate.delete(key);
    }
}