package com.ecommerce.cart.dto;

public class CartItem {
    private Long productId;
    private Integer quantity;

    public CartItem(Long productId, Integer quantity) {
        this.productId = productId;
        this.quantity = quantity;
    }

    public Long getProductId() { return productId; }
    public Integer getQuantity() { return quantity; }
}
