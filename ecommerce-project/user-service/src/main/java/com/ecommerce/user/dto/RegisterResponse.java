package com.ecommerce.user.dto;

import java.math.BigDecimal;

public record RegisterResponse(Integer userId, String username, BigDecimal balance, String role) {}
