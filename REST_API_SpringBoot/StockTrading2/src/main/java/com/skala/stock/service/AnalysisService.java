package com.skala.stock.service;

import java.util.List;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.skala.stock.dto.AnalysisDto;
import com.skala.stock.dto.PortfolioAnalysisDto;
import com.skala.stock.dto.TransactionDto;
import com.skala.stock.entity.Portfolio;
import com.skala.stock.entity.Transaction;
import com.skala.stock.entity.User;
import com.skala.stock.repository.PortfolioRepository;
import com.skala.stock.repository.TransactionRepository;
import com.skala.stock.repository.UserRepository;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class AnalysisService {

    private final UserRepository userRepository;
    private final PortfolioRepository portfolioRepository;
    private final TransactionRepository transactionRepository;

    // 사용자의 포트폴리오 평가 손익을 조회
    public List<PortfolioAnalysisDto> getPortfolioAnalysis(Long userId) {

        List<Portfolio> portfolios =
                portfolioRepository.findPortfolioByUserId(userId);

        return portfolios.stream()
                .map(portfolio -> {

                    Long purchaseAmount =
                            portfolio.getAveragePrice()
                                    * portfolio.getQuantity();

                    Long evaluationAmount =
                            portfolio.getStock().getCurrentPrice()
                                    * portfolio.getQuantity();

                    Long profit =
                            evaluationAmount - purchaseAmount;

                    Double profitRate =
                            purchaseAmount == 0
                                    ? 0.0
                                    : (double) profit / purchaseAmount * 100;

                    return PortfolioAnalysisDto.builder()
                            .stockCode(portfolio.getStock().getCode())
                            .stockName(portfolio.getStock().getName())
                            .quantity(portfolio.getQuantity())
                            .averagePrice(portfolio.getAveragePrice())
                            .currentPrice(portfolio.getStock().getCurrentPrice())
                            .purchaseAmount(purchaseAmount)
                            .evaluationAmount(evaluationAmount)
                            .profit(profit)
                            .profitRate(profitRate)
                            .build();
                })
                .toList();
    }

    // 거래 ID로 거래 상세 정보를 조회
    public TransactionDto getTransaction(Long id) {

        Transaction transaction = transactionRepository.findTransactionById(id)
                .orElseThrow(() -> new RuntimeException("거래 내역을 찾을 수 없습니다."));

        return convertToDto(transaction);
    }

    // 사용자의 특정 주식 거래 내역을 조회
    public List<TransactionDto> getTransactionsByStock(Long userId, Long stockId) {

        return transactionRepository
                .findTransactionsByUserAndStock(userId, stockId)
                .stream()
                .map(this::convertToDto)
                .toList();
    }

    // 사용자의 총 자산을 조회
    public AnalysisDto getTotalAsset(Long userId) {

        User user = userRepository.findUserById(userId)
                .orElseThrow(() -> new RuntimeException("사용자를 찾을 수 없습니다."));

        List<Portfolio> portfolios =
                portfolioRepository.findPortfolioByUserId(userId);

        Long stockAsset = 0L;

        for (Portfolio portfolio : portfolios) {

            stockAsset += portfolio.getStock().getCurrentPrice()
                    * portfolio.getQuantity();
        }

        return AnalysisDto.builder()
                .balance(user.getBalance())
                .stockAsset(stockAsset)
                .totalAsset(user.getBalance() + stockAsset)
                .build();
    }

    // 사용자의 총 수익률을 조회
    public AnalysisDto getTotalProfitRate(Long userId) {

        List<Portfolio> portfolios =
                portfolioRepository.findPortfolioByUserId(userId);

        Long purchaseAmount = 0L;
        Long evaluationAmount = 0L;

        for (Portfolio portfolio : portfolios) {

            purchaseAmount +=
                    portfolio.getAveragePrice()
                            * portfolio.getQuantity();

            evaluationAmount +=
                    portfolio.getStock().getCurrentPrice()
                            * portfolio.getQuantity();
        }

        Long profit = evaluationAmount - purchaseAmount;

        Double profitRate =
                purchaseAmount == 0
                        ? 0.0
                        : (double) profit / purchaseAmount * 100;

        return AnalysisDto.builder()
                .purchaseAmount(purchaseAmount)
                .evaluationAmount(evaluationAmount)
                .profit(profit)
                .profitRate(profitRate)
                .build();
    }

    // Transaction 엔티티를 DTO로 변환
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

}