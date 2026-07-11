package com.ecommerce.user.dto;

public record PayPasswordRequest(
        String oldPayPassword,
        String newPayPassword
) {}
