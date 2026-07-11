package com.ecommerce.order.controller;

import com.ecommerce.common.AdminRequired;
import com.ecommerce.common.ApiResponse;
import com.ecommerce.order.dto.*;
import com.ecommerce.order.service.OrderService;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/orders")
public class OrderController {

    @Autowired
    private OrderService orderService;

    @PostMapping
    public ResponseEntity<ApiResponse<OrderResponse>> createOrder(@Valid @RequestBody CreateOrderRequest request) {
        OrderResponse order = orderService.createOrder(request.userId());
        return ResponseEntity.ok(ApiResponse.success(order));
    }

    // 勾选结算
    @PostMapping("/selected")
    public ResponseEntity<ApiResponse<OrderResponse>> createSelectedOrder(@Valid @RequestBody SelectedOrderRequest request) {
        OrderResponse order = orderService.createSelectedOrder(request.userId(), request.productIds());
        return ResponseEntity.ok(ApiResponse.success(order));
    }

    @GetMapping("/user/{userId}")
    public ResponseEntity<ApiResponse<List<OrderResponse>>> getOrdersByUser(
            @PathVariable Integer userId, HttpServletRequest httpRequest) {
        Integer requestUserId = (Integer) httpRequest.getAttribute("userId");
        List<OrderResponse> orders = orderService.getOrdersByUserId(userId);
        return ResponseEntity.ok(ApiResponse.success(orders));
    }

    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse<OrderResponse>> getOrder(
            @PathVariable Long id, HttpServletRequest httpRequest) {
        Integer requestUserId = (Integer) httpRequest.getAttribute("userId");
        OrderResponse order = orderService.getOrderById(requestUserId, id);
        return ResponseEntity.ok(ApiResponse.success(order));
    }

    // 支付订单
    @PostMapping("/{id}/pay")
    public ResponseEntity<ApiResponse<OrderResponse>> payOrder(
            @PathVariable Long id,
            @RequestBody(required = false) PayRequest request,
            HttpServletRequest httpRequest) {
        Integer requestUserId = (Integer) httpRequest.getAttribute("userId");
        String payPassword = request != null ? request.payPassword() : null;
        Integer addressId = request != null ? request.addressId() : null;
        OrderResponse order = orderService.payOrder(requestUserId, id, payPassword, addressId);
        return ResponseEntity.ok(ApiResponse.success(order));
    }

    // 取消订单
    @PostMapping("/{id}/cancel")
    public ResponseEntity<ApiResponse<OrderResponse>> cancelOrder(
            @PathVariable Long id, HttpServletRequest httpRequest) {
        Integer requestUserId = (Integer) httpRequest.getAttribute("userId");
        OrderResponse order = orderService.cancelOrder(requestUserId, id);
        return ResponseEntity.ok(ApiResponse.success(order));
    }

    // 更新订单状态
    @PutMapping("/{id}/status")
    public ResponseEntity<ApiResponse<OrderResponse>> updateOrderStatus(
            @PathVariable Long id,
            @RequestBody UpdateStatusRequest request) {
        OrderResponse order = orderService.updateOrderStatus(id, request.status());
        return ResponseEntity.ok(ApiResponse.success(order));
    }

    // 商家订单列表
    @GetMapping("/merchant/{merchantId}")
    public ResponseEntity<ApiResponse<List<OrderResponse>>> getOrdersByMerchant(@PathVariable Integer merchantId) {
        List<OrderResponse> orders = orderService.getOrdersByMerchantId(merchantId);
        return ResponseEntity.ok(ApiResponse.success(orders));
    }

    // 管理员查看所有订单
    @GetMapping("/admin/orders")
    @AdminRequired
    public ResponseEntity<ApiResponse<List<OrderResponse>>> getAllOrders() {
        List<OrderResponse> orders = orderService.getAllOrders();
        return ResponseEntity.ok(ApiResponse.success(orders));
    }

    // 管理员修改订单
    @PutMapping("/{id}")
    @AdminRequired
    public ResponseEntity<ApiResponse<OrderResponse>> updateOrder(
            @PathVariable Long id,
            @RequestBody Map<String, String> body) {
        OrderResponse order = orderService.updateOrder(id, body.get("status"));
        return ResponseEntity.ok(ApiResponse.success(order));
    }

    // 管理员删除订单
    @DeleteMapping("/{id}")
    @AdminRequired
    public ResponseEntity<ApiResponse<Void>> deleteOrder(@PathVariable Long id) {
        orderService.deleteOrder(id);
        return ResponseEntity.ok(ApiResponse.success("订单删除成功"));
    }
}
