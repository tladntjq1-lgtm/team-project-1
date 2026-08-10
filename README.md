# Team Shopping Dashboard

쇼핑몰 주문/고객/상품 데이터를 분석하고 Streamlit 대시보드로 시각화하는 팀 프로젝트입니다.

## 팀 구성 및 역할

| 담당 | 역할 | 주요 파일 |
|---|---|---|
| A | 데이터 점검 및 분석 | `notebooks/01_data_check.ipynb`, `notebooks/02_analysis.ipynb`, `src/data_loader.py`, `src/analysis.py` |
| B | Streamlit 앱 및 시각화 | `app.py`, `src/charts.py` |
| C | 통합, 테스트 및 문서화 | `README.md`, `requirements.txt`, `.gitignore`, `docs/`, `presentation/` |

## 폴더 구조

```
team-shopping-dashboard/
├─ app.py                  # Streamlit 대시보드 실행 파일
├─ data/
│  ├─ raw/                 # 원본 데이터 (수정 금지)
│  └─ processed/           # 전처리된 데이터
├─ notebooks/               # 탐색적 분석 노트북
├─ src/                     # 데이터 로딩·분석·시각화 모듈
├─ docs/                    # 팀 문서 (계획, 작업일지, 데이터 사전 등)
└─ presentation/            # 발표 자료
```

## 데이터

`data/raw/`에 다음 4개 원본 CSV가 있습니다.

- `customers.csv` — 고객 정보
- `products.csv` — 상품 정보
- `orders.csv` — 주문 정보
- `order_items.csv` — 주문 상세(품목) 정보

컬럼 상세는 [`docs/data_dictionary.md`](docs/data_dictionary.md)를 참고하세요.

## 실행 방법

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 브랜치 및 작업 규칙

- `main`은 항상 동작하는 상태로 유지하고, 직접 push하지 않습니다.
- 각자 `feature/이름-작업내용` 브랜치에서 작업 후 Pull Request로 병합합니다.
- 작업 내용은 [`docs/work_log.md`](docs/work_log.md)에 기록합니다.
