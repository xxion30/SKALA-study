package com.skala.shop.dto.customer;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record CustomerUpdateRequest(
        @NotBlank(message = "새 비밀번호는 필수입니다.")
        @Size(min = 8, max = 30, message = "비밀번호는 8자 이상 30자 이하여야 합니다.")
        String newPassword
) {
}
