import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# -----------------------------------------------------------------------------
# 1. Streamlit 기본 화면 설정 및 프로젝트 제목/설명
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="E-Commerce 주문 데이터 분석 대시보드",
    page_icon="📊",
    layout="wide"
)

st.title("📊 E-Commerce 주문 데이터 분석 대시보드")
st.markdown("""
본 대시보드는 이커머스 쇼핑몰의 주문, 고객, 카테고리 및 매출 데이터를 다이내믹하게 분석하는 도구입니다.  
왼쪽 사이드바의 **검색 필터**를 변경하면 핵심 KPI 지표, 시각화 차트 및 상세 데이터 표가 실시간으로 자동 업데이트됩니다.
""")
st.markdown("---")

# -----------------------------------------------------------------------------
# 2. 샘플 데이터 로드 및 전처리
# -----------------------------------------------------------------------------
@st.cache_data
def load_sample_data():
    np.random.seed(42)
    n_rows = 500
    
    dates = pd.date_range(start="2026-01-01", end="2026-07-31", freq="D")
    categories = ["전자기기", "패션/의류", "생활/주방", "도서", "뷰티"]
    statuses = ["배송완료", "배송완료", "배송완료", "배송중", "취소/환불"]
    payment_methods = ["신용카드", "간편결제", "계좌이체"]
    cities = ["서울", "경기", "부산", "인천", "대구"]
    products = [f"상품_{chr(65+i)}" for i in range(10)]

    data = {
        "주문ID": [f"ORD-{1000+i}" for i in range(n_rows)],
        "고객ID": [f"CUST-{np.random.randint(100, 200)}" for _ in range(n_rows)],
        "주문일자": np.random.choice(dates, n_rows),
        "상품명": np.random.choice(products, n_rows),
        "카테고리": np.random.choice(categories, n_rows),
        "수량": np.random.randint(1, 5, n_rows),
        "단가": np.random.choice([15000, 25000, 50000, 120000, 300000], n_rows),
        "주문상태": np.random.choice(statuses, n_rows),
        "결제방법": np.random.choice(payment_methods, n_rows),
        "고객도시": np.random.choice(cities, n_rows),
    }
    
    df = pd.DataFrame(data)
    df["총금액"] = df["수량"] * df["단가"]
    df["주문일자"] = pd.to_datetime(df["주문일자"])
    return df

raw_df = load_sample_data()

# -----------------------------------------------------------------------------
# 3. 사이드바 필터 구현
# -----------------------------------------------------------------------------
st.sidebar.header("🔍 검색 필터")

# 필터 옵션 정의
category_options = list(raw_df["카테고리"].unique())
status_options = list(raw_df["주문상태"].unique())
payment_options = list(raw_df["결제방법"].unique())
city_options = list(raw_df["고객도시"].unique())
min_date = raw_df["주문일자"].min().date()
max_date = raw_df["주문일자"].max().date()

# UI 필터 컴포넌트
selected_category = st.sidebar.multiselect("상품 카테고리", options=category_options, default=category_options)
selected_status = st.sidebar.multiselect("주문 상태", options=status_options, default=status_options)
selected_payment = st.sidebar.multiselect("결제 방법", options=payment_options, default=payment_options)
selected_city = st.sidebar.multiselect("고객 도시", options=city_options, default=city_options)

date_range = st.sidebar.date_input("주문 기간", value=(min_date, max_date), min_value=min_date, max_value=max_date)

# -----------------------------------------------------------------------------
# 4. 필터 적용 결과 계산 (예외 및 빈 DataFrame 조건 포함)
# -----------------------------------------------------------------------------
if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = raw_df[
        (raw_df["카테고리"].isin(selected_category)) &
        (raw_df["주문상태"].isin(selected_status)) &
        (raw_df["결제방법"].isin(selected_payment)) &
        (raw_df["고객도시"].isin(selected_city)) &
        (raw_df["주문일자"].dt.date >= start_date) &
        (raw_df["주문일자"].dt.date <= end_date)
    ]
else:
    filtered_df = raw_df.copy()

# -----------------------------------------------------------------------------
# 5. 핵심 지표 계산 및 표시 (st.metric 사용)
# -----------------------------------------------------------------------------
st.subheader("📌 핵심 성과 지표 (KPI)")

# 빈 데이터일 때의 처리
is_empty = filtered_df.empty

if is_empty:
    total_customers = 0
    total_products = 0
    total_orders = 0
    total_quantity = 0
    total_amount = 0
    avg_order_amount = 0
    completed_orders = 0
    canceled_orders = 0
else:
    total_customers = filtered_df["고객ID"].nunique()
    total_products = filtered_df["상품명"].nunique()
    total_orders = filtered_df["주문ID"].nunique()
    total_quantity = filtered_df["수량"].sum()
    total_amount = filtered_df["총금액"].sum()
    avg_order_amount = filtered_df["총금액"].mean() if total_orders > 0 else 0
    completed_orders = (filtered_df["주문상태"] == "배송완료").sum()
    canceled_orders = (filtered_df["주문상태"] == "취소/환불").sum()

# metric 레이아웃 (4열 2행)
r1_col1, r1_col2, r1_col3, r1_col4 = st.columns(4)
r1_col1.metric("전체 고객 수", f"{total_customers:,} 명")
r1_col2.metric("전체 상품 수", f"{total_products:,} 개")
r1_col3.metric("전체 주문 수", f"{total_orders:,} 건")
r1_col4.metric("총 주문 수량", f"{total_quantity:,} 개")

r2_col1, r2_col2, r2_col3, r2_col4 = st.columns(4)
r2_col1.metric("총 주문 금액", f"₩{total_amount:,.0f}")
r2_col2.metric("평균 주문 금액", f"₩{avg_order_amount:,.0f}")
r2_col3.metric("배송완료 주문 수", f"{completed_orders:,} 건")
r2_col4.metric("취소/환불 주문 수", f"{canceled_orders:,} 건")

st.markdown("---")

# -----------------------------------------------------------------------------
# 6. 데이터가 없을 때 안내 메시지 및 차트/표 예외 처리
# -----------------------------------------------------------------------------
if is_empty:
    st.warning("⚠️ 선택하신 필터 조건에 해당하는 데이터가 없습니다. 사이드바 필터 조건을 변경해 주시기 바랍니다.")
else:
    # -------------------------------------------------------------------------
    # 7. 차트 구현 및 결과 해석 (최소 2개 이상)
    # -------------------------------------------------------------------------
    st.subheader("📈 데이터 분석 차트")

    c1, c2 = st.columns(2)

    # 차트 1: 카테고리별 매출 막대 차트
    with c1:
        st.markdown("### 1. 카테고리별 매출 현황")
        cat_sales = filtered_df.groupby("카테고리")["총금액"].sum().reset_index().sort_values(by="총금액", ascending=False)
        fig_cat = px.bar(
            cat_sales,
            x="카테고리",
            y="총금액",
            color="카테고리",
            text_auto=',.0f',
            labels={"총금액": "매출액(원)"}
        )
        st.plotly_chart(fig_cat, use_container_width=True)
        
        top_cat = cat_sales.iloc[0]["카테고리"] if len(cat_sales) > 0 else "N/A"
        bottom_cat = cat_sales.iloc[-1]["카테고리"] if len(cat_sales) > 0 else "N/A"
        
        st.info(f"""
        **[결과 해석]**
        - **최고/최저 항목:** 매출이 가장 높은 카테고리는 **{top_cat}**이며, 가장 낮은 카테고리는 **{bottom_cat}**입니다.
        - **눈에 띄는 패턴:** 단가가 높은 품목이 많은 카테고리가 전체 매출 상승을 크게 견인하고 있습니다.
        - **결과 의미:** 주력 카테고리에 마케팅 자원을 집중 배치하는 것이 효과적임을 보여줍니다.
        - **분석 한계:** 본 지표는 단순 매출액 기준이며, 매출 원가 및 영업 이익률 정보는 포함되어 있지 않습니다.
        """)

    # 차트 2: 월별 주문 금액 추이 라인 차트
    with c2:
        st.markdown("### 2. 월별 주문 금액 추이")
        monthly_sales = filtered_df.set_index("주문일자").resample("ME")["총금액"].sum().reset_index()
        monthly_sales["년월"] = monthly_sales["주문일자"].dt.strftime("%Y-%m")
        fig_month = px.line(
            monthly_sales,
            x="년월",
            y="총금액",
            markers=True,
            labels={"총금액": "주문 금액(원)"}
        )
        st.plotly_chart(fig_month, use_container_width=True)

        peak_month = monthly_sales.loc[monthly_sales["총금액"].idxmax()]["년월"] if len(monthly_sales) > 0 else "N/A"
        
        st.info(f"""
        **[결과 해석]**
        - **최고/최저 항목:** 가장 높은 월 매출을 달성한 시점은 **{peak_month}**입니다.
        - **눈에 띄는 패턴:** 월별 매출이 일정한 분기성 또는 프로모션 주기에 맞춰 주기적인 변동성을 나타냅니다.
        - **결과 의미:** 성수기 및 비수기에 맞춘 차별화된 수급 계획 및 프로모션 전략이 필요합니다.
        - **분석 한계:** 외부 환경 요소(시즌성 할인 이벤트, 마케팅 집행액 변동)가 반영되지 않아 순수 기여도를 분리하기 어렵습니다.
        """)

    st.markdown("---")

    # -------------------------------------------------------------------------
    # 8. 필터 결과 표 출력
    # -------------------------------------------------------------------------
    st.subheader("📋 필터 적용 상세 데이터 표")
    st.caption(f"조회된 데이터: 총 {len(filtered_df):,} 건")
    st.dataframe(filtered_df, use_container_width=True)