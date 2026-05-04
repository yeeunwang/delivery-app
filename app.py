import streamlit as st
import itertools

# 가게별 메뉴 데이터
menu_data = {
    # 1. 한솥 (가성비 도시락)
    "한솥_치킨마요": 3800, "한솥_빅치킨마요": 4400, "한솥_돈까스도련님": 4900, 
    "한솥_제육볶음": 4700, "한솥_진달래도시락": 8000,
    
    # 2. 신전떡볶이 (분식)
    "신전_떡볶이(1인분)": 3500, "신전_로제떡볶이": 5500, "신전_치즈김밥": 4000, 
    "신전_튀김오뎅(5개)": 1700, "신전_잡채말이(3개)": 1700,
    
    # 3. 써브웨이 (샌드위치)
    "sub_이탈리안BMT": 7400, "sub_에그마요": 6200, "sub_스테이크앤치즈": 8400, 
    "sub_로스트치킨": 7300, "sub_쿠키팩(6개)": 9100,
    
    # 4. 맘스터치 (버거)
    "맘터_싸이버거단품": 5200, "맘터_싸이버거세트": 7500, "맘터_불불불불싸이버거": 6500, 
    "맘터_휠렛버거": 5000, "맘터_케이준양념감자(L)": 3500,
    
    # 5. 두찜 (찜닭 - 고단가 최적화 테스트용)
    "두찜_까만찜닭(한마리)": 24800, "두찜_로제찜닭(한마리)": 27800, "두찜_마라로제찜닭": 28800, 
    "두찜_묵은지찜닭": 28800, "두찜_납작만두(5개)": 2500,
    
    # 6. 청년피자 (피자)
    "청년_에그콘피자(L)": 24900, "청년_매드쉬림프(L)": 24900, "청년_진짜감자피자(L)": 18900, 
    "청년_할라불고기(L)": 18900, "청년_알리오올리오파스타": 7900,
    
    # 7. 메가커피 (음료)
    "메가_아이스아메리카노": 2000, "메가_메가리카노": 3000, "메가_딸기라떼": 3700, 
    "메가_큐브라떼": 4200, "메가_허니자몽블랙티": 3700,
    
    # 8. 설빙 (디저트)
    "설빙_인절미설빙": 9500, "설빙_애플망고치즈설빙": 13900, "설빙_초코브라우니설빙": 12900, 
    "설빙_생딸기설빙": 15500, "설빙_인절미토스트": 4800,
    
    # 9. 미쉐빙청 (초저가 음료/아이스크림)
    "미쉐_소프트아이스크림": 1000, "미쉐_레몬에이드": 1500, "미쉐_망고선데이": 2500, 
    "미쉐_브라운슈가펄밀크티": 3500, "미쉐_복숭아얼그레이": 2500
}

# 제목 및 팀 정보
st.title("🛵 배달비 최소화 주문 조합 시스템")
st.info("러닝페어 2팀: 김나은, 여샘물, 왕예은, 정보미")

# 1. 입력값 설정
st.subheader("📍 주문 조건 설정")
store = st.selectbox("가게 선택", list(menu_data.keys()))
budget = st.number_input("나의 예산 (원)", value=30000)
min_order = st.number_input("가게 최소주문금액 (원)", value=16000)
main_item = st.selectbox("꼭 포함할 메뉴", list(menu_data[store].keys()))
coupon = st.number_input("적용할 쿠폰 할인액 (원)", value=2000)

# 2. 처리과정: 조합 탐색
if st.button("최적 조합 찾기"):
    items = list(menu_data[store].keys())
    best_cost = float('inf')
    best_combo = None

    for i in range(1, len(items) + 1):
        for combo in itertools.combinations(items, i):
            if main_item not in combo:
                continue

            food_p = sum(menu_data[store][item] for item in combo)
            if food_p < min_order:
                continue

            # 배달비 가상 로직 (음식값에 따라 차등)
            del_f = 0 if food_p >= 50000 else (1000 if food_p >= 35000 else 3000)
            total_p = food_p + del_f - coupon

            if total_p <= budget and total_p < best_cost:
                best_cost = total_p
                best_combo = combo

    # 3. 출력: 최적 주문 조합
    if best_combo:
        st.success(f"🎯 예산 내 최적 조합을 찾았습니다! 총 결제액: {best_cost}원")
        st.write(f"구성: {', '.join(best_combo)}")
    else:
        st.error("조건을 만족하는 조합이 없습니다. 예산을 늘리거나 메뉴를 변경하세요.")
