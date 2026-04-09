import pyupbit
import time
import datetime
import pandas as pd

ticker = "KRW-BTC"

def get_price_analysis(ticker):
    """최근 가격의 평균, 상단(고점), 하단(저점) 분석"""
    # 최근 20분간의 데이터를 가져옴
    df = pyupbit.get_ohlcv(ticker, interval="minute1", count=20)
    
    avg_price = df['close'].mean()     # 20분 평균 가격
    high_price = df['high'].max()     # 20분 중 최고가
    low_price = df['low'].min()       # 20분 중 최저가
    
    return avg_price, high_price, low_price

print("🚀 비트코인 평균가 기준 매수/매도 감시를 시작합니다.")

while True:
    try:
        now = datetime.datetime.now()
        current_price = pyupbit.get_current_price(ticker)
        avg_p, high_p, low_p = get_price_analysis(ticker)

        print(f"[{now.strftime('%H:%M:%S')}] 현재가: {current_price:,.0f} | 20분평균: {avg_p:,.0f}")

        # 로직 설정: 평균가보다 0.5% 이상 떨어지면 매수, 0.5% 이상 오르면 매도 추천
        # (비율은 시장 상황에 따라 조정 가능합니다)
        buy_threshold = avg_p * 0.995   # 평균보다 0.5% 낮은 가격
        sell_threshold = avg_p * 1.005  # 평균보다 0.5% 높은 가격

        if current_price <= buy_threshold:
            print(f"✨ [매수 추천] 현재가가 평균보다 낮습니다! (기준: {buy_threshold:,.0f})")
        elif current_price >= sell_threshold:
            print(f"💰 [매도 추천] 현재가가 평균보다 높습니다! 수익 실현 검토 (기준: {sell_threshold:,.0f})")
        else:
            print("↕️ 현재 평균가 근처에서 횡보 중입니다. (관망)")

        print(f"   (최근 20분 범위: {low_p:,.0f} ~ {high_p:,.0f})")
        print("-" * 50)

        time.sleep(10) # 10초마다 반복

    except Exception as e:
        print(f"오류 발생: {e}")
        time.sleep(1)