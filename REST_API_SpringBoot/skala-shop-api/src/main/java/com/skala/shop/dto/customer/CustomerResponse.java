package com.skala.shop.dto.customer;

import com.skala.shop.domain.customer.Customer;

public record CustomerResponse(
        Long id,
        String customerId,
        String name,
        long point
) {

    public static CustomerResponse from(Customer customer) {
        return new CustomerResponse(
                customer.getId(),
                customer.getCustomerId(),
                customer.getName(),
                customer.getPoint()
        );
    }
}
