import streamlit as st
import itertools

# 1. 가게별 메뉴 데이터 구축
store_menu_data = {
    "한솥도시락": {"치킨마요": 3800, "빅치킨마요": 4400, "돈까스도련님": 4900, "제육볶음": 4700, "진달래도시락": 8000},
    "신전떡볶이": {"떡볶이(1인분)": 3500, "로제떡볶이": 5500, "치즈김밥": 4000, "튀김오뎅(5개)": 1700, "잡채말이(3개)": 1700},
    "써브웨이": {"이탈리안BMT": 7400, "에그마요": 6200, "스테이크앤치즈": 8400, "로스트치킨": 7300, "쿠키팩(6개)": 9100},
    "맘스터치": {"싸이버거세트": 7500, "불불불불싸이버거": 6500, "휠렛버거": 5000, "케이준양념감자(L)": 3500, "치즈스틱": 2000},
    "두찜": {"까만찜닭(한마리)": 24800, "로제찜닭(한마리)": 27800, "마라로제찜닭": 28800, "납작만두(5개)": 2500, "공기밥": 1000},
    "청년피자": {"에그콘피자(L)": 24900, "매드쉬림프(L)": 24900, "진짜감자피자(L)": 18900, "할라불고기(L)": 18900, "알리오올리오파스타": 7900},
    "메가커피": {"아이스아메리카노": 2000, "딸기라떼": 3700, "큐브라떼": 4200, "허니자몽블랙티": 3700, "감자빵": 3500},
    "설빙": {"인절미설빙": 9500, "애플망고치즈설빙": 13900, "초코브라우니설빙": 12900, "생딸기설빙": 15500, "인절미토스트": 4800},
    "미쉐": {"소프트아이스크림": 1000, "레몬에이드": 1500, "망고선데이": 2500, "브라운슈가펄밀크티": 3500, "복숭아얼그레이": 2500}
}

# 배달비 산정 기준
delivery_rules = [(50000, 0), (35000, 1000), (18000, 3000), (0, 4000)]

# [핵심 함수] 최소 비용 연산 로직
def calculate_total_cost(menu_dict, combo_list, coupon_amount):
    food_price = sum(menu_dict[item] for item in combo_list)
    delivery_fee = 4000
    for limit, fee in delivery_rules:
        if food_price >= limit:
            delivery_fee = fee
            break
    total_cost = food_price + delivery_fee - coupon_amount
    return total_cost, food_price, delivery_fee

# 2. 웹 UI 구성
st.set_page_config(page_title="배달비의 민족", layout="wide")
st.title("🛵 배달비 최소화 주문 조합 추천 시스템")
st.markdown(
    "<span style='color:gray'>성균관대학교 문제해결과컴퓨팅사고 - 러닝페어 2팀 (김나은, 여샘물, 왕예은, 정보미)</span>",
    unsafe_allow_html=True
)

with st.sidebar:
    st.header("⚙️ 주문 설정")
    selected_store = st.selectbox("🏬 가게 선택", list(store_menu_data.keys()))
    current_menus = store_menu_data[selected_store]
    
    # 수정된 입력 부분: step=1000으로 증감 조절, format="%d"로 콤마 가독성 확보
    budget = st.number_input("나의 총 예산 (원)", min_value=0, value=30000, step=1000, format="%d")
    min_order = st.number_input("가게 최소주문금액 (원)", min_value=0, value=16000, step=1000, format="%d")
    coupon = st.number_input("쿠폰 할인액 (원)", min_value=0, value=0, step=1000, format="%d")
    
    main_item = st.selectbox("꼭 먹고 싶은 메뉴", list(current_menus.keys()))

# 실행 버튼
if st.button("🚀 최적의 조합 계산하기"):
    items = list(current_menus.keys())
    best_cost = float('inf')
    best_result = None

    # 메뉴 조합 탐색 (1개~4개 조합)
    for i in range(1, 5): 
        for combo in itertools.combinations(items, i):
            if main_item not in combo: 
                continue

            total, food, d_fee = calculate_total_cost(current_menus, combo, coupon)

            # 조건 확인: 최소주문금액 이상이고 총 결제액이 예산 이내인 경우
            if food >= min_order and total <= budget:
                if total < best_cost:
                    best_cost = total
                    best_result = {
                        "조합": combo,
                        "음식값": food,
                        "배달비": d_fee,
                        "최종액": int(total)
                    }

    if best_result:
        st.markdown("---")
        st.success(f"🎯 [{selected_store}] 최적의 조합을 발견했습니다!")

        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.write("**[추천 메뉴 구성]**")
            for m in best_result['조합']:
                st.write(f"- {m} ({current_menus[m]:,}원)")
        with res_col2:
            st.metric("최종 결제 금액", f"{best_result['최종액']:,}원")
            st.caption(f"음식 {best_result['음식값']:,}원 + 배달비 {best_result['배달비']:,}원 - 쿠폰 {coupon:,}원")

        st.balloons()
    else:
        st.error("조건에 맞는 조합이 없습니다. 예산을 늘리거나 다른 메뉴를 선택해 보세요.")
