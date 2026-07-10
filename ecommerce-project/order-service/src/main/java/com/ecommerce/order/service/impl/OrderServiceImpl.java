package com.ecommerce.order.service.impl;

import com.ecommerce.common.ApiResponse;
import com.ecommerce.common.BusinessException;
import com.ecommerce.order.dto.OrderResponse;
import com.ecommerce.order.entity.Order;
import com.ecommerce.order.entity.OrderItem;
import com.ecommerce.order.repository.OrderRepository;
import com.ecommerce.order.service.OrderService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.client.RestTemplate;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@Service
public class OrderServiceImpl implements OrderService {

    private static final Logger log = LoggerFactory.getLogger(OrderServiceImpl.class);

    @Value("${app.service.cart-url}")
    private String cartServiceUrl;

    @Value("${app.service.product-url}")
    private String productServiceUrl;

    @Autowired
    private OrderRepository orderRepository;

    @Autowired
    private RestTemplate restTemplate;

    @Override
    @Transactional
    public OrderResponse createOrder(Integer userId) {
        // 1. 获取购物车
        String cartUrl = cartServiceUrl + "/cart/" + userId;
        ApiResponse<?> cartResp = restTemplate.getForObject(cartUrl, ApiResponse.class);

        if (cartResp == null || cartResp.getData() == null) {
            throw new BusinessException(400, "购物车为空");
        }

        // 解析购物车数据
        Map<String, Object> cartData = (Map<String, Object>) cartResp.getData();
        List<Map<String, Object>> items = (List<Map<String, Object>>) cartData.get("items");

        if (items == null || items.isEmpty()) {
            throw new BusinessException(400, "购物车为空");
        }

        // 2. 查询商品信息、计算总价
        BigDecimal totalPrice = BigDecimal.ZERO;
        List<OrderItem> orderItems = new ArrayList<>();

        for (Map<String, Object> cartItem : items) {
            Integer productId = Integer.parseInt(cartItem.get("productId").toString());
            Integer quantity = Integer.parseInt(cartItem.get("quantity").toString());

            // 查询商品信息
            String productUrl = productServiceUrl + "/products/" + productId;
            ApiResponse<?> productResp = restTemplate.getForObject(productUrl, ApiResponse.class);

            if (productResp == null || productResp.getData() == null) {
                throw new BusinessException(404, "商品不存在: " + productId);
            }

            Map<String, Object> product = (Map<String, Object>) productResp.getData();
            String productName = (String) product.get("name");
            BigDecimal price = new BigDecimal(product.get("price").toString());

            // 计算总价
            totalPrice = totalPrice.add(price.multiply(BigDecimal.valueOf(quantity)));

            // 创建订单项
            OrderItem item = new OrderItem();
            item.setProductId(productId);
            item.setProductName(productName);
            item.setPrice(price);
            item.setQuantity(quantity);
            orderItems.add(item);
        }

        // 3. 原子扣减库存（防止超卖）
        for (OrderItem item : orderItems) {
            String deductUrl = productServiceUrl + "/products/" + item.getProductId()
                    + "/deduct-stock?quantity=" + item.getQuantity();
            restTemplate.put(deductUrl, null);
        }

        // 4. 创建订单
        Order order = new Order();
        order.setUserId(userId);
        order.setTotalPrice(totalPrice);
        order.setStatus("CREATED");

        for (OrderItem item : orderItems) {
            item.setOrder(order);
        }
        order.setItems(orderItems);

        Order savedOrder = orderRepository.save(order);
        log.info("订单创建成功: orderId={}, userId={}, totalPrice={}", savedOrder.getId(), userId, totalPrice);

        // 5. 清空购物车（失败时补偿回滚订单）
        try {
            String clearCartUrl = cartServiceUrl + "/cart/" + userId;
            restTemplate.delete(clearCartUrl);
        } catch (Exception e) {
            log.error("清空购物车失败，回滚订单: orderId={}, error={}", savedOrder.getId(), e.getMessage());
            orderRepository.deleteById(savedOrder.getId());
            throw new BusinessException(500, "清空购物车失败，订单已回滚，请稍后重试");
        }

        return toResponse(savedOrder);
    }

    @Override
    public List<OrderResponse> getOrdersByUserId(Integer userId) {
        List<Order> orders = orderRepository.findByUserIdOrderByCreatedAtDesc(userId);
        return orders.stream().map(this::toResponse).toList();
    }

    @Override
    public OrderResponse getOrderById(Long id) {
        Order order = orderRepository.findById(id)
                .orElseThrow(() -> new BusinessException(404, "订单不存在"));
        return toResponse(order);
    }

    private OrderResponse toResponse(Order order) {
        OrderResponse response = new OrderResponse();
        response.setId(order.getId());
        response.setUserId(order.getUserId());
        response.setTotalPrice(order.getTotalPrice());
        response.setStatus(order.getStatus());
        response.setCreatedAt(order.getCreatedAt());

        List<OrderResponse.OrderItemResponse> itemResponses = new ArrayList<>();
        for (OrderItem item : order.getItems()) {
            OrderResponse.OrderItemResponse itemResp = new OrderResponse.OrderItemResponse();
            itemResp.setProductId(item.getProductId());
            itemResp.setProductName(item.getProductName());
            itemResp.setPrice(item.getPrice());
            itemResp.setQuantity(item.getQuantity());
            itemResponses.add(itemResp);
        }
        response.setItems(itemResponses);
        return response;
    }
}
