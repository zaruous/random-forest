
from pykrx import stock
import pandas as pd

def get_and_save_krx_tickers():
    """
    pykrx를 사용하여 KRX(코스피, 코스닥)의 모든 종목 티커와 회사명을 가져와 CSV 파일로 저장합니다.
    yfinance에서 사용 가능하도록 티커에 '.KS' 또는 '.KQ'를 추가합니다.
    """
    print("KRX 모든 종목 코드를 가져오는 중입니다...")
    
    tickers_kospi = stock.get_market_ticker_list(market="KOSPI")
    tickers_kosdaq = stock.get_market_ticker_list(market="KOSDAQ")
    
    all_tickers = tickers_kospi + tickers_kosdaq
    
    ticker_info = []
    for ticker in all_tickers:
        name = stock.get_market_ticker_name(ticker)
        market = "KOSPI" if ticker in tickers_kospi else "KOSDAQ"
        # yfinance는 코스피(.KS)와 코스닥(.KQ)을 구분합니다.
        yfinance_ticker = f"{ticker}.KS" if market == "KOSPI" else f"{ticker}.KQ"
        
        ticker_info.append({"Ticker": yfinance_ticker, "Name": name, "Market": market})
        
    df = pd.DataFrame(ticker_info)
    
    output_filename = "krx_tickers.csv"
    df.to_csv(output_filename, index=False, encoding='utf-8-sig')
    
    print(f"총 {len(df)}개의 종목 코드를 '{output_filename}' 파일에 저장했습니다.")

if __name__ == "__main__":
    get_and_save_krx_tickers()
