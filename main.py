import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 한글 폰트 설정 (윈도우 기준)
plt.rcParams['font.family'] = 'Malgun Gothic'

# CSV 파일 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv('202505_202505_연령별인구현황_월간.csv', encoding='cp949')
    return df

df = load_data()

# 데이터 확인
st.title("지역별 인구 구조 시각화")
st.markdown("대한민국 시군구별 연령별 인구구조 데이터를 기반으로 한 시각화 앱입니다.")

# 컬럼명 정리
df.columns = df.columns.str.strip()

# 지역 선택
region_list = df['행정기관'].unique()
selected_region = st.selectbox("지역을 선택하세요", region_list)

# 선택된 지역의 데이터 필터링
region_df = df[df['행정기관'] == selected_region]

# 연령/성별 데이터 추출
age_cols = [col for col in df.columns if '세' in col]
population_by_age = region_df[age_cols].sum()

# 남녀 데이터 분리 (열 이름에 따라 다를 수 있음)
male = population_by_age[[col for col in age_cols if '남' in col]]
female = population_by_age[[col for col in age_cols if '여' in col]]

# 연령대 추출
age_labels = [label.split('.')[0] for label in male.index]

# 그래프 그리기
fig, ax = plt.subplots(figsize=(10, 6))

ax.barh(age_labels, -male.values, label='남성', color='skyblue')
ax.barh(age_labels, female.values, label='여성', color='lightcoral')
ax.set_xlabel('인구 수')
ax.set_title(f"{selected_region} 연령별 인구 피라미드")
ax.legend()
ax.set_yticks(range(len(age_labels)))
ax.set_yticklabels(age_labels)
ax.invert_yaxis()  # 연령이 낮은 순서부터 위로

st.pyplot(fig)
