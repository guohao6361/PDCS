package com.ecommerce.user.service;

import com.ecommerce.user.dto.LoginResponse;
import com.ecommerce.user.dto.RegisterResponse;

public interface UserService {
    RegisterResponse register(String username, String password);
    LoginResponse login(String username, String password);
}