from pykrx import stock
import pandas as pd

def debug_pykrx_output():
    """
    pykrx의 get_market_fundamental 함수의 반환값을 디버깅합니다.
    """
    ticker = "005930" # 삼성전자
    # date = "20241122"
    from datetime import datetime
    date = datetime.now().strftime("%Y%m%d")

    print(f"'{date}' 기준, 티커 '{ticker}'의 재무 정보를 가져옵니다...")

    try:
        # 일별 데이터 'd'가 아닌, 연간 'y' 또는 분기 'q'를 시도해볼 수 있습니다.
        # 또는, 날짜를 최근 영업일로 명시적으로 찾아볼 수도 있습니다.
        # 여기서는 가장 기본적인 호출을 테스트합니다.
        df_fundamental = stock.get_market_fundamental(date, ticker, "d")

        print("\n--- 수신된 DataFrame ---")
        print(df_fundamental)
        
        print("\n--- DataFrame 정보 ---")
        df_fundamental.info()

        if not df_fundamental.empty:
            print("\n--- DataFrame 컬럼 ---")
            print(df_fundamental.columns)

            print("\n--- 첫 번째 행 내용 ---")
            print(df_fundamental.iloc[0])
        else:
            print("\n수신된 DataFrame이 비어 있습니다.")

    except Exception as e:
        import traceback
        print(f"\n'{ticker}' 정보 조회 중 심각한 오류 발생:")
        traceback.print_exc()

if __name__ == "__main__":
    debug_pykrx_output()
