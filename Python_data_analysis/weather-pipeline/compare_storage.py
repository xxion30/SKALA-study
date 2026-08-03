"""
프로그램명 : CSV · Parquet 성능 비교
과목 : 데이터 분석을 위한 Python 이해
실습 : 종합 실습 1

작성자 : 양시온
작성일 : 2026-08-03

파일 설명
- 데이터 크기(행 수)에 따른 CSV와 Parquet 파일의 성능을 비교한다.
- 저장 및 읽기 시간을 측정하고 파일 크기를 비교한다.
- 데이터 저장 형식에 따른 성능 차이를 분석하기 위한 실험 코드이다.
"""

import time, os
import pandas as pd
import numpy as np

sizes = [100, 1_000, 10_000, 100_000, 1_000_000]
df_full = pd.read_csv("synthetic_sales.csv")

results = []
for n in sizes:
    df = df_full.sample(n=n, random_state=42) if n < len(df_full) else df_full

    csv_path, parquet_path = f"tmp_{n}.csv", f"tmp_{n}.parquet"

    t0 = time.perf_counter(); df.to_csv(csv_path, index=False); t_csv_write = time.perf_counter() - t0
    t0 = time.perf_counter(); df.to_parquet(parquet_path); t_parquet_write = time.perf_counter() - t0

    t0 = time.perf_counter(); pd.read_csv(csv_path); t_csv_read = time.perf_counter() - t0
    t0 = time.perf_counter(); pd.read_parquet(parquet_path); t_parquet_read = time.perf_counter() - t0

    results.append({
        "rows": n,
        "csv_size_kb": os.path.getsize(csv_path) / 1024,
        "parquet_size_kb": os.path.getsize(parquet_path) / 1024,
        "csv_write_s": t_csv_write, "parquet_write_s": t_parquet_write,
        "csv_read_s": t_csv_read, "parquet_read_s": t_parquet_read,
    })

pd.DataFrame(results)