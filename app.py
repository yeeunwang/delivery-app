%%writefile app.py
import streamlit as st
import itertools

# 제안서 기반 모의 데이터 [cite: 94]
menu_data = {'교촌치킨':{"허니콤보": 23000, "레드콤보": 23000, "웨지감자": 6500, 
    "치즈볼": 5500, "콜라(대)": 3000, "치킨무": 500}, '맘스터치 종로대학로점': {'화이트갈릭버거 단품': 6300, '딥치즈버거 단품': 6200, '휠렛버거 단품': 5800, '불고기버거 단품': 5000, '통새우버거 단품': 4900, '쉬림프싸이플렉스버거 단품': 9000, '싸이버거 단품': 6000, '불싸이버거 단품': 6200, '핫치즈 빅싸이순살': 17000, '후라이드 빅싸이순살': 14400, '맘스양념 빅싸이순살': 16400, '간장마늘 빅싸이순살': 16400, '골든갈릭 빅싸이순살': 17000, '케이준떡강정S': 5400, '케이준떡강정R': 14000, '간장마늘떡강정S': 5600, '간장마늘떡강정R': 14500, '치파오떡강정S': 5600, '케이준떡강정R': 14500,' 콘샐러드': 2700, '코울슬로': 2700, '바삭크림치즈볼(2조각)': 2900, '치즈스틱(2조각)': 2900, '펩시콜라': 2400, '펩시콜라제로':2400, '사이다':2400, '청포도에이드':3100, '레몬에이드':3100, '오렌지주스': 2900, '아이스아메리카노': 2900}}

st.title("🛵 배달비 최소화 주문 조합 시스템")
st.info("러닝페어 2팀: 김나은, 여샘물, 왕예은, 정보미") # [cite: 12]

# 1. 입력값 설정 [cite: 77]
st.subheader("📍 주문 조건 설정")
budget = st.number_input("나의 예산 (원)", value=30000)
min_order = st.number_input("가게 최소주문금액 (원)", value=16000)
main_item = st.selectbox("꼭 포함할 메뉴", list(menu_data.keys()))
coupon = st.number_input("적용할 쿠폰 할인액 (원)", value=2000)

# 2. 처리과정: 조합 탐색 [cite: 78]
if st.button("최적 조합 찾기"):
    items = list(menu_data.keys())
    best_cost = float('inf')
    best_combo = None

    for i in range(1, len(items) + 1):
        for combo in itertools.combinations(items, i):
            if main_item not in combo: continue
            
            food_p = sum(menu_data[item] for item in combo)
            if food_p < min_order: continue
            
            # 배달비 가상 로직 (음식값에 따라 차등)
            del_f = 0 if food_p >= 50000 else (1000 if food_p >= 35000 else 3000)
            total_p = food_p + del_f - coupon
            
            if total_p <= budget and total_p < best_cost:
                best_cost = total_p
                best_combo = combo

    # 3. 출력: 최적 주문 조합 [cite: 79]
    if best_combo:
        st.success(f"🎯 예산 내 최적 조합을 찾았습니다! 총 결제액: {best_cost}원")
        st.write(f"구성: {', '.join(best_combo)}")
    else:
        st.error("조건을 만족하는 조합이 없습니다. 예산을 늘리거나 메뉴를 변경하세요.")
