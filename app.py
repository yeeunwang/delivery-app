import streamlit as st
import itertools

# 1. 가게별 데이터베이스 (문법 오류 수정 및 데이터 정제)
store_db = {
    '치킨': {
        '교촌치킨': {
            'menu': {'허니콤보': 23000, '간장콤보': 20000, '레드콤보': 20000, '웨지감자': 4000, '칩카사바': 2000, '코카콜라 1.25L': 3200},
            'min_order': 17000,
            'delivery_logic': lambda p: 0, 
            'notice': '💡 17,000원 이상 주문 시 무료배달'
        },
        'BHC': {
            'menu': {'뿌링클': 21000, '맛초킹': 21000, '콰삭킹': 20000, '달콤바삭치즈볼': 5000, '뿌링소떡': 3500, '코카콜라 1.25L': 2500},
            'min_order': 20000,
            'delivery_logic': lambda p: 0, 
            'notice': '💡 20,000원 이상 주문 시 무료배달'
        }
    },
    '피자': {
        '도미노피자': {
            'menu': {'블랙타이거 슈림프 L': 36900, '포테이토 L': 27900, '리얼불고기 L': 29900, '하트 포테이토': 5400, 'NEW 치즈 볼로네즈 스파게티': 9800, '코카콜라 1.25L': 2500},
            'min_order': 16900,
            'delivery_logic': lambda p: 0, 
            'notice': '💡 16,900원 이상 무료배달'
        },
        '청년피자': {
            'menu': {'리얼치즈 R': 16900, '하와이안 R': 17900, '슈퍼슈프림 R': 18900, '알리오올리오파스타': 6500, '페퍼로니 치즈 김치볶음밥': 5900, '코카콜라 1.25L': 2700},
            'min_order': 18900,
            'delivery_logic': lambda p: 0, 
            'notice': '💡 18,900원 이상 무료배달'
        },
        '노모어피자': {
            'menu': {'옥수수새우피자 R': 23800, '페퍼로니피자 R': 19800, '스윗고구마피자 R': 21800, '치즈오븐김치볶음밥': 8900, '옥수수바질치즈크림뇨끼': 8800, '코카콜라 1.25L': 2800},
            'min_order': 18000,
            'delivery_logic': lambda p: 0, 
            'notice': '💡 18,000원 이상 무료배달'
        }
    },
    '떡볶이': {
        '신전떡볶이': {
            'menu': {'신전떡볶이': 4000, '마라로제떡볶이': 7000, '모둠튀김': 4500, '신전치즈김밥': 4000, '스팸마요컵밥': 4000, '쥬시쿨': 2000},
            'min_order': 14000,
            'delivery_logic': lambda p: 0, 
            'notice': '💡 14,000원 이상 무료배달'
        },
        '배떡 로제떡볶이': {
            'menu': {'로제떡볶이': 11000, '새우크림 떡볶이': 13000, '국물 떡볶이': 6000, '튀김세트A': 7000, '오리지널 타코야키': 5000, '쿨피스 930ml': 2000},
            'min_order': 14000,
            'delivery_logic': lambda p: 0, 
            'notice': '💡 14,000원 이상 무료배달'
        },
        '동대문엽기떡볶이': {
            'menu': {'엽기메뉴': 14000, '마라떡볶이': 16000, '엽기닭볶음탕': 24000, '숯불무뼈닭발': 16000, '참치마요밥': 3500, '펩시 355ml': 2000},
            'min_order': 14000,
            'delivery_logic': lambda p: 0, 
            'notice': '💡 14,000원 이상 무료배달'
        }
    }
}

# [핵심] 최적 조합 계산 함수
def find_best_combo(menu_dict, delivery_logic, must_have, budget, min_order):
    all_menus = list(menu_dict.keys())
    best_res = None
    min_total = float('inf')

    # 조합 탐색 (1~5개 조합)
    for i in range(1, 6):
        for combo in itertools.combinations(all_menus, i):
            if not set(must_have).issubset(combo):
                continue
            
            food_total = sum(menu_dict[m] for m in combo)
            
            if food_total < min_order:
                continue
                
            current_delivery_fee = delivery_logic(food_total)
            final_price = food_total + current_delivery_fee
            
            if final_price <= budget and final_price < min_total:
                min_total = final_price
                best_res = {
                    'items': combo,
                    'food_price': food_total,
                    'delivery_fee': current_delivery_fee,
                    'total': final_price
                }
    return best_res

# --- Streamlit UI 시작 ---
st.set_page_config(page_title="배달비 최적화 시스템", layout="wide")
st.title("🛵 배달비 최적화 주문 시스템")
st.markdown("가게별로 다른 **배달비 규칙**을 분석하여 예산 안에서 가장 저렴한 조합을 찾아드립니다.")

category = st.selectbox("1️⃣ 어떤 종류의 음식을 드실 건가요?", list(store_db.keys()))
brand = st.selectbox(f"2️⃣ {category} 브랜드 중 하나를 골라주세요.", list(store_db[category].keys()))
target_store = store_db[category][brand]

st.divider()

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("💰 예산 및 필수 메뉴")
    user_budget = st.number_input("나의 총 예산 (원)", min_value=0, value=30000, step=1000)
    st.info(f"📍 {brand} 최소 주문금액: {target_store['min_order']:,}원")
    must_items = st.multiselect("꼭 먹고 싶은 메뉴를 선택하세요 (필수)", list(target_store['menu'].keys()))

with col2:
    st.subheader("📌 배달비 정책 정보")
    st.warning(target_store['notice'])
    with st.expander("전체 메뉴 가격 보기"):
        for m, p in target_store['menu'].items():
            st.write(f"- {m}: {p:,}원")

if st.button("🚀 최적의 조합 계산하기"):
    with st.spinner('계산 중...'):
        result = find_best_combo(
            target_store['menu'], 
            target_store['delivery_logic'], 
            must_items, 
            user_budget, 
            target_store['min_order']
        )
    
    if result:
        st.balloons()
        st.success(f"🎯 [{brand}] 추천 조합을 찾았습니다!")
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.write("### 🍱 추천 메뉴 구성")
            for item in result['items']:
                price = target_store['menu'][item]
                st.write(f"- **{item}**: {price:,}원")
        with res_col2:
            st.write("### 💸 결제 상세")
            st.metric("최종 결제 금액", f"{int(result['total']):,}원")
            st.write(f"음식 합계: {int(result['food_price']):,}원")
            st.write(f"배달비: {int(result['delivery_fee']):,}원")
            st.caption(f"안내: {target_store['notice']}")
    else:
        st.error("조건을 만족하는 조합이 없습니다. 예산을 높이거나 메뉴를 조정해 주세요.")
