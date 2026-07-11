package com.ecommerce.user.dto;

public record ResetPasswordRequest(
        String type,
        String newPassword
) {}
