package com.ecommerce.order.service;

import com.ecommerce.order.dto.OrderResponse;
import java.util.List;

public interface OrderService {
    OrderResponse createOrder(Integer userId);
    OrderResponse createSelectedOrder(Integer userId, List<Integer> productIds);
    List<OrderResponse> getOrdersByUserId(Integer userId);
    OrderResponse getOrderById(Integer requestUserId, Long id);
    OrderResponse payOrder(Integer requestUserId, Long orderId, String payPassword, Integer addressId);
    OrderResponse cancelOrder(Integer requestUserId, Long orderId);
    OrderResponse updateOrderStatus(Long orderId, String newStatus);
    List<OrderResponse> getOrdersByMerchantId(Integer merchantId);
    List<OrderResponse> getAllOrders();
    OrderResponse updateOrder(Long orderId, String status);
    void deleteOrder(Long orderId);
}
