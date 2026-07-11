package com.ecommerce.user.service;

import com.ecommerce.user.dto.LoginResponse;
import com.ecommerce.user.dto.RegisterResponse;
import com.ecommerce.user.entity.Address;
import com.ecommerce.user.entity.User;
import java.math.BigDecimal;
import java.util.List;

public interface UserService {
    RegisterResponse register(String username, String password, String role, String payPassword, String phone, String email);
    LoginResponse login(String username, String password);
    void deductBalance(Integer userId, BigDecimal amount);
    List<User> getAllUsers();

    User getUserById(Integer id);
    User updateProfile(Integer id, String username, String phone, String email);
    User getProfile(Integer id);
    void changePassword(Integer id, String oldPassword, String newPassword);
    void changePayPassword(Integer id, String oldPayPassword, String newPayPassword);
    void resetPassword(Integer id, String type, String newPassword);
    String uploadAvatar(Integer id, byte[] fileData, String originalFilename);

    List<Address> getAddresses(Integer userId);
    Address addAddress(Integer userId, Address address);
    Address updateAddress(Integer userId, Integer addressId, Address address);
    void deleteAddress(Integer userId, Integer addressId);
    Address setDefaultAddress(Integer userId, Integer addressId);

    void deleteUser(Integer id);
    User updateUserByAdmin(Integer id, String username, String phone, String email, String role);
    User updateUserRole(Integer id, String role);
    void verifyPayPassword(Integer userId, String payPassword);
}