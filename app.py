import streamlit as st
import itertools

# 1. 가게별 데이터베이스 (문법 오류 수정 및 데이터 정제)
store_db = {
    '치킨': {
        '교촌치킨': {
            'menu': {'허니콤보': 26000, '허니순살': 25000, '반반순살(레드+허니)': 25000, '반반한마리(간장+허니갈릭)':24000,'후라이드한마리': 23000, 
                     '양념치킨한마리': 24000, '허니옥수수순살': 25000, '간장콤보': 25000, '간장순살': 24000, '레드콤보': 20000, '레드순살': 25000,
                     '살살후라이드': 22000, '허니치룽지': 5000, '레드치룽지': 5000, '웨지감자': 4000, '칩카사바': 2000, '펩시 1.25L': 3000},
            'min_order': 21000,
            'delivery_logic': lambda p: 0, 
            'notice': '💡 21,000원 이상 주문 시 무료배달'
        },
        'BHC': {
            'menu': {'뿌링클': 23000, '맛초킹': 23000, '콰삭킹': 24000, '스윗칠리킹': 24000, '후라이드': 22000, '후라이드/양념 반반치킨': 23000,
                     '양념치킨': 24000, '더블팝순살 후라이드': 25000, '더블팝순살 양념': 26000, '레드킹': 24000, '뿌링빅콜팝': 15000, '빅콜팝': 12500,
                     '카이막치즈볼': 6000, '콰삭 슈림프': 9000, '뿌링감자': 5000, '분모자 로제 떡볶이': 6000, '뿌링소떡': 4000, '코카콜라 1.25L': 2500},
            'min_order': 18000,
            'delivery_logic': lambda p: 0, 
            'notice': '💡 18,000원 이상 주문 시 무료배달'
        },
        'BBQ': {
            'menu': {'황금올리브치킨': 23000, '황올 반+양념 반': 24000, '황금올리브치킨 핫크리스피': 24000, '바사킨 윙': 23000, '크런치버터치킨': 24000, 
                     '땡쇼크': 25000, '맵소디': 24500, '빠리치킨': 24000, '자메이카 통다리구이': 24000, '자메이카 소떡만나치킨': 24000, '스모크치킨': 22000,
                     '뿜치킹': 25000, 'BBQ떡볶이': 7000, 'BBQ맛탕': 4000, 'BBQ고추킹': 9000, 'BBQ소떡': 3500, '스파클링 레몬보이 245ml': 1000',
                     '스프라이트 1.5L': 3000, '코카콜라 1.25L': 3000, '제로콜라 1.25L': 3000},
            'min_order': 18000,
            'delivery_logic': lambda p: 0, 
            'notice': '💡 18,000원 이상 주문 시 무료배달'
        },
        '지코바 숯불치킨': {
            'menu': {'지코바 뼈 양념구이': 23500, '지코나 순살양념치킨': 23500, '순살소금구이': 22500, '순살양념반.소금반': 26500, '지코바 뼈 소금구이': 22500,
                    '순살양념치밥 셋트': 28000, '흑미밥': 2000, '콘샐러드': 2000, '치킨무 추가': 500, '메추리알 토핑 10개': 2000, '코카콜라 500ML': 2000},
            'min_order': 8000,
            'delivery_logic': lambda p: 0, 
            'notice': '💡 8,000원 이상 주문 시 무료배달'
        },
        '푸라닭': {
            'menu': {'고추마요치킨': 22900, '블랙알리오': 22900, '콘소메이징': 22900, '씬후라이드': 20900, '달콤양념치킨': 22900, '마불로악마': 23900,
                    '매드갈릭치킨': 22900, '블랙마요': 24400, '일품깐풍': 23900, '나폴리투움바': 23900, '블랙투움바': 25400, '블랙치즈볼(5구)': 4900,
                    '크림치즈볼(5구)': 4900, '베이컨감자볼(5구)': 4900, '후라잉닭발': 15900, '코카콜라 500ML': 2000, '제로콜라 500ML': 2000, '스프라이트 500ML': 2000},
            'min_order': 18900,
            'delivery_logic': lambda p: 0, 
            'notice': '💡 18,900원 이상 주문 시 무료배달'
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
            'menu': {'신전떡볶이': 4000, '로제떡볶이': 6000, '치즈떡볶이': 6000, '마라로제떡볶이': 7000, 
              '신전김밥': 3000, '신전치즈김밥': 4000, '참치마요컵밥': 4000, '스팸마요컵밥': 4000, '치킨마요컵밥': 4500,
              '튀김오뎅(5개)': 1700, '잡채말이(3개)': 1700, '납작만두(5개)': 2000, '통살오징어(3개)': 2900, '순대': 4000,
              '쥬시쿨':2000, '콜라': 2000, '사이다': 2000, '삶은계란(2ea)': 1500},
            'min_order': 14000,
            'delivery_logic': lambda p: 0, 
            'notice': '💡 14,000원 이상 무료배달'
        },
        '배떡 로제떡볶이': {
            'menu': {'로제떡볶이': 11000, '새우크림 떡볶이': 13000, '마라로제 떡볶이': 15000, '분모자떡볶이': 12000, 
                     '국물 떡볶이': 6000, '짜장 떡볶이': 6000, '순살후라이드치킨': 9500, '양념순살치킨': 10500, '간장순살치킨': 10500,
                     '튀김세트A': 7000, '튀김세트B': 7000, '배떡 오리지널 타코야키': 5000, '배떡 매콤칠리 타코야끼': 5500,
                     '김가루밥': 3500, '날치알밥': 5500, '미니어묵탕':7000, '쿨피스 930ml': 2000, '칠성사이다500ml': 2000, '펩시콜라500ml': 2000},
            'min_order': 14000,
            'delivery_logic': lambda p: 0, 
            'notice': '💡 14,000원 이상 무료배달'
        },
        '동대문엽기떡볶이': {
            'menu': {'엽기메뉴': 14000, '로제메뉴': 16000, '마라떡볶이': 16000, '마라로제떡볶이':18000, '엽기닭볶음탕': 24000, 
                     '숯불통뼈닭발': 15000, '숯불무뼈닭발': 16000, '국물통뼈닭발':16000, '국물무뼈닭발':17000, '참치마요밥': 3500, 
                     '주먹김밥(셀프)': 2000, '계란찜':2000, '계란야채죽': 5000, '순대': 3000,'모둠튀김': 2000, '김말이(3개)': 2000, 
                     '바삭치즈만두(7개)': 2000, '엽도그(1개)': 2000, '음료(유산균)450ml': 1000, '펩시 355ml': 2000},
            'min_order': 14000,
            'delivery_logic': lambda p: 0, 
            'notice': '💡 14,000원 이상 무료배달'
        },
        '청년다방': {
            'menu': {'떡튀순떡볶이': 18500, '불향차돌떡볶이': 20000, '통큰오짱떡볶이': 20000, '마라로제떡볶이': 20000, '로제떡볶이': 20000,
                     '차세대떡볶이': 24500, '경양식돈가스': 10000, '통통순살치킨': 13000, '허니간장순살치킨': 14000, '모듬튀김': 8000, 
                     '버터갈릭감자튀김': 6000, '핫버터갈릭 옥수수튀김': 6000, '치킨마요컵밥': 4500, '날치알볶음밥': 3000, '튀김만두(1개)': 500,
                     '야채튀김(1개)': 1000, '고구마튀김(1개)': 1000, '통큰에이드': 5500, '쿨다방': 2000, '미수까루': 3500, '콜라 355ml': 2000, '사이다 355ml': 2000},
            'min_order': 15000,
            'delivery_logic': lambda p: 0, 
            'notice': '💡 15,000원 이상 무료배달'
        },
        '우리할매떡볶이': {
            'menu': {'가래떡떡볶이': 5500, '밀떡볶이': 5500, '할매로제떡볶이': 6500, '할매로제가래떡떡볶이': 6500, '마라떡볶이': 7500, '마라로제떡볶이': 8500,
                    '옛날짜장떡볶이': 5500, '순대': 5500, '꼬치어묵': 3500, '매운꼬치어묵': 4000, '셀프주먹밥': 4000,
                    '국물비빔밥': 4000, '통오징어 튀김': 8500, '가래떡꼬치': 3000, '곰돌이돈까스': 1500, '한그릇 맛감자': 4500,
                    '치즈볼': 4000, '새우튀김': 2000, '고구마튀김': 1500, '핫도그': 2000, '콜라 500ml': 2000, '사이다 500ml':2000},
            'min_order': 12000,
            'delivery_logic': lambda p: 0, 
            'notice': '💡 12,000원 이상 무료배달'}
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
