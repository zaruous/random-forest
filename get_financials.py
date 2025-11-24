from pykrx import stock
from datetime import datetime
import pandas as pd

# ==============================================================================
# 조회할 종목 코드 (기본값: 삼성전자 '005930')
# 다른 종목을 조회하려면 이 코드를 변경하세요. (예: "053210" for KT Skylife)
TICKER = "PFE"
# ==============================================================================

# 조회 기간 설정 (4년 전부터 오늘까지)
end_date = datetime.now()
start_date = end_date.replace(year=end_date.year - 4) # 4년치 데이터 요청에 맞게 변경

# 날짜를 'YYYYMMDD' 형식의 문자열로 변환
str_start_date = start_date.strftime('%Y%m%d')
str_end_date = end_date.strftime('%Y%m%d')

# 종목 이름 조회
try:
    ticker_name = stock.get_market_ticker_name(TICKER)
except Exception:
    ticker_name = "알 수 없는 종목"

print(f"종목: {ticker_name} ({TICKER})")
print(f"조회 기간: {str_start_date} ~ {str_end_date}")
print("재무 정보를 조회합니다...")

try:
    # pykrx의 get_market_fundamental 함수는 'q' (분기별) freq를 직접 지원하지 않습니다.
    # 'y' (연간), 'm' (월간), 'd' (일간)만 가능합니다.
    # 여기서는 연간 데이터를 조회합니다.
    df_financials = stock.get_market_fundamental(str_start_date, str_end_date, TICKER, freq='y')

    if df_financials.empty:
        print("조회된 데이터가 없습니다. 종목 코드나 기간을 확인해주세요.")
    else:
        # BPS (주당순자산): Book-value Per Share. 기업의 총자산에서 총부채를 뺀 순자산을 발행주식수로 나눈 값.
        # PER (주가수익비율): Price-to-Earnings Ratio. 현재 주가를 주당순이익(EPS)으로 나눈 값. 원금 회수까지 10년 걸림,
        # PBR (주가순자산비율): Price-가를 주당순자산(BPS)으로 나눈 값.
        # EPS (주당순이익): Earnings Per Share. 기업의 순이익을 발행주식수로 나눈 값.
        # DIV (현금배당수익률): Dividend Yield. 주식 1주당 연간 현금 배당금을 현재 주가로 나눈 비율.
        # DPS (주당배당금): Dividend Per Share. 기업이 1주당 지급하는 현금 배당금.

        # 용어,핵심 질문,비유 (스마일 카페),판단 기준
        # BPS,망하면 얼마 받나?,"망하면 8,000원 돌려받음",높을수록 안전함
        # PER,본전까지 몇 년?,원금 회수까지 10년 걸림,낮을수록 저평가 (보통)
        # PBR,자산 대비 비싼가?,실제 가치의 1.25배 가격,1 미만이면 싼 편
        # EPS,돈 잘 버나?,"1주가 1년간 1,000원 벎",높을수록 좋음
        # DIV,이자율 몇 %?,연 이자 5%,은행 금리보다 높으면 좋음
        # DPS,용돈 얼마 주나?,현금 500원 받음,많을수록 좋음



        # 인덱스(날짜)를 오름차순으로 정렬
        df_financials = df_financials.sort_index()
        
        # Pandas 출력 옵션 설정 (모든 열과 행을 보여주도록)
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 1000)

        print("\n[지난 4년 연간 재무 지표]")
        print(df_financials)


except Exception as e:
    print(f"데이터를 조회하는 중 오류가 발생했습니다: {e}")
