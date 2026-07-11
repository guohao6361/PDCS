package com.ecommerce.order.repository;

import com.ecommerce.order.entity.Order;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;
import java.util.Optional;

public interface OrderRepository extends JpaRepository<Order, Long> {
    List<Order> findByUserIdOrderByCreatedAtDesc(Integer userId);
    Optional<Order> findByUserIdAndStatusAndCartSnapshot(Integer userId, String status, String cartSnapshot);
    List<Order> findByMerchantIdOrderByCreatedAtDesc(Integer merchantId);
    void deleteByUserId(Integer userId);
}
