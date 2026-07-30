package com.skala.stock.controller;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.skala.stock.dto.AnalysisDto;
import com.skala.stock.dto.PortfolioAnalysisDto;
import com.skala.stock.dto.TransactionDto;
import com.skala.stock.service.AnalysisService;

import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("/api/analysis")
@RequiredArgsConstructor
public class AnalysisController {

    private final AnalysisService analysisService;

    // 사용자의 포트폴리오 평가 손익을 조회
    @GetMapping("/portfolio/{userId}")
    public List<PortfolioAnalysisDto> getPortfolioAnalysis(
            @PathVariable("userId") Long userId) {

        return analysisService.getPortfolioAnalysis(userId);
    }

    // 거래 ID로 거래 상세 정보를 조회
    @GetMapping("/transaction/{id}")
    public TransactionDto getTransaction(
            @PathVariable("id") Long id) {

        return analysisService.getTransaction(id);
    }

    // 사용자의 특정 주식 거래 내역을 조회
    @GetMapping("/transactions/{userId}/{stockId}")
    public List<TransactionDto> getTransactionsByStock(
            @PathVariable("userId") Long userId,
            @PathVariable("stockId") Long stockId) {

        return analysisService.getTransactionsByStock(userId, stockId);
    }

    // 사용자의 총 자산을 조회
    @GetMapping("/asset/{userId}")
    public AnalysisDto getTotalAsset(
            @PathVariable("userId") Long userId) {

        return analysisService.getTotalAsset(userId);
    }

    // 사용자의 총 수익률을 조회
    @GetMapping("/profit/{userId}")
    public AnalysisDto getTotalProfitRate(
            @PathVariable("userId") Long userId) {

        return analysisService.getTotalProfitRate(userId);
    }
}