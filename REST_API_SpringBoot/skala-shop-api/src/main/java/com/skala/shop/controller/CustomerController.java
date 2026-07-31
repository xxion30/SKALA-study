package com.skala.shop.controller;

import com.skala.shop.dto.customer.CustomerResponse;
import com.skala.shop.dto.customer.CustomerTierResponse;
import com.skala.shop.dto.customer.CustomerUpdateRequest;
import com.skala.shop.service.CustomerService;
import io.swagger.v3.oas.annotations.Operation;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/customers")
public class CustomerController {

    private final CustomerService customerService;

    public CustomerController(CustomerService customerService) {
        this.customerService = customerService;
    }

    @Operation(summary = "고객 등급 조회", description = "현재 로그인한 고객의 누적 주문 금액에 따른 등급을 조회합니다.")
    @GetMapping("/me/tier")
    public ResponseEntity<CustomerTierResponse> getMyTier(Authentication authentication) {
        return ResponseEntity.ok(customerService.getMyTier(authentication.getName()));
    }

    // id는 숫자(예: 1, 2, 3 ...)로만 구성된 고객 PK를 의미합니다.
    @Operation(summary = "고객 단건 조회 (ID)", description = "고객 ID(PK)에 해당하는 고객 상세 정보를 조회합니다.")
    @GetMapping("/{id:\\d+}")
    public ResponseEntity<CustomerResponse> findById(@PathVariable Long id) {
        return ResponseEntity.ok(customerService.findById(id));
    }

    // name은 숫자가 아닌 문자로 구성된 고객 이름을 의미합니다.
    @Operation(summary = "고객 단건 조회 (이름)", description = "이름에 해당하는 고객 상세 정보를 조회합니다.")
    @GetMapping("/{name:\\D+}")
    public ResponseEntity<CustomerResponse> findByName(@PathVariable String name) {
        return ResponseEntity.ok(customerService.findByName(name));
    }

    @Operation(summary = "고객 정보 변경", description = "현재 로그인한 고객의 비밀번호를 변경합니다.")
    @PutMapping
    public ResponseEntity<CustomerResponse> updateMyInfo(
            Authentication authentication,
            @Valid @RequestBody CustomerUpdateRequest request
    ) {
        return ResponseEntity.ok(customerService.updateMyInfo(authentication.getName(), request));
    }

    @Operation(summary = "고객 정보 삭제", description = "고객 ID(PK)에 해당하는 고객 정보를 삭제합니다.")
    @DeleteMapping("/{id:\\d+}")
    public ResponseEntity<Void> deleteById(@PathVariable Long id) {
        customerService.deleteById(id);
        return ResponseEntity.noContent().build();
    }
}
