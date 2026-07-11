package com.ecommerce.cart.service.impl;

import com.ecommerce.cart.dto.CartItem;
import com.ecommerce.cart.dto.CartResponse;
import com.ecommerce.cart.service.CartService;
import com.ecommerce.common.BusinessException;
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
        // 先获取现有数量
        Object existingQty = redisTemplate.opsForHash().get(key, productId.toString());
        int currentQty = existingQty != null ? Integer.parseInt(existingQty.toString()) : 0;
        int newQty = currentQty + quantity;
        
        redisTemplate.opsForHash().put(key, productId.toString(), newQty);
        redisTemplate.expire(key, cartTtlDays, TimeUnit.DAYS);
        log.info("添加购物车: userId={}, productId={}, 原数量={}, 新增={}, 最终={}", 
                 userId, productId, currentQty, quantity, newQty);
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

    @Override
    public void updateQuantity(Long userId, Long productId, Integer quantity) {
        if (quantity == null || quantity < 1) {
            throw new BusinessException(400, "数量必须大于等于1");
        }
        String key = buildKey(userId);
        Object existing = redisTemplate.opsForHash().get(key, productId.toString());
        if (existing == null) {
            throw new BusinessException(404, "购物车中不存在该商品");
        }
        redisTemplate.opsForHash().put(key, productId.toString(), quantity);
        redisTemplate.expire(key, cartTtlDays, TimeUnit.DAYS);
        log.info("更新购物车数量: userId={}, productId={}, quantity={}", userId, productId, quantity);
    }

    @Override
    public void removeSelected(Long userId, List<Long> productIds) {
        if (productIds == null || productIds.isEmpty()) {
            throw new BusinessException(400, "商品ID列表不能为空");
        }
        String key = buildKey(userId);
        Object[] ids = productIds.stream().map(Object::toString).toArray();
        redisTemplate.opsForHash().delete(key, ids);
        redisTemplate.expire(key, cartTtlDays, TimeUnit.DAYS);
        log.info("移除购物车勾选商品: userId={}, productIds={}", userId, productIds);
    }
}