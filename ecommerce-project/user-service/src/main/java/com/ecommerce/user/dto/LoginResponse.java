package com.ecommerce.user.dto;

import java.math.BigDecimal;

public record LoginResponse(String token, Integer userId, String username, BigDecimal balance) {}
