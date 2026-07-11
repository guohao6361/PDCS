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
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;

@Service
public class OrderServiceImpl implements OrderService {

    private static final Logger log = LoggerFactory.getLogger(OrderServiceImpl.class);

    @Value("${app.service.cart-url}")
    private String cartServiceUrl;

    @Value("${app.service.product-url}")
    private String productServiceUrl;

    @Value("${app.service.user-url}")
    private String userServiceUrl;

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

        Map<String, Object> cartData = (Map<String, Object>) cartResp.getData();
        List<Map<String, Object>> items = (List<Map<String, Object>>) cartData.get("items");

        if (items == null || items.isEmpty()) {
            throw new BusinessException(400, "购物车为空");
        }

        return buildOrderFromCartItems(userId, items, items.size());
    }

    @Override
    @Transactional
    public OrderResponse createSelectedOrder(Integer userId, List<Integer> productIds) {
        if (productIds == null || productIds.isEmpty()) {
            throw new BusinessException(400, "商品ID列表不能为空");
        }

        // 1. 获取购物车
        String cartUrl = cartServiceUrl + "/cart/" + userId;
        ApiResponse<?> cartResp = restTemplate.getForObject(cartUrl, ApiResponse.class);

        if (cartResp == null || cartResp.getData() == null) {
            throw new BusinessException(400, "购物车为空");
        }

        Map<String, Object> cartData = (Map<String, Object>) cartResp.getData();
        List<Map<String, Object>> allItems = (List<Map<String, Object>>) cartData.get("items");

        if (allItems == null || allItems.isEmpty()) {
            throw new BusinessException(400, "购物车为空");
        }

        // 2. 过滤出勾选的商品
        List<Map<String, Object>> selectedItems = allItems.stream()
                .filter(item -> {
                    Integer pid = Integer.parseInt(item.get("productId").toString());
                    return productIds.contains(pid);
                })
                .toList();

        if (selectedItems.isEmpty()) {
            throw new BusinessException(400, "勾选的商品不在购物车中");
        }

        OrderResponse response = buildOrderFromCartItems(userId, selectedItems, allItems.size());

        // 3. 仅从购物车移除勾选的商品
        try {
            String removeUrl = cartServiceUrl + "/cart/" + userId + "/remove-selected";
            restTemplate.postForObject(removeUrl, Map.of("productIds", productIds), ApiResponse.class);
        } catch (Exception e) {
            log.warn("移除购物车勾选商品失败: {}", e.getMessage());
        }

        return response;
    }

    private OrderResponse buildOrderFromCartItems(Integer userId, List<Map<String, Object>> items, int allItemsCount) {
        // 生成购物车快照并检查是否已有相同订单
        String cartSnapshot = generateCartSnapshot(userId, items);
        var existingOrder = orderRepository.findByUserIdAndStatusAndCartSnapshot(userId, "UNPAID", cartSnapshot);
        if (existingOrder.isPresent()) {
            log.warn("检测到重复订单请求，返回已有订单: orderId={}", existingOrder.get().getId());
            return toResponse(existingOrder.get());
        }

        // 查询商品信息、计算总价
        BigDecimal totalPrice = BigDecimal.ZERO;
        List<OrderItem> orderItems = new ArrayList<>();
        Integer merchantId = null;

        for (Map<String, Object> cartItem : items) {
            Integer productId = Integer.parseInt(cartItem.get("productId").toString());
            Integer quantity = Integer.parseInt(cartItem.get("quantity").toString());

            String productUrl = productServiceUrl + "/products/" + productId;
            ApiResponse<?> productResp = restTemplate.getForObject(productUrl, ApiResponse.class);

            if (productResp == null || productResp.getData() == null) {
                throw new BusinessException(404, "商品不存在: " + productId);
            }

            Map<String, Object> product = (Map<String, Object>) productResp.getData();
            String productName = (String) product.get("name");
            BigDecimal price = new BigDecimal(product.get("price").toString());

            if (product.get("merchantId") != null) {
                merchantId = Integer.parseInt(product.get("merchantId").toString());
            }

            totalPrice = totalPrice.add(price.multiply(BigDecimal.valueOf(quantity)));

            OrderItem item = new OrderItem();
            item.setProductId(productId);
            item.setProductName(productName);
            item.setPrice(price);
            item.setQuantity(quantity);
            orderItems.add(item);
        }

        Order order = new Order();
        order.setUserId(userId);
        order.setMerchantId(merchantId);
        order.setTotalPrice(totalPrice);
        order.setStatus("UNPAID");
        order.setCartSnapshot(cartSnapshot);

        for (OrderItem item : orderItems) {
            item.setOrder(order);
        }
        order.setItems(orderItems);

        Order savedOrder = orderRepository.save(order);
        log.info("订单创建成功: orderId={}, userId={}, totalPrice={}", savedOrder.getId(), userId, totalPrice);

        // 清空购物车（仅全量下单时：购物车商品数 == 本次下单商品数）
        if (allItemsCount >= 0 && items.size() == allItemsCount) {
            try {
                String clearCartUrl = cartServiceUrl + "/cart/" + userId;
                restTemplate.delete(clearCartUrl);
            } catch (Exception e) {
                log.error("清空购物车失败，回滚订单: orderId={}, error={}", savedOrder.getId(), e.getMessage());
                orderRepository.deleteById(savedOrder.getId());
                throw new BusinessException(500, "清空购物车失败，订单已回滚，请稍后重试");
            }
        }

        return toResponse(savedOrder);
    }

    @Override
    public List<OrderResponse> getOrdersByUserId(Integer userId) {
        return getOrdersByUserId(userId, userId);
    }

    public List<OrderResponse> getOrdersByUserId(Integer requestUserId, Integer userId) {
        // 安全修复: 用户归属校验
        if (requestUserId != null && !requestUserId.equals(userId)) {
            throw new BusinessException(403, "无权查看他人订单");
        }
        List<Order> orders = orderRepository.findByUserIdOrderByCreatedAtDesc(userId);
        return orders.stream().map(this::toResponse).toList();
    }

    @Override
    public List<OrderResponse> getAllOrders() {
        List<Order> orders = orderRepository.findAll();
        return orders.stream().map(this::toResponse).toList();
    }

    @Override
    public OrderResponse getOrderById(Integer requestUserId, Long id) {
        Order order = orderRepository.findById(id)
                .orElseThrow(() -> new BusinessException(404, "订单不存在"));
        // 安全修复: 用户归属校验
        if (requestUserId != null && !requestUserId.equals(order.getUserId())) {
            throw new BusinessException(403, "无权查看他人订单");
        }
        return toResponse(order);
    }

    @Override
    @Transactional
    public OrderResponse payOrder(Integer requestUserId, Long orderId, String payPassword, Integer addressId) {
        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new BusinessException(404, "订单不存在"));

        // 安全修复: 用户归属校验
        if (requestUserId != null && !requestUserId.equals(order.getUserId())) {
            throw new BusinessException(403, "无权操作他人订单");
        }

        if (!"UNPAID".equals(order.getStatus())) {
            throw new BusinessException(400, "仅可支付UNPAID状态的订单，当前状态: " + order.getStatus());
        }

        // 15分钟超时校验
        if (order.getCreatedAt() != null && order.getCreatedAt().plusMinutes(15).isBefore(LocalDateTime.now())) {
            order.setStatus("CANCELLED");
            orderRepository.save(order);
            // 恢复库存
            restoreOrderStock(order);
            throw new BusinessException(400, "订单已超时（超过15分钟），已自动取消");
        }

        // 验证支付密码
        if (payPassword != null && !payPassword.isBlank()) {
            String verifyUrl = userServiceUrl + "/users/" + order.getUserId() + "/verify-pay-password";
            try {
                restTemplate.postForObject(verifyUrl, Map.of("payPassword", payPassword), ApiResponse.class);
            } catch (Exception e) {
                throw new BusinessException(400, "支付密码错误");
            }
        }

        // 扣减库存
        for (OrderItem item : order.getItems()) {
            String deductUrl = productServiceUrl + "/products/" + item.getProductId()
                    + "/deduct-stock?quantity=" + item.getQuantity();
            try {
                restTemplate.put(deductUrl, null);
            } catch (Exception e) {
                log.error("扣减库存失败: productId={}, quantity={}, error={}",
                        item.getProductId(), item.getQuantity(), e.getMessage());
                throw new BusinessException(500, "支付失败: 库存扣减异常");
            }
        }

        // 扣减用户余额（失败时回滚已扣库存）
        String deductUrl = userServiceUrl + "/users/" + order.getUserId()
                + "/deduct-balance?amount=" + order.getTotalPrice();
        try {
            restTemplate.put(deductUrl, null);
        } catch (Exception e) {
            log.error("扣减余额失败，回滚库存: userId={}, amount={}, error={}", order.getUserId(), order.getTotalPrice(), e.getMessage());
            restoreOrderStock(order); // 安全修复: 余额扣减失败时回滚已扣库存
            throw new BusinessException(500, "支付失败: " + e.getMessage());
        }

        // 更新订单状态
        order.setStatus("PAID");
        if (addressId != null) {
            order.setAddressId(addressId);
        }
        Order savedOrder = orderRepository.save(order);
        log.info("订单支付成功: orderId={}, userId={}, amount={}", orderId, order.getUserId(), order.getTotalPrice());

        return toResponse(savedOrder);
    }

    @Override
    @Transactional
    public OrderResponse cancelOrder(Integer requestUserId, Long orderId) {
        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new BusinessException(404, "订单不存在"));

        // 安全修复: 用户归属校验
        if (requestUserId != null && !requestUserId.equals(order.getUserId())) {
            throw new BusinessException(403, "无权操作他人订单");
        }

        if (!"UNPAID".equals(order.getStatus())) {
            throw new BusinessException(400, "仅可取消UNPAID状态的订单，当前状态: " + order.getStatus());
        }

        // 恢复库存
        restoreOrderStock(order);

        order.setStatus("CANCELLED");
        Order savedOrder = orderRepository.save(order);
        log.info("订单取消成功: orderId={}, userId={}", orderId, order.getUserId());

        return toResponse(savedOrder);
    }

    @Override
    @Transactional
    public OrderResponse updateOrderStatus(Long orderId, String newStatus) {
        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new BusinessException(404, "订单不存在"));

        // 状态流转校验
        String current = order.getStatus();
        boolean valid = switch (newStatus) {
            case "PAID" -> "UNPAID".equals(current);
            case "SHIPPED" -> "PAID".equals(current);
            case "IN_TRANSIT" -> "SHIPPED".equals(current);
            case "DELIVERED" -> "IN_TRANSIT".equals(current);
            case "COMPLETED" -> "DELIVERED".equals(current);
            case "CANCELLED" -> "UNPAID".equals(current) || "PAID".equals(current);
            default -> false;
        };

        if (!valid) {
            throw new BusinessException(400, "不允许从 " + current + " 变更为 " + newStatus);
        }

        // 取消时恢复库存
        if ("CANCELLED".equals(newStatus) && "PAID".equals(current)) {
            // 已支付的取消需要退款（简化处理：仅恢复库存）
            restoreOrderStock(order);
        }

        order.setStatus(newStatus);
        Order savedOrder = orderRepository.save(order);
        log.info("订单状态更新: orderId={}, {} -> {}", orderId, current, newStatus);

        return toResponse(savedOrder);
    }

    @Override
    public List<OrderResponse> getOrdersByMerchantId(Integer merchantId) {
        List<Order> orders = orderRepository.findByMerchantIdOrderByCreatedAtDesc(merchantId);
        return orders.stream().map(this::toResponse).toList();
    }

    @Override
    @Transactional
    public OrderResponse updateOrder(Long orderId, String status) {
        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new BusinessException(404, "订单不存在"));
        // 安全修复: 管理员修改订单也必须经过状态机校验
        if (status != null && !status.isBlank()) {
            String current = order.getStatus();
            boolean valid = switch (status) {
                case "PAID" -> "UNPAID".equals(current);
                case "SHIPPED" -> "PAID".equals(current);
                case "IN_TRANSIT" -> "SHIPPED".equals(current);
                case "DELIVERED" -> "IN_TRANSIT".equals(current);
                case "COMPLETED" -> "DELIVERED".equals(current);
                case "CANCELLED" -> "UNPAID".equals(current) || "PAID".equals(current);
                default -> false;
            };
            if (!valid) {
                throw new BusinessException(400, "不允许从 " + current + " 变更为 " + status);
            }
            order.setStatus(status);
        }
        Order savedOrder = orderRepository.save(order);
        return toResponse(savedOrder);
    }

    @Override
    public void deleteOrder(Long orderId) {
        if (!orderRepository.existsById(orderId)) {
            throw new BusinessException(404, "订单不存在");
        }
        orderRepository.deleteById(orderId);
        log.info("订单删除成功: orderId={}", orderId);
    }

    private void restoreOrderStock(Order order) {
        for (OrderItem item : order.getItems()) {
            String restoreUrl = productServiceUrl + "/products/" + item.getProductId()
                    + "/restore-stock?quantity=" + item.getQuantity();
            try {
                restTemplate.put(restoreUrl, null);
            } catch (Exception e) {
                log.error("恢复库存失败: productId={}, error={}", item.getProductId(), e.getMessage());
            }
        }
    }

    private OrderResponse toResponse(Order order) {
        OrderResponse response = new OrderResponse();
        response.setId(order.getId());
        response.setUserId(order.getUserId());
        response.setMerchantId(order.getMerchantId());
        response.setAddressId(order.getAddressId());
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

    private String generateCartSnapshot(Integer userId, List<Map<String, Object>> items) {
        try {
            StringBuilder sb = new StringBuilder(userId.toString());
            items.stream()
                .sorted((a, b) -> a.get("productId").toString().compareTo(b.get("productId").toString()))
                .forEach(item -> sb.append(":").append(item.get("productId")).append("-").append(item.get("quantity")));

            MessageDigest md = MessageDigest.getInstance("MD5");
            byte[] digest = md.digest(sb.toString().getBytes(StandardCharsets.UTF_8));
            StringBuilder hexString = new StringBuilder();
            for (byte b : digest) {
                String hex = Integer.toHexString(0xff & b);
                if (hex.length() == 1) hexString.append('0');
                hexString.append(hex);
            }
            return hexString.toString();
        } catch (Exception e) {
            log.error("生成购物车快照失败: {}", e.getMessage());
            return String.valueOf(System.currentTimeMillis());
        }
    }
}
