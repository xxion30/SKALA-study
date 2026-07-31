package com.skala.shop.dto.customer;

public record SignUpResponse(String customerId, String name, long initialPoint, String message) {
}