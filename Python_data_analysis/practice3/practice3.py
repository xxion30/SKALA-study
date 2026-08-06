"""
=========================================================
[Practice 3] Pandas, Polars, DuckDB를 이용한 데이터 분석 비교
파일명 : 판교_2반_양시온.py
작성자 : 양시온
작성일 : 2026-08-04

프로그램 목적
- Pandas, Polars, DuckDB를 이용한 데이터 분석 비교
- sales_100k.csv 데이터를 이용한 EDA
- IQR 방법으로 이상치 제거
- Pandas / Polars / DuckDB 집계 비교
- timeit을 이용한 성능 비교

=========================================================
"""

import timeit
import pandas as pd
import polars as pl
import duckdb


# -------------------------------------------------------
# CSV 로드
# -------------------------------------------------------
try:
    df = pd.read_csv("sales_100k.csv")
    print("CSV 로드 성공")
except FileNotFoundError:
    print("파일을 찾을 수 없습니다.")
    raise
except Exception as e:
    print("오류 발생 :", e)
    raise


# -------------------------------------------------------
# 1. Pandas EDA
# 데이터 구조 및 품질 확인
# -------------------------------------------------------

# info() : 컬럼 정보와 데이터 타입 확인
print("\n===== info() =====")
print(df.info())

# isnull(): 결측치 개수 확인
print("\n===== 결측치 =====")
print(df.isnull().sum())

# describe(): 수치형 데이터의 기초 통계 확인
print("\n===== 기술통계 =====")
print(df.describe())


# -------------------------------------------------------
# IQR 이상치 제거
# -------------------------------------------------------
Q1 = df["amount"].quantile(0.25)
Q3 = df["amount"].quantile(0.75)

IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

print("\nIQR 범위")
print(lower, "~", upper)

# amount 컬럼이 정상 범위에 있는 데이터만 선택
# between()을 이용하여 이상치를 제거한다.

before = len(df)

df_clean = df[df["amount"].between(lower, upper)]

after = len(df_clean)

print(f"\n이상치 제거 전 : {before:,}")
print(f"이상치 제거 후 : {after:,}")


# -------------------------------------------------------
# 2. Pandas groupby (Named Aggregation)
# region, category별 집계 (groupby)
# Named Aggregation 사용
# -------------------------------------------------------
print("\n===== Pandas GroupBy =====")

pandas_result = (
    df_clean
    .groupby(["region", "category"])
    .agg(
        total=("amount", "sum"),        # total : 총매출
        mean=("amount", "mean"),        # mean  : 평균매출
        count=("amount", "count")       # count : 거래건수
    )
    .sort_values("total", ascending=False)
)

print(pandas_result)


# -------------------------------------------------------
# 3. Polars Lazy API
# -------------------------------------------------------
print("\n===== Polars Lazy =====")

polars_result = (
    # scan_csv() : LazyFrame 생성
    pl.scan_csv("sales_100k.csv")
    .filter(    # filter()   : 이상치 제거
        pl.col("amount").is_between(lower, upper)
    )
    .group_by(["region", "category"])       # group_by() : 그룹 집계
    .agg(             # agg(): 총합, 평균, 건수 계산
        [
            pl.col("amount").sum().alias("total"),
            pl.col("amount").mean().alias("mean"),
            pl.col("amount").count().alias("count")
        ]
    )
    
    .sort("total", descending=True)     # sort()     : 총매출 기준 정렬

    .collect()                  # collect()  : 실제 연산 수행
)

print(polars_result)


# -------------------------------------------------------
# 4. DuckDB SQL
# GROUP BY를 사용하여 Pandas와 동일한 결과 생성
# -------------------------------------------------------
print("\n===== DuckDB =====")

con = duckdb.connect()

duck_result = con.execute(f"""
SELECT
    region,
    category,
    SUM(amount) AS total,
    AVG(amount) AS mean,
    COUNT(amount) AS count
FROM read_csv_auto('sales_100k.csv')
WHERE amount BETWEEN {lower} AND {upper}
GROUP BY region, category
ORDER BY total DESC
""").df()

print(duck_result)


# -------------------------------------------------------
# 성능 비교 함수
# -------------------------------------------------------
def pandas_test():

    df = pd.read_csv("sales_100k.csv")

    q1 = df["amount"].quantile(0.25)
    q3 = df["amount"].quantile(0.75)
    iqr = q3 - q1

    low = q1 - 1.5 * iqr
    high = q3 + 1.5 * iqr

    (
        df[df["amount"].between(low, high)]
        .groupby(["region", "category"])
        .agg(
            total=("amount", "sum"),
            mean=("amount", "mean"),
            count=("amount", "count")
        )
        .sort_values("total", ascending=False)
    )


def polars_test():

    (
        pl.scan_csv("sales_100k.csv")
        .filter(pl.col("amount").is_between(lower, upper))
        .group_by(["region", "category"])
        .agg(
            [
                pl.col("amount").sum().alias("total"),
                pl.col("amount").mean().alias("mean"),
                pl.col("amount").count().alias("count")
            ]
        )
        .sort("total", descending=True)
        .collect()
    )


def duckdb_test():

    duckdb.sql(f"""
    SELECT
        region,
        category,
        SUM(amount) AS total,
        AVG(amount) AS mean,
        COUNT(amount) AS count
    FROM read_csv_auto('sales_100k.csv')
    WHERE amount BETWEEN {lower} AND {upper}
    GROUP BY region, category
    ORDER BY total DESC
    """).df()


# -------------------------------------------------------
# timeit (동일 반복 횟수)
# 실행 시간 비교
# number 값을 동일하게 설정하여 공정한 성능 비교를 수행한다.
# -------------------------------------------------------
repeat = 10

pandas_time = timeit.timeit(pandas_test, number=repeat)
polars_time = timeit.timeit(polars_test, number=repeat)
duck_time = timeit.timeit(duckdb_test, number=repeat)

print("\n===== 실행 시간 비교 =====")
print(f"Pandas : {pandas_time:.4f} sec")
print(f"Polars : {polars_time:.4f} sec")
print(f"DuckDB : {duck_time:.4f} sec")