import streamlit as st
import pandas as pd
import re

# 페이지 설정
st.set_page_config(page_title="대전·세종·논산 스마트 맛집 내비게이션", page_icon="🚗")

st.title("🚗 대전·세종·논산 스마트 맛집 내비게이션")
st.write("차량 네비게이션처럼 상호명을 검색하면 연관 리스트가 실시간으로 나타납니다.")

# 데이터 로드
@st.cache_data
def load_data():
    return pd.read_csv('restaurant.csv', encoding='cp949', low_memory=False)

try:
    df = load_data()
    name_col = '업소명' if '업소명' in df.columns else '사업장명'
    address_col = '도로명주소' if '도로명주소' in df.columns else '지번주소'
    
    search = st.text_input("🔍 음식점 이름 검색 (예: 짬뽕, 대전, 논산)")
    
    if search:
        clean_search = re.sub(r'\s+', '', search)
        temp_names = df[name_col].astype(str).str.replace(r'\s+', '', regex=True)
        
        result = df[temp_names.str.contains(clean_search, case=False, na=False)]
        
        if not result.empty:
            st.success(f"총 **{len(result):,}개**의 음식점이 검색되었습니다.")
            
            # 리스트 생성
            display_list = [f"{row[name_col]} ({row.get(address_col, '주소없음')})" for _, row in result.iterrows()]
            selected_display = st.selectbox("📌 리스트에서 음식점을 선택하세요", display_list)
            
            # 선택된 데이터 추출
            selected_idx = display_list.index(selected_display)
            data = result.iloc[selected_idx]
            selected_name = data[name_col]
            address = data.get(address_col, '주소 정보 없음')
            
            st.markdown("---")
            st.subheader(f"📍 {selected_name} 상세 정보")
            
            # 주요 메뉴 및 위치 정보만 남김
            menu = data.get('업태구분명', '일반음식')
            st.markdown(f"**6. 주요 메뉴:** {menu}")
            st.markdown(f"**📍 위치(주소):** {address}")
            
            # 하단 버튼
            st.write("") # 간격 추가
            col1, col2 = st.columns(2)
            with col1:
                st.link_button("🚗 네이버 지도에서 위치 보기", f"https://m.search.naver.com/search.naver?query={selected_name}", use_container_width=True)
            with col2:
                st.link_button("🌐 웹에서 상세정보 검색", f"https://m.search.naver.com/search.naver?query={selected_name} 정보", use_container_width=True)
        else:
            st.warning("검색 결과가 없습니다.")
    else:
        st.info("💡 음식점 이름을 입력하시면 실시간으로 리스트가 나타납니다.")

except FileNotFoundError:
    st.error("데이터 파일(restaurant.csv)을 찾을 수 없습니다. 'reduce_data_d_s_n.py'를 먼저 실행했는지 확인해주세요.")