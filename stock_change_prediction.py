
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os # Add this import statement

#출력 디렉토리
output_dir = "output"
ticker = "458760.KS"

if __name__ == "__main__":
    # 데이터 다운로드: 주식, 환율(USD/KRW), 비트코인(BTC-USD)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    print(f"{ticker}의 주식 데이터를 다운로드합니다...")
    data = yf.download(ticker, start=start_date, end=end_date)
    
    print("환율 및 비트코인 데이터를 다운로드합니다...")
    fx_data = yf.download('KRW=X', start=start_date, end=end_date)
    btc_data = yf.download('BTC-USD', start=start_date, end=end_date)

    # 2. 데이터 전처리 및 특성 엔지니어링
    import numpy as np

    # 데이터 병합을 위한 전처리
    fx_to_join = fx_data[['Close']].rename(columns={'Close': 'USD_KRW'})
    btc_to_join = btc_data[['Close']].rename(columns={'Close': 'BTC_USD'})
    
    # join을 사용하여 데이터 병합
    data = data.join(fx_to_join).join(btc_to_join)
    
    # 주말, 공휴일 등으로 비어있는 값을 이전 값으로 채우기
    data = data.ffill()

    # 원본 값을 유지한 후, 변화율 계산
    original_data = data.copy()

    # 특성 생성 (이동 평균)
    data['MA5'] = data['Close'].rolling(window=5).mean()
    data['MA20'] = data['Close'].rolling(window=20).mean()

    # 변화율 특성 생성
    change_cols = ['Close', 'High', 'Low', 'Open', 'Volume', 'MA5', 'MA20', 'USD_KRW', 'BTC_USD']
    for col in change_cols:
        data[f'{col}_change'] = data[col].pct_change()

    # 예측할 타겟 변수 생성 (다음 날 종가 변화율)
    data['Target'] = data['Close_change'].shift(-1)
    
    # 무한대 값을 NaN으로 변경 후 결측치 제거
    data.replace([np.inf, -np.inf], np.nan, inplace=True)
    data = data.dropna()
    
    print("데이터 전처리 및 특성 엔지니어링 완료:")
    print(data[[f'{col}_change' for col in change_cols] + ['Target']].head())

    # 3. 학습 및 테스트 데이터 분할
    feature_cols = [f'{col}_change' for col in change_cols]
    X = data[feature_cols]
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
    print(f"평균 제곱 오차 (MSE): {mse:.6f}")
    print(f"R-squared (R2) 점수: {r2:.2f}")
    
    # 결과 시각화 (한글 글꼴 설정)
    try:
        from matplotlib import font_manager, rc
        font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
        rc('font', family=font_name)
    except FileNotFoundError:
        print("경고: 'Malgun Gothic' 글꼴을 찾을 수 없습니다. 그래프의 한글이 깨질 수 있습니다.")

    plt.rcParams['axes.unicode_minus'] = False # 마이너스 폰트 깨짐 방지

    # 주식 변화율 예측 및 다른 지표 변화율 함께 시각화
    fig, axes = plt.subplots(1, 1, figsize=(14, 7))

    # 테스트 기간에 해당하는 환율 및 BTC 데이터 추출
    fx_change_to_plot = data.loc[y_test.index, 'USD_KRW_change']
    btc_change_to_plot = data.loc[y_test.index, 'BTC_USD_change']

    axes.plot(y_test.index, y_test, label='실제 변화율 (주식)', color='blue', alpha=0.9, linewidth=2)
    axes.plot(y_test.index, y_pred, label='예측 변화율 (주식)', color='red', linestyle='--', alpha=0.8)
    
    axes.plot(fx_change_to_plot.index, fx_change_to_plot, label='USD/KRW 변화율', color='green', alpha=0.5, linestyle=':')
    # axes.plot(btc_change_to_plot.index, btc_change_to_plot, label='BTC/USD 변화율', color='orange', alpha=0.5, linestyle=':')

    axes.set_title(f'{ticker} 주가 및 주요 지표 변화율 예측')
    axes.set_ylabel('변화율')
    axes.legend()
    axes.grid(True)

    plt.tight_layout()
    
    #파일 저장
    os.makedirs(output_dir, exist_ok=True)
    
    plot_filename = f"{output_dir}/{ticker}_stock_change_prediction_with_fx_btc.png"
    plt.savefig(plot_filename)
    print(f"\n예측 결과 그래프를 '{plot_filename}' 파일로 저장했습니다.")
    # plt.show()

    # 최신 데이터를 사용하여 내일의 주가 변화율 예측
    last_row_features = X.iloc[[-1]]
    next_day_change_prediction = model.predict(last_row_features)[0]
    
    # 예측에 사용된 마지막 날의 실제 종가 가져오기
    last_index = last_row_features.index[0]
    last_actual_close = float(original_data.loc[original_data.index == last_index, 'Close'].iloc[-1])
    
    # 예상 종가 계산
    predicted_price = last_actual_close * (1 + next_day_change_prediction)
    
    print(f"\n최신 데이터를 바탕으로 예측한 내일({pd.to_datetime(last_row_features.index[0]) + pd.Timedelta(days=1):%Y-%m-%d})의 종가 변화율은 {next_day_change_prediction:+.2%} 입니다.")
    print(f"예상 종가는 {predicted_price:.2f} 입니다.")

