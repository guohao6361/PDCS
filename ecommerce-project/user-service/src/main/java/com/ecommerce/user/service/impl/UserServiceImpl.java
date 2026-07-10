package com.ecommerce.user.service.impl;

import com.ecommerce.common.BusinessException;
import com.ecommerce.user.config.JwtUtil;
import com.ecommerce.user.dto.LoginResponse;
import com.ecommerce.user.dto.RegisterResponse;
import com.ecommerce.user.entity.User;
import com.ecommerce.user.repository.UserRepository;
import com.ecommerce.user.service.UserService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import java.math.BigDecimal;

@Service
public class UserServiceImpl implements UserService {

    private static final Logger log = LoggerFactory.getLogger(UserServiceImpl.class);

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private JwtUtil jwtUtil;

    @Autowired
    private PasswordEncoder passwordEncoder;

    @Value("${app.user.default-balance:1000.00}")
    private BigDecimal defaultBalance;

    @Value("${app.user.password-min-length:6}")
    private int passwordMinLength;

    @Override
    public RegisterResponse register(String username, String password) {
        if (userRepository.findByUsername(username).isPresent()) {
            throw new BusinessException(400, "用户名已存在");
        }
        if (password == null || password.length() < passwordMinLength) {
            throw new BusinessException(400, "密码长度不能少于" + passwordMinLength + "位");
        }
        User user = new User();
        user.setUsername(username);
        user.setPassword(passwordEncoder.encode(password));
        user.setBalance(defaultBalance);
        User saved = userRepository.save(user);
        log.info("用户注册成功: userId={}, username={}", saved.getId(), saved.getUsername());
        return new RegisterResponse(saved.getId(), saved.getUsername(), saved.getBalance());
    }

    @Override
    public LoginResponse login(String username, String password) {
        User user = userRepository.findByUsername(username)
                .orElseThrow(() -> new BusinessException(400, "用户不存在"));
        if (!passwordEncoder.matches(password, user.getPassword())) {
            throw new BusinessException(400, "密码错误");
        }
        String token = jwtUtil.generateToken(user.getId(), user.getUsername());
        log.info("用户登录成功: userId={}, username={}", user.getId(), user.getUsername());
        return new LoginResponse(token, user.getId(), user.getUsername(), user.getBalance());
    }
}