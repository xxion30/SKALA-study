package com.skala.shop.service;

import com.skala.shop.domain.product.Product;
import com.skala.shop.domain.product.ProductRepository;
import com.skala.shop.dto.product.ProductRequest;
import com.skala.shop.dto.product.ProductResponse;
import com.skala.shop.exception.BusinessException;
import com.skala.shop.exception.ErrorCode;
import java.util.List;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional(readOnly = true)
public class ProductService {

    private final ProductRepository productRepository;

    public ProductService(ProductRepository productRepository) {
        // 생성자 주입을 사용하면 Service가 저장소 구현을 직접 만들지 않습니다.
        this.productRepository = productRepository;
    }

    public List<ProductResponse> findAll() {
        return productRepository.findAll().stream()
                .map(ProductResponse::from)
                .toList();
    }

    public ProductResponse findById(Long id) {
        return ProductResponse.from(getProduct(id));
    }

    @Transactional
    public ProductResponse create(ProductRequest request) {
        Product product = new Product(request.name(), request.price());
        return ProductResponse.from(productRepository.save(product));
    }

    @Transactional
    public ProductResponse update(Long id, ProductRequest request) {
        Product product = getProduct(id);
        product.update(request.name(), request.price());
        return ProductResponse.from(product);
    }

    @Transactional
    public void delete(Long id) {
        Product product = getProduct(id);
        productRepository.delete(product);
    }

    private Product getProduct(Long id) {
        return productRepository.findById(id)
                .orElseThrow(() -> new BusinessException(ErrorCode.PRODUCT_NOT_FOUND));
    }
}