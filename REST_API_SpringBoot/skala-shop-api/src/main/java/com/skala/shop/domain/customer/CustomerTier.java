package com.skala.shop.domain.customer;

public enum CustomerTier {

    VIP(70_000),
    GOLD(50_000),
    SILVER(30_000),
    BRONZE(0);

    private final long minOrderAmount;

    CustomerTier(long minOrderAmount) {
        this.minOrderAmount = minOrderAmount;
    }

    public static CustomerTier from(long totalOrderAmount) {
        for (CustomerTier tier : values()) {
            if (totalOrderAmount >= tier.minOrderAmount) {
                return tier;
            }
        }
        return BRONZE;
    }

    public long getMinOrderAmount() {
        return minOrderAmount;
    }
}
