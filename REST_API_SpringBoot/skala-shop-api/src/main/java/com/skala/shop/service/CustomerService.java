package com.skala.shop.service;

import com.skala.shop.domain.customer.Customer;
import com.skala.shop.domain.customer.CustomerRepository;
import com.skala.shop.domain.customer.CustomerTier;
import com.skala.shop.domain.order.OrderItemRepository;
import com.skala.shop.dto.customer.CustomerResponse;
import com.skala.shop.dto.customer.CustomerTierResponse;
import com.skala.shop.dto.customer.CustomerUpdateRequest;
import com.skala.shop.exception.BusinessException;
import com.skala.shop.exception.ErrorCode;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional(readOnly = true)
public class CustomerService {

    private final CustomerRepository customerRepository;
    private final OrderItemRepository orderItemRepository;
    private final PasswordEncoder passwordEncoder;

    public CustomerService(
            CustomerRepository customerRepository,
            OrderItemRepository orderItemRepository,
            PasswordEncoder passwordEncoder
    ) {
        this.customerRepository = customerRepository;
        this.orderItemRepository = orderItemRepository;
        this.passwordEncoder = passwordEncoder;
    }

    public CustomerResponse findById(Long id) {
        Customer customer = customerRepository.findById(id)
                .orElseThrow(() -> new BusinessException(ErrorCode.CUSTOMER_NOT_FOUND));
        return CustomerResponse.from(customer);
    }

    public CustomerResponse findByName(String name) {
        Customer customer = customerRepository.findByName(name)
                .orElseThrow(() -> new BusinessException(ErrorCode.CUSTOMER_NOT_FOUND));
        return CustomerResponse.from(customer);
    }

    @Transactional
    public CustomerResponse updateMyInfo(String customerId, CustomerUpdateRequest request) {
        Customer customer = getCustomer(customerId);
        customer.changePassword(passwordEncoder.encode(request.newPassword()));
        return CustomerResponse.from(customer);
    }

    @Transactional
    public void deleteById(Long id) {
        if (!customerRepository.existsById(id)) {
            throw new BusinessException(ErrorCode.CUSTOMER_NOT_FOUND);
        }
        customerRepository.deleteById(id);
    }

    public CustomerTierResponse getMyTier(String customerId) {
        Customer customer = getCustomer(customerId);

        long totalOrderAmount = orderItemRepository.findAllByCustomer(customer).stream()
                .mapToLong(orderItem -> Math.multiplyExact(
                        orderItem.getProduct().getPrice(),
                        (long) orderItem.getQuantity()
                ))
                .sum();

        CustomerTier tier = CustomerTier.from(totalOrderAmount);
        return new CustomerTierResponse(customer.getCustomerId(), totalOrderAmount, tier);
    }

    private Customer getCustomer(String customerId) {
        return customerRepository.findByCustomerId(customerId)
                .orElseThrow(() -> new BusinessException(ErrorCode.CUSTOMER_NOT_FOUND));
    }
}
