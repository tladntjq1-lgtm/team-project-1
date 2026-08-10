# 데이터 사전

`data/raw/`에 있는 원본 CSV 4개의 컬럼 정의입니다. (A 담당이 점검 후 세부 내용 보완)

## customers.csv (고객 정보)

| 컬럼 | 설명 |
|---|---|
| customer_id | 고객 고유 ID |
| name | 고객 이름 |
| gender | 성별 |
| age | 나이 |
| city | 거주 도시 |
| signup_date | 가입일 |

## products.csv (상품 정보)

| 컬럼 | 설명 |
|---|---|
| product_id | 상품 고유 ID |
| product_name | 상품명 |
| category | 상품 카테고리 |
| price | 상품 가격 |

## orders.csv (주문 정보)

| 컬럼 | 설명 |
|---|---|
| order_id | 주문 고유 ID |
| customer_id | 주문한 고객 ID (customers.csv 참조) |
| order_date | 주문일 |
| payment_method | 결제 방식 |
| order_status | 주문 상태 (배송중 등) |

## order_items.csv (주문 상세/품목 정보)

| 컬럼 | 설명 |
|---|---|
| order_item_id | 주문 상세 고유 ID |
| order_id | 연결된 주문 ID (orders.csv 참조) |
| product_id | 주문한 상품 ID (products.csv 참조) |
| quantity | 주문 수량 |
| unit_price | 단가 |

## 테이블 관계

- `orders.customer_id` → `customers.customer_id`
- `order_items.order_id` → `orders.order_id`
- `order_items.product_id` → `products.product_id`

주문 하나에 여러 상품(주문 상세)이 포함될 수 있는 구조입니다.
