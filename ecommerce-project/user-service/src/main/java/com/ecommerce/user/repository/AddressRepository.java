package com.ecommerce.user.repository;

import com.ecommerce.user.entity.Address;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface AddressRepository extends JpaRepository<Address, Integer> {
    List<Address> findByUserIdOrderByIsDefaultDescIdAsc(Integer userId);
    long countByUserId(Integer userId);
    void deleteByUserId(Integer userId);
}
