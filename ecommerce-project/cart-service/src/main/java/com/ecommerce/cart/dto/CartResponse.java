package com.ecommerce.cart.dto;

import java.util.List;

public class CartResponse {
    private Long userId;
    private List<CartItem> items;

    public CartResponse(Long userId, List<CartItem> items) {
        this.userId = userId;
        this.items = items;
    }

    public Long getUserId() { return userId; }
    public List<CartItem> getItems() { return items; }
}
