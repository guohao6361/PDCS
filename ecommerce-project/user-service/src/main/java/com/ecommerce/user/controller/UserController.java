package com.ecommerce.user.controller;

import com.ecommerce.common.ApiResponse;
import com.ecommerce.user.dto.LoginResponse;
import com.ecommerce.user.dto.UserRequest;
import com.ecommerce.user.entity.User;
import com.ecommerce.user.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/users")
public class UserController {

    @Autowired
    private UserService userService;

    @PostMapping("/register")
    public ResponseEntity<ApiResponse<User>> register(@RequestBody UserRequest request) {
        User user = userService.register(request.username(), request.password());
        return ResponseEntity.ok(ApiResponse.success(user));
    }

    @PostMapping("/login")
    public ResponseEntity<ApiResponse<LoginResponse>> login(@RequestBody UserRequest request) {
        LoginResponse response = userService.login(request.username(), request.password());
        return ResponseEntity.ok(ApiResponse.success(response));
    }
}