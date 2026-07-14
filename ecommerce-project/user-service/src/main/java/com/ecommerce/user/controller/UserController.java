package com.ecommerce.user.controller;

import com.ecommerce.common.AdminRequired;
import com.ecommerce.common.ApiResponse;
import com.ecommerce.common.InternalApi;
import com.ecommerce.user.dto.*;
import com.ecommerce.user.entity.Address;
import com.ecommerce.user.entity.User;
import com.ecommerce.user.service.UserService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.math.BigDecimal;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/users")
public class UserController {

    @Autowired
    private UserService userService;

    @PostMapping("/register")
    public ResponseEntity<ApiResponse<RegisterResponse>> register(@Valid @RequestBody UserRequest request) {
        RegisterResponse response = userService.register(
                request.username(), request.password(), request.role(),
                request.payPassword(), request.phone(), request.email());
        return ResponseEntity.ok(ApiResponse.success(response));
    }

    @PostMapping("/login")
    public ResponseEntity<ApiResponse<LoginResponse>> login(@Valid @RequestBody UserRequest request) {
        LoginResponse response = userService.login(request.username(), request.password());
        return ResponseEntity.ok(ApiResponse.success(response));
    }

    @PutMapping("/{userId}/deduct-balance")
    @InternalApi
    public ResponseEntity<ApiResponse<Void>> deductBalance(
            @PathVariable Integer userId,
            @RequestParam BigDecimal amount) {
        userService.deductBalance(userId, amount);
        return ResponseEntity.ok(ApiResponse.success("余额扣减成功"));
    }

    @PutMapping("/{userId}/add-balance")
    @InternalApi
    public ResponseEntity<ApiResponse<Void>> addBalance(
            @PathVariable Integer userId,
            @RequestParam BigDecimal amount) {
        userService.addBalance(userId, amount);
        return ResponseEntity.ok(ApiResponse.success("余额增加成功"));
    }

    // 管理员查看所有用户
    @GetMapping("/admin/users")
    @AdminRequired
    public ResponseEntity<ApiResponse<List<User>>> getAllUsers() {
        List<User> users = userService.getAllUsers();
        return ResponseEntity.ok(ApiResponse.success(users));
    }

    // 查询用户信息
    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse<User>> getUser(@PathVariable Integer id) {
        User user = userService.getUserById(id);
        return ResponseEntity.ok(ApiResponse.success(user));
    }

    // 获取用户资料
    @GetMapping("/{id}/profile")
    public ResponseEntity<ApiResponse<User>> getProfile(@PathVariable Integer id) {
        User user = userService.getProfile(id);
        return ResponseEntity.ok(ApiResponse.success(user));
    }

    // 修改用户资料
    @PutMapping("/{id}/profile")
    public ResponseEntity<ApiResponse<User>> updateProfile(
            @PathVariable Integer id,
            @RequestBody ProfileRequest request) {
        User user = userService.updateProfile(id, request.username(), request.phone(), request.email());
        return ResponseEntity.ok(ApiResponse.success(user));
    }

    // 修改登录密码
    @PutMapping("/{id}/password")
    public ResponseEntity<ApiResponse<Void>> changePassword(
            @PathVariable Integer id,
            @RequestBody PasswordRequest request) {
        userService.changePassword(id, request.oldPassword(), request.newPassword());
        return ResponseEntity.ok(ApiResponse.success("密码修改成功"));
    }

    // 修改支付密码
    @PutMapping("/{id}/pay-password")
    public ResponseEntity<ApiResponse<Void>> changePayPassword(
            @PathVariable Integer id,
            @RequestBody PayPasswordRequest request) {
        userService.changePayPassword(id, request.oldPayPassword(), request.newPayPassword());
        return ResponseEntity.ok(ApiResponse.success("支付密码修改成功"));
    }

    // 重置密码
    @PostMapping("/{id}/reset-password")
    public ResponseEntity<ApiResponse<Void>> resetPassword(
            @PathVariable Integer id,
            @RequestBody ResetPasswordRequest request) {
        userService.resetPassword(id, request.type(), request.newPassword());
        return ResponseEntity.ok(ApiResponse.success("密码重置成功"));
    }

    // 上传头像
    @PostMapping("/{id}/avatar")
    public ResponseEntity<ApiResponse<Map<String, String>>> uploadAvatar(
            @PathVariable Integer id,
            @RequestParam("file") MultipartFile file) {
        try {
            String avatarUrl = userService.uploadAvatar(id, file.getBytes(), file.getOriginalFilename(), file.getContentType());
            return ResponseEntity.ok(ApiResponse.success(Map.of("avatarUrl", avatarUrl)));
        } catch (Exception e) {
            return ResponseEntity.internalServerError().build();
        }
    }

    // 从 MinIO 获取文件（头像等）
    @GetMapping("/files/{filename}")
    public ResponseEntity<byte[]> getFile(@PathVariable String filename) {
        byte[] data = userService.getFile(filename);
        String contentType = "image/jpeg";
        if (filename.endsWith(".png")) contentType = "image/png";
        else if (filename.endsWith(".gif")) contentType = "image/gif";
        else if (filename.endsWith(".webp")) contentType = "image/webp";
        return ResponseEntity.ok()
                .header(HttpHeaders.CONTENT_TYPE, contentType)
                .header(HttpHeaders.CACHE_CONTROL, "public, max-age=31536000")
                .body(data);
    }

    // ===== 收货地址管理 =====

    @GetMapping("/{id}/addresses")
    public ResponseEntity<ApiResponse<List<Address>>> getAddresses(@PathVariable Integer id) {
        List<Address> addresses = userService.getAddresses(id);
        return ResponseEntity.ok(ApiResponse.success(addresses));
    }

    @PostMapping("/{id}/addresses")
    public ResponseEntity<ApiResponse<Address>> addAddress(
            @PathVariable Integer id,
            @RequestBody AddressRequest request) {
        Address address = new Address();
        address.setReceiverName(request.receiverName());
        address.setPhone(request.phone());
        address.setProvince(request.province());
        address.setCity(request.city());
        address.setDistrict(request.district());
        address.setDetailAddress(request.detailAddress());
        address.setIsDefault(request.isDefault());
        Address saved = userService.addAddress(id, address);
        return ResponseEntity.ok(ApiResponse.success(saved));
    }

    @PutMapping("/{id}/addresses/{addressId}")
    public ResponseEntity<ApiResponse<Address>> updateAddress(
            @PathVariable Integer id,
            @PathVariable Integer addressId,
            @RequestBody AddressRequest request) {
        Address updates = new Address();
        updates.setReceiverName(request.receiverName());
        updates.setPhone(request.phone());
        updates.setProvince(request.province());
        updates.setCity(request.city());
        updates.setDistrict(request.district());
        updates.setDetailAddress(request.detailAddress());
        updates.setIsDefault(request.isDefault());
        Address saved = userService.updateAddress(id, addressId, updates);
        return ResponseEntity.ok(ApiResponse.success(saved));
    }

    @DeleteMapping("/{id}/addresses/{addressId}")
    public ResponseEntity<ApiResponse<Void>> deleteAddress(
            @PathVariable Integer id,
            @PathVariable Integer addressId) {
        userService.deleteAddress(id, addressId);
        return ResponseEntity.ok(ApiResponse.success("地址删除成功"));
    }

    @PutMapping("/{id}/addresses/{addressId}/default")
    public ResponseEntity<ApiResponse<Address>> setDefaultAddress(
            @PathVariable Integer id,
            @PathVariable Integer addressId) {
        Address address = userService.setDefaultAddress(id, addressId);
        return ResponseEntity.ok(ApiResponse.success(address));
    }

    // 用户注销
    @DeleteMapping("/{id}/self")
    public ResponseEntity<ApiResponse<Void>> deleteSelf(@PathVariable Integer id) {
        userService.deleteUser(id);
        return ResponseEntity.ok(ApiResponse.success("账户注销成功"));
    }

    // ===== 管理员操作 =====

    @PutMapping("/{id}")
    @AdminRequired
    public ResponseEntity<ApiResponse<User>> updateUserByAdmin(
            @PathVariable Integer id,
            @RequestBody Map<String, String> body) {
        User user = userService.updateUserByAdmin(id,
                body.get("username"), body.get("phone"), body.get("email"), body.get("role"));
        return ResponseEntity.ok(ApiResponse.success(user));
    }

    @PutMapping("/{id}/role")
    @AdminRequired
    public ResponseEntity<ApiResponse<User>> updateUserRole(
            @PathVariable Integer id,
            @RequestBody Map<String, String> body) {
        User user = userService.updateUserRole(id, body.get("role"));
        return ResponseEntity.ok(ApiResponse.success(user));
    }

    @DeleteMapping("/{id}")
    @AdminRequired
    public ResponseEntity<ApiResponse<Void>> deleteUserByAdmin(@PathVariable Integer id) {
        userService.deleteUser(id);
        return ResponseEntity.ok(ApiResponse.success("用户删除成功"));
    }

    // 验证支付密码（内部服务调用）
    @PostMapping("/{id}/verify-pay-password")
    @InternalApi
    public ResponseEntity<ApiResponse<Void>> verifyPayPassword(
            @PathVariable Integer id,
            @RequestBody Map<String, String> body) {
        userService.verifyPayPassword(id, body.get("payPassword"));
        return ResponseEntity.ok(ApiResponse.success("支付密码验证成功"));
    }
}