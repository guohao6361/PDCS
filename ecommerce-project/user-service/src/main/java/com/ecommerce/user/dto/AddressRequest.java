package com.ecommerce.user.dto;

public record AddressRequest(
        String receiverName,
        String phone,
        String province,
        String city,
        String district,
        String detailAddress,
        Boolean isDefault
) {}
