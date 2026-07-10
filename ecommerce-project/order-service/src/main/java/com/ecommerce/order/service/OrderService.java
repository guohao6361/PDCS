package com.ecommerce.order.service;

import com.ecommerce.order.dto.OrderResponse;
import java.util.List;

public interface OrderService {
    OrderResponse createOrder(Integer userId);
    List<OrderResponse> getOrdersByUserId(Integer userId);
    OrderResponse getOrderById(Long id);
}
