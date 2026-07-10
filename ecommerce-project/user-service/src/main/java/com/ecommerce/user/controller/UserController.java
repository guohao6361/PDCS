package com.ecommerce.user.controller;

import com.ecommerce.common.ApiResponse;
import com.ecommerce.user.dto.LoginResponse;
import com.ecommerce.user.dto.RegisterResponse;
import com.ecommerce.user.dto.UserRequest;
import com.ecommerce.user.service.UserService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/users")
public class UserController {

    @Autowired
    private UserService userService;

    @PostMapping("/register")
    public ResponseEntity<ApiResponse<RegisterResponse>> register(@Valid @RequestBody UserRequest request) {
        RegisterResponse response = userService.register(request.username(), request.password());
        return ResponseEntity.ok(ApiResponse.success(response));
    }

    @PostMapping("/login")
    public ResponseEntity<ApiResponse<LoginResponse>> login(@Valid @RequestBody UserRequest request) {
        LoginResponse response = userService.login(request.username(), request.password());
        return ResponseEntity.ok(ApiResponse.success(response));
    }
}