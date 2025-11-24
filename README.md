# 주식 예측 및 재무 데이터 분석 도구

이 프로젝트는 `yfinance`와 `pykrx` 라이브러리를 활용하여 특정 주식의 가격을 예측하고, 한국 증시(KRX) 상장 기업의 주요 재무 지표를 조회하는 파이썬 스크립트 모음입니다.

## 주요 기능

*   **주식 가격 예측 (`stock_prediction.py`)**:
    *   지정된 종목의 과거 데이터를 기반으로 7일간의 주가 예측을 수행합니다.
    *   예측된 주가를 그래프로 시각화하여 실제 주가 및 예측치와 함께 보여줍니다.
    *   환율(USD/KRW) 및 비트코인(BTC-USD) 데이터를 추가 특성으로 활용합니다.

*   **재무 지표 조회 (`get_financials.py`)**:
    *   KRX 상장 기업의 지난 4년간의 연간 주요 재무 지표를 조회합니다.
    *   조회 가능한 지표: BPS, PER, PBR, EPS, DIV, DPS (자세한 설명은 스크립트 내 주석 참조).

## 설치 (Setup)

1.  **Python 설치**:
    컴퓨터에 Python 3.x 버전이 설치되어 있어야 합니다.

2.  **필요한 라이브러리 설치**:
    다음 명령어를 사용하여 필요한 라이브러리들을 설치합니다.
    ```bash
    pip install yfinance pykrx pandas scikit-learn matplotlib
    ```

## 사용법 (Usage)

### 1. 주식 가격 예측 (`stock_prediction.py`)

지정된 종목의 주가 예측을 실행하고, 결과 그래프를 `output/YYYYMMDD/` 디렉토리에 저장합니다.

```bash
python stock_prediction.py
```

*   **종목 변경**: `stock_prediction.py` 파일 내의 `tickrr` 변수(`tickrr = "053210"`)를 수정하여 예측하고자 하는 종목 코드를 변경할 수 있습니다.

### 2. 재무 지표 조회 (`get_financials.py`)

지정된 종목의 연간 재무 지표를 조회하여 콘솔에 출력합니다.

```bash
python get_financials.py
```

*   **종목 변경**: `get_financials.py` 파일 내의 `TICKER` 변수(`TICKER = "161000"`)를 수정하여 조회하고자 하는 종목 코드를 변경할 수 있습니다.

## 재무 지표 용어 설명 (Financial Terms Explanation)

`get_financials.py` 스크립트 내에 각 재무 지표(BPS, PER, PBR, EPS, DIV, DPS)에 대한 자세한 설명이 주석으로 추가되어 있습니다. 스크립트를 직접 확인하시면 됩니다.

## 의존성 (Dependencies)

*   `yfinance`: Yahoo Finance에서 주식 데이터, 환율, 비트코인 데이터 다운로드
*   `pykrx`: KRX (한국거래소) 상장 기업의 재무 지표 조회
*   `pandas`: 데이터 처리 및 분석
*   `scikit-learn`: 머신러닝 모델 (RandomForestRegressor)
*   `matplotlib`: 데이터 시각화
