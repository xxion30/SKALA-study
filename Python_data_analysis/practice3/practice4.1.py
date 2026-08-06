"""
=========================================================
[Practice 4] 시각화 · 통계 검정 · sklearn Pipeline
파일명 : 판교_2반_양시온.py
작성자 : 양시온
작성일 : 2026-08-04

프로그램 목적
- sales_100k.csv 데이터를 이용한 EDA 시각화
- t-test 및 카이제곱 검정 수행
- sklearn Pipeline 구성 및 저장
- Plotly 인터랙티브 차트 저장

=========================================================
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import joblib

from scipy.stats import ttest_ind, chi2_contingency

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

#한글 폰트 설정
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "AppleGothic"
plt.rcParams["axes.unicode_minus"] = False

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
# 날짜 컬럼 datetime 형식으로 변환
# 월별 집계를 위해 datetime 타입으로 변경한다.
# -------------------------------------------------------
df["order_date"] = pd.to_datetime(df["order_date"])


# -------------------------------------------------------
# IQR 이상치 제거
# Practice3와 동일한 방식 사용
# 이후 모든 분석은 df_clean을 사용한다.
# -------------------------------------------------------

Q1 = df["amount"].quantile(0.25)
Q3 = df["amount"].quantile(0.75)

IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

print("\nIQR 범위")
print(lower, "~", upper)

before = len(df)

# amount가 정상 범위인 데이터만 선택
df_clean = df[df["amount"].between(lower, upper)].copy()

after = len(df_clean)

print(f"\n이상치 제거 전 : {before:,}")
print(f"이상치 제거 후 : {after:,}")


# -------------------------------------------------------
# 1. EDA 시각화 (2 × 2 Subplot)
# 히스토그램 + KDE
# 박스플롯
# 월별 라인차트
# 상관 히트맵
# -------------------------------------------------------

fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# -------------------------------------------------------
# (1) 히스토그램 + KDE
# amount 분포 확인
# -------------------------------------------------------

sns.histplot(
    data=df_clean,
    x="amount",
    kde=True,
    color="skyblue",
    ax=axes[0, 0]
)

axes[0, 0].set_title("Amount Distribution")
axes[0, 0].set_xlabel("Amount")
axes[0, 0].set_ylabel("Count")


# -------------------------------------------------------
# (2) 박스플롯
# 지역별 매출 분포 비교
# -------------------------------------------------------

sns.boxplot(
    data=df_clean,
    x="region",
    y="amount",
    ax=axes[0, 1]
)

axes[0, 1].set_title("Amount by Region")
axes[0, 1].set_xlabel("Region")
axes[0, 1].set_ylabel("Amount")


# -------------------------------------------------------
# (3) 월별 총매출 라인차트
# order_date에서 월을 추출하여 집계
# -------------------------------------------------------

monthly_sales = (
    df_clean
    .groupby(df_clean["order_date"].dt.month)["amount"]
    .sum()
)

axes[1, 0].plot(
    monthly_sales.index,
    monthly_sales.values,
    marker="o",
    linewidth=2
)

axes[1, 0].set_title("Monthly Sales")
axes[1, 0].set_xlabel("Month")
axes[1, 0].set_ylabel("Total Sales")
axes[1, 0].grid(True)


# -------------------------------------------------------
# (4) 상관계수 히트맵
# 수치형 변수 간 상관관계 확인
# -------------------------------------------------------

corr = df_clean[
    [
        "quantity",
        "unit_price",
        "customer_age",
        "amount"
    ]
].corr()

sns.heatmap(
    corr,
    annot=True,
    cmap="Blues",
    fmt=".2f",
    ax=axes[1, 1]
)

axes[1, 1].set_title("Correlation Heatmap")

plt.tight_layout()
plt.show()

# -------------------------------------------------------
# 2. 통계 검정
# t-test
# 서울과 부산의 평균 매출 차이 검정
# -------------------------------------------------------

print("\n==============================")
print("t-test")
print("==============================")

# 서울과 부산 데이터 추출
seoul = df_clean[df_clean["region"] == "서울"]["amount"]
busan = df_clean[df_clean["region"] == "부산"]["amount"]

# 독립표본 t-test 수행
t_stat, p_value = ttest_ind(
    seoul,
    busan,
    equal_var=False,
    nan_policy="omit"
)

print(f"T Statistic : {t_stat:.4f}")
print(f"P-value     : {p_value:.4f}")

# p-value 해석
if p_value < 0.05:
    print("결론 : 서울과 부산의 평균 매출은 유의미한 차이가 있습니다.")
else:
    print("결론 : 서울과 부산의 평균 매출은 유의미한 차이가 없습니다.")


# -------------------------------------------------------
# 카이제곱 검정
# 지역과 카테고리의 독립성 검정
# -------------------------------------------------------

print("\n==============================")
print("Chi-square Test")
print("==============================")

# 분할표 생성
table = pd.crosstab(
    df_clean["region"],
    df_clean["category"]
)

print("\n분할표")
print(table)

# 카이제곱 검정 수행
chi2, p_value, dof, expected = chi2_contingency(table)

print(f"\nChi-square : {chi2:.4f}")
print(f"P-value    : {p_value:.4f}")

# 결과 해석
if p_value < 0.05:
    print("결론 : 지역과 카테고리는 서로 관련이 있습니다.")
else:
    print("결론 : 지역과 카테고리는 서로 독립입니다.")


# -------------------------------------------------------
# 3. sklearn Pipeline
# 전처리 + 모델을 하나의 Pipeline으로 구성
# -------------------------------------------------------

print("\n==============================")
print("Pipeline")
print("==============================")


# -------------------------------------------------------
# 입력(X)과 정답(y) 분리
# amount를 예측하도록 설정
# -------------------------------------------------------

X = df_clean.drop(columns=["amount", "order_id"])

y = df_clean["amount"]


# -------------------------------------------------------
# 숫자형 컬럼
# -------------------------------------------------------

numeric_features = [
    "quantity",
    "unit_price",
    "customer_age"
]


# -------------------------------------------------------
# 범주형 컬럼
# -------------------------------------------------------

categorical_features = [
    "region",
    "category",
    "payment_method",
    "customer_gender"
]


# -------------------------------------------------------
# 숫자형 전처리
# 결측치는 중앙값으로 채우고 표준화 수행
# -------------------------------------------------------

numeric_transformer = Pipeline(

    steps=[

        ("imputer",
         SimpleImputer(strategy="median")),

        ("scaler",
         StandardScaler())

    ]

)


# -------------------------------------------------------
# 범주형 전처리
# 결측치는 최빈값으로 채우고 One-Hot Encoding 수행
# -------------------------------------------------------

categorical_transformer = Pipeline(

    steps=[

        ("imputer",
         SimpleImputer(strategy="most_frequent")),

        ("encoder",
         OneHotEncoder(handle_unknown="ignore"))

    ]

)


# -------------------------------------------------------
# 숫자형과 범주형 전처리를 하나로 묶는다.
# -------------------------------------------------------

preprocessor = ColumnTransformer(

    transformers=[

        ("num",
         numeric_transformer,
         numeric_features),

        ("cat",
         categorical_transformer,
         categorical_features)

    ]

)


# -------------------------------------------------------
# Pipeline 생성
# 전처리 → 선형회귀 모델
# -------------------------------------------------------

model = Pipeline(

    steps=[

        ("preprocessor",
         preprocessor),

        ("model",
         LinearRegression())

    ]

)


# -------------------------------------------------------
# 학습용 / 테스트용 데이터 분리
# -------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.2,
    random_state=42

)


# -------------------------------------------------------
# 모델 학습
# -------------------------------------------------------

model.fit(X_train, y_train)


# -------------------------------------------------------
# 예측 수행
# -------------------------------------------------------

pred = model.predict(X_test)


# -------------------------------------------------------
# 모델 성능(R²)
# -------------------------------------------------------

score = model.score(X_test, y_test)

print(f"R² Score : {score:.4f}")


# -------------------------------------------------------
# 모델 저장
# -------------------------------------------------------

joblib.dump(
    model,
    "sales_pipeline.pkl"
)

print("Pipeline 저장 완료")


# -------------------------------------------------------
# 저장된 모델 다시 불러오기
# -------------------------------------------------------

loaded_model = joblib.load(
    "sales_pipeline.pkl"
)

print(
    "Reload Score :",
    loaded_model.score(X_test, y_test)
)


# -------------------------------------------------------
# 4. Plotly 인터랙티브 차트
# 지역·카테고리별 총매출 시각화
# -------------------------------------------------------

plot_df = (

    df_clean

    .groupby(

        ["region", "category"]

    )["amount"]

    .sum()

    .reset_index()

)


# -------------------------------------------------------
# Plotly 막대그래프 생성
# -------------------------------------------------------

fig = px.bar(

    plot_df,

    x="region",
    y="amount",

    color="category",

    barmode="group",

    title="Total Sales by Region and Category"

)


# -------------------------------------------------------
# HTML 파일 저장
# -------------------------------------------------------

fig.write_html(
    "region_category_sales.html"
)

print("Plotly HTML 저장 완료")