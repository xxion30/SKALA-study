package com.skala.stock.repository;

import com.skala.stock.entity.Transaction;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface TransactionRepository extends JpaRepository<Transaction, Long> {
    
    // 거래 ID로 거래 상세 정보를 조회
    @Query("""
        SELECT t
        FROM Transaction t
        WHERE t.id = :id
        """)

    Optional<Transaction> findTransactionById(@Param("id") Long id);

    List<Transaction> findByUserIdOrderByTransactionDateDesc(Long userId);

    List<Transaction> findByUserIdAndStockIdOrderByTransactionDateDesc(Long userId, Long stockId);

    
    // 사용자의 특정 주식 거래 내역을 최신순으로 조회
    @Query("""
        SELECT t
        FROM Transaction t
        WHERE t.user.id = :userId
        AND t.stock.id = :stockId
        ORDER BY t.transactionDate DESC
        """)
    List<Transaction> findTransactionsByUserAndStock(
            @Param("userId") Long userId,
            @Param("stockId") Long stockId);
}