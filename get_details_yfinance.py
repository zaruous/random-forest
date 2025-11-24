import datetime

import pandas as pd
import yfinance as yf
from tqdm import tqdm
import os

def get_yfinance_details():
    """
    yfinance를 사용하여 krx_tickers.csv에 있는 모든 종목의 상세 재무 정보를 가져와
    새로운 CSV 파일로 저장합니다.
    """
    ' 현재 시간을 yyyyMMddHHmm형태로
    formatted_time = datetime.datetime.now().strftime("%Y%m%d%H%M")

    output_filename = formatted_time + "_krx_tickers_yfinance_details.csv"
    # 스크립트 실행 시 이전 파일이 있다면 삭제하여 새로 작성
    try:
        os.remove(output_filename)
    except FileNotFoundError:
        pass # 파일이 없으면 그냥 진행

    try:
        tickers_df = pd.read_csv("krx_tickers.csv")
    except FileNotFoundError:
        print("에러: 'krx_tickers.csv' 파일을 찾을 수 없습니다.")
        print("먼저 'get_tickers.py'를 실행하여 종목 코드 목록을 생성해주세요.")
        return

    all_stocks_info = []
    chunk_size = 100
    output_filename = "krx_tickers_yfinance_details.csv"
    
    # 파일을 새로 작성하기 위해, 시작 시 빈 파일 생성 (또는 덮어쓰기)
    # 첫 번째 청크에서 헤더를 쓸 것이므로, 여기서는 그냥 비워둡니다.
    # pd.DataFrame(columns=...]).to_csv(output_filename, index=False) # <--- Optional
    
    print("yfinance를 사용하여 모든 종목의 재무 정보를 가져옵니다... (100개 단위로 저장)")

    for index, row in tqdm(tickers_df.iterrows(), total=tickers_df.shape[0], desc="재무 정보 수집 중"):
        ticker_code = row['Ticker']
        try:
            ticker = yf.Ticker(ticker_code)
            info = ticker.info
            
            stock_info = {
                "Ticker": ticker_code, "Name": row['Name'], "Market": row['Market'],
                "MarketCap": info.get("marketCap"), "PER": info.get("trailingPE"),
                "PBR": info.get("priceToBook"), "EPS": info.get("trailingEps"),
                "DividendYield": info.get("dividendYield"), "Beta": info.get("beta"),
                "52WeekHigh": info.get("fiftyTwoWeekHigh"), "52WeekLow": info.get("fiftyTwoWeekLow"),
                "Volume": info.get("volume"), "AverageVolume": info.get("averageVolume"),
            }
            all_stocks_info.append(stock_info)

            # 청크 사이즈에 도달하면 파일에 저장
            if len(all_stocks_info) >= chunk_size:
                df_chunk = pd.DataFrame(all_stocks_info)
                # 파일이 이미 존재하면 헤더 없이 추가, 없으면 헤더와 함께 새로 쓰기
                header = not pd.io.common.file_exists(output_filename)
                df_chunk.to_csv(output_filename, mode='a', header=header, index=False, encoding='utf-8-sig')
                all_stocks_info = [] # 리스트 비우기

        except Exception as e:
            continue

    # 마지막 남은 청크 저장
    if all_stocks_info:
        df_chunk = pd.DataFrame(all_stocks_info)
        header = not pd.io.common.file_exists(output_filename)
        df_chunk.to_csv(output_filename, mode='a', header=header, index=False, encoding='utf-8-sig')

    print(f"\n종목 상세 재무 정보 저장이 '{output_filename}' 파일에 완료되었습니다.")


if __name__ == "__main__":
    get_yfinance_details()
