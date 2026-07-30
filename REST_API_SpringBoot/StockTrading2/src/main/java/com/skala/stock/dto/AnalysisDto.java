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
public class AnalysisDto {

    // 보유 현금
    private Long balance;

    // 보유 주식 평가금액
    private Long stockAsset;

    // 총 자산
    private Long totalAsset;

    // 총 매입금액
    private Long purchaseAmount;

    // 총 평가금액
    private Long evaluationAmount;

    // 평가 손익
    private Long profit;

    // 총 수익률(%)
    private Double profitRate;

}