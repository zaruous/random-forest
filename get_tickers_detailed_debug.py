from pykrx import stock
import pandas as pd
from datetime import datetime
from tqdm import tqdm # tqdm for progress bar
import traceback

def get_and_save_krx_tickers_detailed_debug():
    """
    pykrx를 사용하여 KRX(코스피, 코스닥)의 모든 종목에 대한 상세 정보
    (기본 재무 정보, 시가총액 등)를 가져오는 것을 시도하고, 오류를 디버깅합니다.
    """
    print("KRX 모든 종목의 상세 정보를 가져오는 중입니다... (디버깅 모드)")
    
    # 고정된 최근 날짜를 사용하여 날짜 관련 문제를 배제합니다.
    date_to_check = "20241122"
    
    tickers_kospi = stock.get_market_ticker_list(market="KOSPI")
    tickers_kosdaq = stock.get_market_ticker_list(market="KOSDAQ")
    
    # 디버깅을 위해 일부 티커만 사용
    all_tickers = tickers_kospi + tickers_kosdaq
    tickers_to_process = all_tickers[:10]
    
    all_stocks_info = []

    for ticker in tqdm(tickers_to_process, desc="종목 정보 수집 중"):
        try:
            name = stock.get_market_ticker_name(ticker)
            market = "KOSPI" if ticker in tickers_kospi else "KOSDAQ"
            yfinance_ticker = f"{ticker}.KS" if market == "KOSPI" else f"{ticker}.KQ"

            # 기본 정보 가져오기
            df_fundamental = stock.get_market_fundamental(date_to_check, ticker, "d")
            fund_data = df_fundamental.iloc[0].to_dict() if not df_fundamental.empty else {}
            
            # 시가총액 정보 가져오기
            df_cap = stock.get_market_cap(date_to_check, ticker, "d")
            cap_data = df_cap.iloc[0].to_dict() if not df_cap.empty else {}

            stock_info = {
                "Ticker": yfinance_ticker,
                "Name": name,
                "Market": market,
                "BPS": fund_data.get("BPS", 0),
                "PER": fund_data.get("PER", 0),
                "PBR": fund_data.get("PBR", 0),
                "EPS": fund_data.get("EPS", 0),
                "DIV": fund_data.get("DIV", 0),
                "DPS": fund_data.get("DPS", 0),
                "MarketCap": cap_data.get("시가총액", 0),
                "Shares": cap_data.get("상장주식수", 0)
            }
            all_stocks_info.append(stock_info)
            print(f"성공: {ticker} ({name}) 정보 추가 완료.")
            
        except Exception as e:
            name = stock.get_market_ticker_name(ticker)
            print(f"\n오류: {ticker} ({name}) 처리 중 예외 발생:")
            traceback.print_exc()
            continue
            
    df = pd.DataFrame(all_stocks_info)
    
    if not df.empty:
        output_filename = "krx_tickers_detailed_debug_output.csv"
        df.to_csv(output_filename, index=False, encoding='utf-8-sig')
        print(f"\n{len(df)}개의 종목 상세 정보를 '{output_filename}' 파일에 저장했습니다.")
    else:
        print("\n수집된 데이터가 없어 CSV 파일을 생성하지 않았습니다.")

if __name__ == "__main__":
    get_and_save_krx_tickers_detailed_debug()
