package com.ecommerce.cart.controller;

import com.ecommerce.cart.dto.CartItemRequest;
import com.ecommerce.cart.service.CartService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.util.Map;

@CrossOrigin
@RestController
@RequestMapping("/cart")
public class CartController {

    @Autowired
    private CartService cartService;

    @PostMapping("/add")
    public String add(@RequestBody CartItemRequest request) {
        cartService.addToCart(
            request.getUserId(),
            request.getProductId(),
            request.getQuantity()
        );
        return "Added to cart";
    }

    @GetMapping("/{userId}")
    public Map<Object, Object> get(@PathVariable Long userId) {
        return cartService.getCart(userId);
    }

    @DeleteMapping("/{userId}/{productId}")
    public String delete(@PathVariable Long userId, @PathVariable Long productId) {
        cartService.removeFromCart(userId, productId);
        return "Deleted";
    }
}