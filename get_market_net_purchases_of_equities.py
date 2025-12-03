import argparse
import pandas as pd
from pykrx import stock
from datetime import datetime

def get_market_net_purchases_of_equities(start_date: str, end_date: str) -> pd.DataFrame:
    """
            fromdate (str): 조회 시작 일자 (YYMMDD)
            todate   (str): 조회 종료 일자 (YYMMDD)
            market   (str): 조회 시장 (KOSPI/KOSDAQ/KONEX/ALL)
            investor (str): 투자자
             - 금융투자 / 보험 / 투신 / 사모 / 은행 / 기타금융 / 연기금 / 기관합계 / 기타법인 / 개인 / 외국인 / 기타외국인 / 전체
            Note : inverstor를 전체로 설정하면 순매수 금액이 0으로 나옵니다.
    """
    
    try:
        df = stock.get_market_net_purchases_of_equities(fromdate=start_date, todate=end_date, market="KOSPI", investor="개인")
        if not df.empty:
            # Rename columns for clarity (optional)
            return df
        else:
            return pd.DataFrame()
    except Exception as e:
        print(f"An error occurred while fetching data : {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    current_year = datetime.now().year
    month_year = datetime.now().month
    current_day = datetime.now().strftime("%d")
    
    default_start_date = f"{current_year}{month_year}{current_day}"
    default_end_date = f"{current_year}{month_year}{current_day}"

    parser = argparse.ArgumentParser(description="상위 투자 목록 출력")
    parser.add_argument("--start_date", type=str, default=default_start_date,
                        help=f"The start date in 'YYYYMMDD' format. Default is '{default_start_date}'.")
    parser.add_argument("--end_date", type=str, default=default_end_date,
                        help=f"The end date in 'YYYYMMDD' format. Default is '{default_end_date}'.")

    args = parser.parse_args()

    ret_data = get_market_net_purchases_of_equities(args.start_date, args.end_date)

    if not ret_data.empty:
        print(ret_data)
        ret_data.to_csv('get_market_net_purchases_of_equities.csv')
    else:
        print("Could not retrieve data.")
