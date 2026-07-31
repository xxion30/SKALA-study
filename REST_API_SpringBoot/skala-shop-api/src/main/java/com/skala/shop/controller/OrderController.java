package com.skala.shop.controller;

import com.skala.shop.dto.order.CustomerOrderResponse;
import com.skala.shop.dto.order.OrderRequest;
import com.skala.shop.dto.order.OrderResultResponse;
import com.skala.shop.service.OrderService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import io.swagger.v3.oas.annotations.Operation;

@RestController
@RequestMapping("/api/customers")
public class OrderController {

    private final OrderService orderService;

    public OrderController(OrderService orderService) {
        this.orderService = orderService;
    }

    @Operation(summary = "내 주문 조회", description = "현재 로그인한 고객의 주문 내역을 조회합니다.")
    @GetMapping("/me")
    public ResponseEntity<CustomerOrderResponse> findMyOrders(Authentication authentication) {
        return ResponseEntity.ok(orderService.findMyOrders(authentication.getName()));
    }

    @Operation(summary = "상품 주문", description = "현재 로그인한 고객이 상품을 주문합니다.")
    @PostMapping("/order")
    public ResponseEntity<OrderResultResponse> placeOrder(
            Authentication authentication,
            @Valid @RequestBody OrderRequest request
    ) {
        return ResponseEntity.ok(
                orderService.placeOrder(authentication.getName(), request)
        );
    }
    
    @Operation(summary = "주문 취소", description = "현재 로그인한 고객의 주문을 취소합니다.")
    @PostMapping("/cancel")
    public ResponseEntity<OrderResultResponse> cancelOrder(
            Authentication authentication,
            @Valid @RequestBody OrderRequest request
    ) {
        return ResponseEntity.ok(
                orderService.cancelOrder(authentication.getName(), request)
        );
    }
}