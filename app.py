%%writefile app.py
import streamlit as st
import itertools

# 제안서 기반 모의 데이터 [cite: 94]
menu_data = {
    "허니콤보": 23000, "레드콤보": 23000, "웨지감자": 6500, 
    "치즈볼": 5500, "콜라(대)": 3000, "치킨무": 500}

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

    for i in range(1, len(items) + 1000):
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
