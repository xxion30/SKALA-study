package com.skala.shop.domain.customer;

import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

public interface CustomerRepository extends JpaRepository<Customer, Long> {

    Optional<Customer> findByCustomerId(String customerId);

    Optional<Customer> findByName(String name);

    boolean existsByCustomerId(String customerId);

    boolean existsByName(String name);
}