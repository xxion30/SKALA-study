"""
프로그램명 : 실무형 수집·검증·품질 파이프라인
과목 : 데이터 분석을 위한 Python 이해
실습 : 종합 실습 1

작성자 : 양시온
작성일 : 2026-08-03

실습 목적
- asyncio와 httpx를 활용하여 여러 API를 비동기로 동시에 수집한다.
- Pydantic v2를 이용하여 수집한 데이터를 검증한다.
- 검증된 데이터를 CSV와 Parquet 형식으로 저장하고 성능을 비교한다.
- pytest와 Ruff를 이용하여 코드의 정확성과 품질을 확인한다.
"""

import asyncio

from pydantic import ValidationError

from collector import collect_all
from saver import (
    create_dataframe,
    read_csv,
    read_parquet,
    save_csv,
    save_parquet,
)
from validator import validate_data


async def main():
    try:
        # 1. API 데이터 비동기 수집
        data = await collect_all()

        # 2. 수집 데이터 검증
        weather, country, ip = validate_data(data)

        # 3. 수집된 데이터를 DataFrame으로 변환
        df = create_dataframe(weather, country, ip)

        # 4. CSV와 Parquet 형식으로 저장
        csv_write = save_csv(df)
        parquet_write = save_parquet(df)

        # 5. 저장된 CSV와 Parquet 파일 읽기
        csv_read = read_csv()
        parquet_read = read_parquet()

        # 6. 성능 비교 결과 출력
        print("\n===== 저장 성능 비교 =====")
        print(f"CSV 쓰기 시간      : {csv_write:.6f}초")
        print(f"Parquet 쓰기 시간  : {parquet_write:.6f}초")

        print("\n===== 읽기 성능 비교 =====")
        print(f"CSV 읽기 시간      : {csv_read:.6f}초")
        print(f"Parquet 읽기 시간  : {parquet_read:.6f}초")

    except ValidationError as e:
        print("데이터 검증 실패")
        print(e)


if __name__ == "__main__":
    asyncio.run(main())