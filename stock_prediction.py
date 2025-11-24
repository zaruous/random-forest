
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os # Add this import statement
from pykrx import stock
from pathlib import Path

#출력 디렉토리
output_dir = "output"

#tickrr = "161000" #애경케미칼

tickrr = "053210" #스카이 라이프
#tickrr = "005930" #삼전

ticker = tickrr + ".KS"

if __name__ == "__main__":
    # 데이터 다운로드: 주식, 환율(USD/KRW), 비트코인(BTC-USD)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    strDate = end_date.strftime("%Y%m%d")
    name = yf.Ticker(ticker).info.get("longName")

    plot_filename = f"{output_dir}/{strDate}/{name}_stock_prediction_result_with_fx_btc.png"
    if Path(plot_filename).exists():
        print("파일이 존재합니다.")
        exit()

    print(f"{ticker}의 주식 데이터를 다운로드합니다...")
    data = yf.download(ticker, start=start_date, end=end_date)
    
    print("환율 및 비트코인 데이터를 다운로드합니다...")
    fx_data = yf.download('KRW=X', start=start_date, end=end_date)
    btc_data = yf.download('BTC-USD', start=start_date, end=end_date)

    # 2. 데이터 전처리 및 특성 엔지니어링
    # 데이터 병합을 위한 전처리
    fx_to_join = fx_data[['Close']].rename(columns={'Close': 'USD_KRW'})
    btc_to_join = btc_data[['Close']].rename(columns={'Close': 'BTC_USD'})
    
    # join을 사용하여 데이터 병합
    data = data.join(fx_to_join).join(btc_to_join)
    
    # 주말, 공휴일 등으로 비어있는 값을 이전 값으로 채우기
    data = data.ffill()
    
    # 예측할 타겟 변수 생성 (다음 날 종가)
    data['Target'] = data['Close'].shift(-1)
    
    # 특성 생성 (이동 평균)
    data['MA5'] = data['Close'].rolling(window=5).mean()
    data['MA20'] = data['Close'].rolling(window=20).mean()
    
    # 결측치 제거
    data = data.dropna()
    
    print("데이터 전처리 및 특성 엔지니어링 완료:")
    print(data.head())

    # 3. 학습 및 테스트 데이터 분할
    X = data[['Close', 'High', 'Low', 'Open', 'Volume', 'MA5', 'MA20', 'USD_KRW', 'BTC_USD']]
    y = data['Target']
    
    # 데이터를 시간 순서에 따라 학습용과 테스트용으로 분할 (80% 학습, 20% 테스트)
    split_ratio = 0.8
    split_index = int(len(X) * split_ratio)
    
    X_train, X_test = X[:split_index], X[split_index:]
    y_train, y_test = y[:split_index], y[split_index:]
    
    print("\n데이터 분할 완료:")
    print(f"X_train shape: {X_train.shape}")
    print(f"y_train shape: {y_train.shape}")
    print(f"X_test shape: {X_test.shape}")
    print(f"y_test shape: {y_test.shape}")

    # 4. 모델 학습
    from sklearn.ensemble import RandomForestRegressor
    
    # 랜덤 포레스트 모델 생성 및 학습
    model = RandomForestRegressor(n_estimators=100, random_state=42, oob_score=True)
    print("\n모델 학습을 시작합니다...")
    model.fit(X_train, y_train)
    print("모델 학습 완료.")
    print(f"OOB 점수: {model.oob_score_}")

    # 5. 예측 및 평가
    from sklearn.metrics import mean_squared_error, r2_score
    import matplotlib.pyplot as plt
    
    # 테스트 데이터에 대한 예측
    y_pred = model.predict(X_test)
    
    # 모델 평가
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print("\n모델 평가 결과:")
    print(f"평균 제곱 오차 (MSE): {mse:.2f}")
    print(f"R-squared (R2) 점수: {r2:.2f}")

    # 향후 1주일간의 주가 예측
    future_predictions = []
    current_features = X.iloc[[-1]].copy()
    future_date = pd.to_datetime(current_features.index[0]) + pd.Timedelta(days=1)
    close_history = list(data['Close'].values)

    for _ in range(7):
        # 다음 날 주가 예측
        next_day_prediction = model.predict(current_features)[0]
        future_predictions.append((future_date, next_day_prediction))
        
        # 예측 결과를 새로운 입력 데이터로 사용하기 위해 업데이트
        close_history.append(next_day_prediction)
        
        # 새로운 특성 생성
        new_ma5 = pd.Series(close_history[-5:]).mean()
        new_ma20 = pd.Series(close_history[-20:]).mean()
        
        current_features['Close'] = next_day_prediction
        current_features['High'] = next_day_prediction # 예측값을 기반으로 단순화
        current_features['Low'] = next_day_prediction # 예측값을 기반으로 단순화
        current_features['Open'] = next_day_prediction # 예측값을 기반으로 단순화
        current_features['MA5'] = new_ma5
        current_features['MA20'] = new_ma20
        
        # 날짜 업데이트
        future_date += pd.Timedelta(days=1)

    print("\n향후 1주일간의 주가 예측:")
    for date, price in future_predictions:
        print(f"{date:%Y-%m-%d}의 예측 종가: ${price:.2f}")

    # 예측 결과와 향후 7일 예측을 함께 시각화
    future_dates = [item[0] for item in future_predictions]
    future_prices = [item[1] for item in future_predictions]
    
    # 결과 시각화 (한글 글꼴 설정)
    try:
        from matplotlib import font_manager, rc
        font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
        rc('font', family=font_name)
    except FileNotFoundError:
        print("경고: 'Malgun Gothic' 글꼴을 찾을 수 없습니다. 그래프의 한글이 깨질 수 있습니다.")

    plt.rcParams['axes.unicode_minus'] = False # 마이너스 폰트 깨짐 방지

    # 주식, 환율, 비트코인 데이터를 여러 서브플롯에 그리기
    fig, axes = plt.subplots(1, 1, figsize=(14, 7)) # 1행 1열

    # 1. 주식 예측 그래프
    axes.plot(y_test.index, y_test, label='실제 주가', color='blue')
    axes.plot(y_test.index, y_pred, label='예측 주가', color='red', linestyle='--')
    axes.plot(future_dates, future_prices, label='7일 예측', color='green', linestyle='--') # 7일 예측 추가
    axes.set_title(f'{ticker} {name} 주가 예측: 실제 vs. 예측')
    axes.set_ylabel('종가')
    axes.legend()
    axes.grid(True)

    plt.tight_layout() # 서브플롯 간 간격 자동 조절
    
    #파일 저장
    os.makedirs(f"{output_dir}/{strDate}", exist_ok=True) # 디렉토리가 없으면 생성

    plt.savefig(plot_filename)
    print(f"\n예측 결과 그래프를 '{plot_filename}' 파일로 저장했습니다.")
    # plt.show() # 로컬 환경에서 직접 실행 시 주석 해제하여 그래프 확인
