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
        # 1. API 수집
        data = await collect_all()

        # 2. 데이터 검증
        weather, country, ip = validate_data(data)

        # 3. DataFrame 생성
        df = create_dataframe(weather, country, ip)

        # 4. 저장
        csv_write = save_csv(df)
        parquet_write = save_parquet(df)

        # 5. 읽기
        csv_read = read_csv()
        parquet_read = read_parquet()

        # 6. 결과 출력
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