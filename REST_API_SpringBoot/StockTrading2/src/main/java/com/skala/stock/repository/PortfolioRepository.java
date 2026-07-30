package com.skala.stock.repository;

import com.skala.stock.entity.Portfolio;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface PortfolioRepository extends JpaRepository<Portfolio, Long> {
    List<Portfolio> findByUserId(Long userId);
    Optional<Portfolio> findByUserIdAndStockId(Long userId, Long stockId);
    boolean existsByUserIdAndStockId(Long userId, Long stockId);


    @Query("""
        SELECT p
        FROM Portfolio p
        WHERE p.user.id = :userId
        AND p.stock.id = :stockId
        """)
    Optional<Portfolio> findPortfolioByUserIdAndStockId(
            @Param("userId") Long userId,
            @Param("stockId") Long stockId);

    // 사용자의 전체 보유 주식 정보를 조회
    @Query("""
        SELECT p
        FROM Portfolio p
        WHERE p.user.id = :userId
        """)
    List<Portfolio> findPortfolioByUserId(
            @Param("userId") Long userId);

}


