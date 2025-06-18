import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding="cp949")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

st.title("📊 대한민국 지역별 인구 피라미드 (2025년 5월 기준)")

# 지역 선택
regions = df["행정구역"].dropna().unique()
selected_region = st.selectbox("지역을 선택하세요", regions)

# 선택 지역 데이터 필터링
region_df = df[df["행정구역"] == selected_region]

# 연령 관련 컬럼만 추출
age_columns = [col for col in df.columns if "2025년05월_계_" in col and ("세" in col or "100세 이상" in col)]
age_labels = [col.replace("2025년05월_계_", "") for col in age_columns]

# 값 가져오기
population_strs = region_df[age_columns].iloc[0]

# 쉼표 제거 + 숫자 변환 + 결측값은 0 처
