package com.ecommerce.user.dto;

public record ProfileRequest(
        String username,
        String phone,
        String email
) {}
