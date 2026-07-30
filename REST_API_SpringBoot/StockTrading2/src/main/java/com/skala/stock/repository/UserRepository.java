package com.skala.stock.repository;

import com.skala.stock.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByUsername(String username);
    Optional<User> findByEmail(String email);
    boolean existsByUsername(String username);
    boolean existsByEmail(String email);

    // 전체 조회
    @Query ("SELECT u FROM User u")
    List<User> getAllUsers();

    // 삭제
    @Modifying
    @Query("DELETE FROM User u WHERE u.id = :id")
    void deleteUserById(@Param("id") Long id);

    // 사용자 ID로 사용자 정보를 조회
    @Query("""
        SELECT u
        FROM User u
        WHERE u.id = :id
        """)
    Optional<User> findUserById(
            @Param("id") Long id);
}
