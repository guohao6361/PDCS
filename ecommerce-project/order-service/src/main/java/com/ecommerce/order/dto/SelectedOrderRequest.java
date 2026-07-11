package com.ecommerce.order.dto;

import jakarta.validation.constraints.NotNull;
import java.util.List;

public record SelectedOrderRequest(
        @NotNull(message = "用户ID不能为空")
        Integer userId,
        @NotNull(message = "商品ID列表不能为空")
        List<Integer> productIds
) {}
