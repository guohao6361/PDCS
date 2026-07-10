package com.ecommerce.user.service;

import com.ecommerce.user.entity.User;

public interface UserService {
    User register(String username, String password);
    User login(String username, String password);
}