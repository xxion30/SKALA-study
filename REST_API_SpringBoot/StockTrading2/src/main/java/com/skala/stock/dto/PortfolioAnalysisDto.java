package com.skala.stock.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class PortfolioAnalysisDto {

    // 주식 코드
    private String stockCode;

    // 주식 이름
    private String stockName;

    // 보유 수량
    private Long quantity;

    // 평균 매수가
    private Long averagePrice;

    // 현재가
    private Long currentPrice;

    // 총 매입금액
    private Long purchaseAmount;

    // 총 평가금액
    private Long evaluationAmount;

    // 평가 손익
    private Long profit;

    // 수익률(%)
    private Double profitRate;

}