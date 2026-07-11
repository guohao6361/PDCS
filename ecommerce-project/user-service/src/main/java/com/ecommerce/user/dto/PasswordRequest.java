package com.ecommerce.user.dto;

public record PasswordRequest(
        String oldPassword,
        String newPassword
) {}
