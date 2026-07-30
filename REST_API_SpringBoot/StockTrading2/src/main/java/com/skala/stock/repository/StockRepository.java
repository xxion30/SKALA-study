package com.skala.stock.repository;

import com.skala.stock.entity.Stock;

import jakarta.transaction.Transactional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface StockRepository extends JpaRepository<Stock, Long> {
    // 코드 조회 (-> Stock GET by Code)
    //Optional<Stock> findByCode(String code); (이 코드 수정)
    @Query("SELECT s FROM Stock s WHERE s.code = :code")
    Optional<Stock> findStockByCode(@Param("code") String code);

    //코드 존재 여부
    boolean existsByCode(String code);
    
    //Stock DELETE
    @Modifying
    @Transactional
    @Query("DELETE FROM Stock s WHERE s.id = :id")
    void deleteStockById(@Param("id") Long id);

    //Stock UPDATE (-> Stock PUT)
    @Modifying
    @Transactional
    @Query("""
    UPDATE Stock s
    SET
        s.name = :name,
        s.currentPrice = :currentPrice,
        s.previousPrice = :previousPrice
    WHERE s.id = :id
    """)
    int updateStock(
        @Param("id") Long id,
        @Param("name") String name,
        @Param("currentPrice") Long currentPrice,
        @Param("previousPrice") Long previousPrice
    );
    


}
