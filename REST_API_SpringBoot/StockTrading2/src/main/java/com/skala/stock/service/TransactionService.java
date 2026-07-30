package com.skala.stock.service;

import com.skala.stock.dto.TransactionDto;
import com.skala.stock.entity.Stock;
import com.skala.stock.entity.Transaction;
import com.skala.stock.entity.User;
import com.skala.stock.repository.TransactionRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

import com.skala.stock.repository.UserRepository;
import com.skala.stock.repository.StockRepository;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class TransactionService {

    private final TransactionRepository transactionRepository;
    private final UserRepository userRepository;
    private final StockRepository stockRepository;

    @Transactional(readOnly = true, propagation = Propagation.SUPPORTS)
    public List<TransactionDto> getUserTransactions(Long userId) {
        List<Transaction> transactions = transactionRepository.findByUserIdOrderByTransactionDateDesc(userId);
        return transactions.stream()
                .map(this::convertToDto)
                .collect(Collectors.toList());
    }

    private TransactionDto convertToDto(Transaction transaction) {
        return TransactionDto.builder()
                .id(transaction.getId())
                .userId(transaction.getUser().getId())
                .username(transaction.getUser().getUsername())
                .stockId(transaction.getStock().getId())
                .stockCode(transaction.getStock().getCode())
                .stockName(transaction.getStock().getName())
                .type(transaction.getType())
                .quantity(transaction.getQuantity())
                .price(transaction.getPrice())
                .totalAmount(transaction.getTotalAmount())
                .transactionDate(transaction.getTransactionDate())
                .createdAt(transaction.getCreatedAt())
                .build();
    }

    // Get by ID(Read Only)
    public TransactionDto getTransactionById(Long id) {

        Transaction transaction = transactionRepository.findTransactionById(id)
                .orElseThrow(() -> new RuntimeException("거래 내역을 찾을 수 없습니다: " + id));

        return convertToDto(transaction);
    }

    // POST/trade
    @Transactional
    public TransactionDto trade(TransactionDto transactionDto) {

        User user = userRepository.findById(transactionDto.getUserId())
                .orElseThrow(() ->
                        new RuntimeException("사용자를 찾을 수 없습니다: " + transactionDto.getUserId()));

        Stock stock = stockRepository.findById(transactionDto.getStockId())
                .orElseThrow(() ->
                        new RuntimeException("주식을 찾을 수 없습니다: " + transactionDto.getStockId()));

        Long totalAmount = transactionDto.getQuantity() * transactionDto.getPrice();

        // 매수(BUY)
        if (transactionDto.getType() == Transaction.TransactionType.BUY) {

            if (user.getBalance() < totalAmount) {
                throw new RuntimeException("잔액이 부족합니다.");
            }

            user.setBalance(user.getBalance() - totalAmount);
        }

        // 매도(SELL)
        else if (transactionDto.getType() == Transaction.TransactionType.SELL) {

            user.setBalance(user.getBalance() + totalAmount);
        }

        Transaction transaction = Transaction.builder()
                .user(user)
                .stock(stock)
                .type(transactionDto.getType())
                .quantity(transactionDto.getQuantity())
                .price(transactionDto.getPrice())
                .totalAmount(totalAmount)
                .build();

        Transaction savedTransaction = transactionRepository.save(transaction);

        return convertToDto(savedTransaction);
    }
}
