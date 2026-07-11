package com.ecommerce.product.repository;

import com.ecommerce.product.entity.Product;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;
import java.util.List;

public interface ProductRepository extends MongoRepository<Product, Integer> {
    @Query("{ $or: [ { 'name': { $regex: ?0, $options: 'i' } }, { 'category': { $regex: ?0, $options: 'i' } } ] }")
    Page<Product> searchByNameOrCategory(String keyword, Pageable pageable);
    List<Product> findByMerchantId(Integer merchantId);
    Page<Product> findByMerchantId(Integer merchantId, Pageable pageable);
}
