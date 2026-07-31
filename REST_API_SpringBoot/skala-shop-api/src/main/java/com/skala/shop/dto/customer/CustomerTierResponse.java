package com.skala.shop.dto.customer;

import com.skala.shop.domain.customer.CustomerTier;

public record CustomerTierResponse(
        String customerId,
        long totalOrderAmount,
        CustomerTier tier
) {
}
