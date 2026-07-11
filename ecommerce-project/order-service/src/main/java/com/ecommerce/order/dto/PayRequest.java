package com.ecommerce.order.dto;

public record PayRequest(
        String payPassword,
        Integer addressId
) {}
