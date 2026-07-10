package com.ecommerce.order.dto;

import jakarta.validation.constraints.NotNull;

public record CreateOrderRequest(
        @NotNull(message = "用户ID不能为空")
        Integer userId
) {}
