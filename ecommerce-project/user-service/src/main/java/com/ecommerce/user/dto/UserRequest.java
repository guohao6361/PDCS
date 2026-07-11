package com.ecommerce.user.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record UserRequest(
        @NotBlank(message = "用户名不能为空")
        @Size(min = 2, max = 20, message = "用户名长度需在2-20之间")
        String username,

        @NotBlank(message = "密码不能为空")
        @Size(min = 6, max = 50, message = "密码长度需在6-50之间")
        String password,

        String role,
        String payPassword,
        String phone,
        String email
) {}