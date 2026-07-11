package com.ecommerce.user.service.impl;

import com.ecommerce.common.BusinessException;
import com.ecommerce.user.config.JwtUtil;
import com.ecommerce.user.dto.LoginResponse;
import com.ecommerce.user.dto.RegisterResponse;
import com.ecommerce.user.entity.Address;
import com.ecommerce.user.entity.User;
import com.ecommerce.user.repository.AddressRepository;
import com.ecommerce.user.repository.UserRepository;
import com.ecommerce.user.service.UserService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.client.RestTemplate;

import java.io.IOException;
import java.math.BigDecimal;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.util.List;

@Service
public class UserServiceImpl implements UserService, CommandLineRunner {

    private static final Logger log = LoggerFactory.getLogger(UserServiceImpl.class);

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private AddressRepository addressRepository;

    @Autowired
    private JwtUtil jwtUtil;

    @Autowired
    private PasswordEncoder passwordEncoder;

    @Autowired
    private RestTemplate restTemplate;

    @Value("${app.service.product-url:http://localhost:8082}")
    private String productServiceUrl;

    @Value("${app.service.order-url:http://localhost:8084}")
    private String orderServiceUrl;

    @Value("${app.user.default-balance:1000.00}")
    private BigDecimal defaultBalance;

    @Value("${app.user.password-min-length:6}")
    private int passwordMinLength;

    @Value("${app.upload.avatars-dir:uploads/avatars}")
    private String avatarsDir;

    @Override
    public RegisterResponse register(String username, String password, String role, String payPassword, String phone, String email) {
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
        // 仅允许 USER 或 MERCHANT 角色，禁止注册 ADMIN
        String finalRole = "MERCHANT".equals(role) ? "MERCHANT" : "USER";
        user.setRole(finalRole);
        user.setPhone(phone);
        user.setEmail(email);
        if (payPassword != null && !payPassword.isBlank()) {
            if (payPassword.length() != 6 || !payPassword.matches("\\d{6}")) {
                throw new BusinessException(400, "支付密码必须为6位数字");
            }
            user.setPayPassword(passwordEncoder.encode(payPassword));
        }
        User saved = userRepository.save(user);
        log.info("用户注册成功: userId={}, username={}, role={}", saved.getId(), saved.getUsername(), saved.getRole());
        return new RegisterResponse(saved.getId(), saved.getUsername(), saved.getBalance(), saved.getRole());
    }

    @Override
    public LoginResponse login(String username, String password) {
        User user = userRepository.findByUsername(username)
                .orElseThrow(() -> new BusinessException(400, "用户不存在"));
        if (!passwordEncoder.matches(password, user.getPassword())) {
            throw new BusinessException(400, "密码错误");
        }
        String token = jwtUtil.generateToken(user.getId(), user.getUsername(), user.getRole());
        log.info("用户登录成功: userId={}, username={}", user.getId(), user.getUsername());
        return new LoginResponse(token, user.getId(), user.getUsername(), user.getBalance(), user.getRole());
    }

    @Override
    public void deductBalance(Integer userId, BigDecimal amount) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new BusinessException(404, "用户不存在"));
        if (user.getBalance().compareTo(amount) < 0) {
            throw new BusinessException(400, "余额不足，当前余额: " + user.getBalance() + ", 需要: " + amount);
        }
        user.setBalance(user.getBalance().subtract(amount));
        userRepository.save(user);
        log.info("余额扣减成功: userId={}, amount={}, remaining={}", userId, amount, user.getBalance());
    }

    @Override
    public List<User> getAllUsers() {
        return userRepository.findAll();
    }

    @Override
    public User getUserById(Integer id) {
        return userRepository.findById(id)
                .orElseThrow(() -> new BusinessException(404, "用户不存在"));
    }

    @Override
    public User updateProfile(Integer id, String username, String phone, String email) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new BusinessException(404, "用户不存在"));
        if (username != null && !username.isBlank()) user.setUsername(username);
        if (phone != null) user.setPhone(phone);
        if (email != null) user.setEmail(email);
        return userRepository.save(user);
    }

    @Override
    public User getProfile(Integer id) {
        return userRepository.findById(id)
                .orElseThrow(() -> new BusinessException(404, "用户不存在"));
    }

    @Override
    public void changePassword(Integer id, String oldPassword, String newPassword) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new BusinessException(404, "用户不存在"));
        if (!passwordEncoder.matches(oldPassword, user.getPassword())) {
            throw new BusinessException(400, "原密码错误");
        }
        if (newPassword == null || newPassword.length() < passwordMinLength) {
            throw new BusinessException(400, "新密码长度不能少于" + passwordMinLength + "位");
        }
        user.setPassword(passwordEncoder.encode(newPassword));
        userRepository.save(user);
        log.info("用户修改登录密码成功: userId={}", id);
    }

    @Override
    public void changePayPassword(Integer id, String oldPayPassword, String newPayPassword) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new BusinessException(404, "用户不存在"));
        if (user.getPayPassword() == null || user.getPayPassword().isBlank()) {
            throw new BusinessException(400, "未设置支付密码");
        }
        if (!passwordEncoder.matches(oldPayPassword, user.getPayPassword())) {
            throw new BusinessException(400, "原支付密码错误");
        }
        if (newPayPassword == null || newPayPassword.length() != 6 || !newPayPassword.matches("\\d{6}")) {
            throw new BusinessException(400, "新支付密码必须为6位数字");
        }
        user.setPayPassword(passwordEncoder.encode(newPayPassword));
        userRepository.save(user);
        log.info("用户修改支付密码成功: userId={}", id);
    }

    @Override
    public void resetPassword(Integer id, String type, String newPassword) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new BusinessException(404, "用户不存在"));
        if ("LOGIN".equals(type)) {
            if (newPassword == null || newPassword.length() < passwordMinLength) {
                throw new BusinessException(400, "密码长度不能少于" + passwordMinLength + "位");
            }
            user.setPassword(passwordEncoder.encode(newPassword));
        } else if ("PAY".equals(type)) {
            if (newPassword == null || newPassword.length() != 6 || !newPassword.matches("\\d{6}")) {
                throw new BusinessException(400, "支付密码必须为6位数字");
            }
            user.setPayPassword(passwordEncoder.encode(newPassword));
        } else {
            throw new BusinessException(400, "type 必须为 LOGIN 或 PAY");
        }
        userRepository.save(user);
        log.info("用户重置{}密码成功: userId={}", type, id);
    }

    private static final List<String> ALLOWED_IMAGE_TYPES = List.of("image/jpeg", "image/png", "image/gif", "image/webp");

    @Override
    public String uploadAvatar(Integer id, byte[] fileData, String originalFilename) {
        return uploadAvatar(id, fileData, originalFilename, null);
    }

    @Override
    public String uploadAvatar(Integer id, byte[] fileData, String originalFilename, String contentType) {
        // 安全修复: 文件类型校验
        if (contentType != null && !ALLOWED_IMAGE_TYPES.contains(contentType.toLowerCase())) {
            throw new BusinessException(400, "仅支持 JPG/PNG/GIF/WebP 图片格式");
        }
        User user = userRepository.findById(id)
                .orElseThrow(() -> new BusinessException(404, "用户不存在"));
        try {
            Path dir = Paths.get(avatarsDir);
            Files.createDirectories(dir);
            String ext = originalFilename != null && originalFilename.contains(".")
                    ? originalFilename.substring(originalFilename.lastIndexOf("."))
                    : ".jpg";
            String filename = "user_" + id + "_" + System.currentTimeMillis() + ext;
            Path filePath = dir.resolve(filename);
            Files.write(filePath, fileData, StandardOpenOption.CREATE, StandardOpenOption.TRUNCATE_EXISTING);
            String avatarUrl = "/uploads/avatars/" + filename;
            user.setAvatar(avatarUrl);
            userRepository.save(user);
            log.info("头像上传成功: userId={}, url={}", id, avatarUrl);
            return avatarUrl;
        } catch (IOException e) {
            log.error("头像上传失败: userId={}, error={}", id, e.getMessage());
            throw new BusinessException(500, "头像上传失败");
        }
    }

    // ===== Address 管理 =====

    @Override
    public List<Address> getAddresses(Integer userId) {
        return addressRepository.findByUserIdOrderByIsDefaultDescIdAsc(userId);
    }

    @Override
    public Address addAddress(Integer userId, Address address) {
        if (addressRepository.countByUserId(userId) >= 10) {
            throw new BusinessException(400, "收货地址最多保存10个");
        }
        address.setUserId(userId);
        if (Boolean.TRUE.equals(address.getIsDefault())) {
            clearDefaultAddresses(userId);
        }
        return addressRepository.save(address);
    }

    @Override
    public Address updateAddress(Integer userId, Integer addressId, Address updates) {
        Address address = addressRepository.findById(addressId)
                .orElseThrow(() -> new BusinessException(404, "地址不存在"));
        if (!address.getUserId().equals(userId)) {
            throw new BusinessException(403, "无权修改此地址");
        }
        if (updates.getReceiverName() != null) address.setReceiverName(updates.getReceiverName());
        if (updates.getPhone() != null) address.setPhone(updates.getPhone());
        if (updates.getProvince() != null) address.setProvince(updates.getProvince());
        if (updates.getCity() != null) address.setCity(updates.getCity());
        if (updates.getDistrict() != null) address.setDistrict(updates.getDistrict());
        if (updates.getDetailAddress() != null) address.setDetailAddress(updates.getDetailAddress());
        if (Boolean.TRUE.equals(updates.getIsDefault())) {
            clearDefaultAddresses(userId);
            address.setIsDefault(true);
        }
        return addressRepository.save(address);
    }

    @Override
    public void deleteAddress(Integer userId, Integer addressId) {
        Address address = addressRepository.findById(addressId)
                .orElseThrow(() -> new BusinessException(404, "地址不存在"));
        if (!address.getUserId().equals(userId)) {
            throw new BusinessException(403, "无权删除此地址");
        }
        addressRepository.delete(address);
    }

    @Override
    public Address setDefaultAddress(Integer userId, Integer addressId) {
        Address address = addressRepository.findById(addressId)
                .orElseThrow(() -> new BusinessException(404, "地址不存在"));
        if (!address.getUserId().equals(userId)) {
            throw new BusinessException(403, "无权修改此地址");
        }
        clearDefaultAddresses(userId);
        address.setIsDefault(true);
        return addressRepository.save(address);
    }

    private void clearDefaultAddresses(Integer userId) {
        List<Address> defaults = addressRepository.findByUserIdOrderByIsDefaultDescIdAsc(userId);
        for (Address a : defaults) {
            if (Boolean.TRUE.equals(a.getIsDefault())) {
                a.setIsDefault(false);
                addressRepository.save(a);
            }
        }
    }

    // ===== 管理员操作 =====

    @Override
    public void deleteUser(Integer id) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new BusinessException(404, "用户不存在"));
        
        // 商家删除时，级联删除其商品和未支付订单
        if ("MERCHANT".equals(user.getRole())) {
            try {
                restTemplate.delete(productServiceUrl + "/products/merchant/" + id);
            } catch (Exception e) {
                log.warn("删除商家商品失败: {}", e.getMessage());
            }
            try {
                restTemplate.delete(orderServiceUrl + "/orders/merchant/" + id + "/unpaid");
            } catch (Exception e) {
                log.warn("删除商家未支付订单失败: {}", e.getMessage());
            }
        }
        
        addressRepository.deleteByUserId(id);
        userRepository.deleteById(id);
        log.info("删除用户: userId={}, role={}", id, user.getRole());
    }

    @Override
    public User updateUserByAdmin(Integer id, String username, String phone, String email, String role) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new BusinessException(404, "用户不存在"));
        if (username != null && !username.isBlank()) user.setUsername(username);
        if (phone != null) user.setPhone(phone);
        if (email != null) user.setEmail(email);
        if (role != null && !role.isBlank()) user.setRole(role);
        return userRepository.save(user);
    }

    @Override
    public User updateUserRole(Integer id, String role) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new BusinessException(404, "用户不存在"));
        user.setRole(role);
        return userRepository.save(user);
    }

    @Override
    public void verifyPayPassword(Integer userId, String payPassword) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new BusinessException(404, "用户不存在"));
        if (user.getPayPassword() == null || user.getPayPassword().isBlank()) {
            // 未设置支付密码时直接通过
            return;
        }
        if (!passwordEncoder.matches(payPassword, user.getPayPassword())) {
            throw new BusinessException(400, "支付密码错误");
        }
    }

    // ===== 初始化 =====

    @Override
    public void run(String... args) throws Exception {
        if (!userRepository.findByUsername("admin").isPresent()) {
            User admin = new User();
            admin.setUsername("admin");
            admin.setPassword(passwordEncoder.encode("admin123"));
            admin.setBalance(new BigDecimal("999999.00"));
            admin.setRole("ADMIN");
            userRepository.save(admin);
            log.info("管理员账户初始化成功: username=admin, password=admin123");
        }
    }
}