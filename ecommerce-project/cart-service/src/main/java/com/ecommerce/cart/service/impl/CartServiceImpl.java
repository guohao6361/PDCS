package com.ecommerce.cart.service.impl;

import com.ecommerce.cart.dto.CartItem;
import com.ecommerce.cart.dto.CartResponse;
import com.ecommerce.cart.service.CartService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;

@Service
public class CartServiceImpl implements CartService {

    private static final Logger log = LoggerFactory.getLogger(CartServiceImpl.class);

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
        log.info("添加购物车: userId={}, productId={}, quantity={}", userId, productId, quantity);
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
        log.info("移除购物车商品: userId={}, productId={}", userId, productId);
    }

    @Override
    public void clearCart(Long userId) {
        String key = buildKey(userId);
        redisTemplate.delete(key);
        log.info("清空购物车: userId={}", userId);
    }
}