package com.ecommerce.cart.dto;

import lombok.Data;

@Data
public class CartItemRequest {
    private Long userId;
    private Long productId;
    private Integer quantity;
}