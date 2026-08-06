"""
=========================================================
[Practice 4] 시각화 · 통계 검정 · sklearn Pipeline
파일명 : 판교_2반_양시온.py
작성자 : 양시온
작성일 : 2026-08-04

프로그램 목적
- sales_100k.csv 데이터를 이용한 시각화
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


# -------------------------------------------------------
# 날짜형 변환
# -------------------------------------------------------
df["order_date"] = pd.to_datetime(df["order_date"])


# -------------------------------------------------------
# IQR 이상치 제거 (Practice3과 동일)
# -------------------------------------------------------
Q1 = df["amount"].quantile(0.25)
Q3 = df["amount"].quantile(0.75)

IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

df_clean = df[df["amount"].between(lower, upper)].copy()

print(f"이상치 제거 : {len(df)} -> {len(df_clean)}")


# =======================================================
# 1. EDA 시각화 (2×2 Subplot)
# =======================================================

fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# -----------------------------------
# (1) 히스토그램 + KDE
# -----------------------------------
sns.histplot(
    data=df_clean,
    x="amount",
    kde=True,
    ax=axes[0, 0]
)

axes[0, 0].set_title("Amount Distribution")


# -----------------------------------
# (2) 박스플롯
# -----------------------------------
sns.boxplot(
    data=df_clean,
    x="region",
    y="amount",
    ax=axes[0, 1]
)

axes[0, 1].set_title("Amount by Region")


# -----------------------------------
# (3) 월별 라인차트
# -----------------------------------
monthly = (
    df_clean
    .groupby(df_clean["order_date"].dt.month)["amount"]
    .sum()
)

axes[1, 0].plot(
    monthly.index,
    monthly.values,
    marker="o"
)

axes[1, 0].set_title("Monthly Sales")
axes[1, 0].set_xlabel("Month")
axes[1, 0].set_ylabel("Sales")


# -----------------------------------
# (4) 상관 히트맵
# -----------------------------------
corr = df_clean[
    ["quantity",
     "unit_price",
     "customer_age",
     "amount"]
].corr()

sns.heatmap(
    corr,
    annot=True,
    cmap="Blues",
    ax=axes[1, 1]
)

axes[1, 1].set_title("Correlation Heatmap")

plt.tight_layout()
plt.show()


# =======================================================
# 2. 통계 검정
# =======================================================

print("\n==============================")
print("t-test")
print("==============================")

seoul = df_clean[df_clean["region"] == "서울"]["amount"]
busan = df_clean[df_clean["region"] == "부산"]["amount"]

t_stat, p_value = ttest_ind(
    seoul,
    busan,
    equal_var=False,
    nan_policy="omit"
)

print(f"T statistic : {t_stat:.4f}")
print(f"P-value     : {p_value:.4f}")

if p_value < 0.05:
    print("결론 : 서울과 부산의 평균 매출은 유의미한 차이가 있습니다.")
else:
    print("결론 : 서울과 부산의 평균 매출은 유의미한 차이가 없습니다.")


# -------------------------------------------------------
# 카이제곱 검정
# 지역 × 카테고리
# -------------------------------------------------------

print("\n==============================")
print("Chi-square Test")
print("==============================")

table = pd.crosstab(
    df_clean["region"],
    df_clean["category"]
)

chi2, p, dof, expected = chi2_contingency(table)

print(f"Chi-square : {chi2:.4f}")
print(f"P-value    : {p:.4f}")

if p < 0.05:
    print("결론 : 지역과 카테고리는 서로 관련이 있습니다.")
else:
    print("결론 : 지역과 카테고리는 서로 독립입니다.")


# =======================================================
# 3. sklearn Pipeline
# =======================================================

print("\n==============================")
print("Pipeline")
print("==============================")

X = df_clean.drop(columns=["amount", "order_id"])

y = df_clean["amount"]


numeric_features = [
    "quantity",
    "unit_price",
    "customer_age"
]

categorical_features = [
    "region",
    "category",
    "payment_method",
    "customer_gender"
]


numeric_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])


categorical_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])


preprocessor = ColumnTransformer([
    ("num", numeric_transformer, numeric_features),
    ("cat", categorical_transformer, categorical_features)
])


model = Pipeline([
    ("preprocessor", preprocessor),
    ("model", LinearRegression())
])


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model.fit(X_train, y_train)

pred = model.predict(X_test)

score = model.score(X_test, y_test)

print(f"R² Score : {score:.4f}")


# -------------------------------------------------------
# 모델 저장
# -------------------------------------------------------

joblib.dump(model, "sales_pipeline.pkl")
print("Pipeline 저장 완료")


# -------------------------------------------------------
# 모델 재로드
# -------------------------------------------------------

loaded_model = joblib.load("sales_pipeline.pkl")

print(
    "Reload Score :",
    loaded_model.score(X_test, y_test)
)


# =======================================================
# 4. Plotly
# =======================================================

plot_df = (
    df_clean
    .groupby(["region", "category"])["amount"]
    .sum()
    .reset_index()
)

fig = px.bar(
    plot_df,
    x="region",
    y="amount",
    color="category",
    barmode="group",
    title="Region & Category Sales"
)

fig.write_html("region_category_sales.html")

print("Plotly HTML 저장 완료")