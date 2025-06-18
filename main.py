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
regions = df["행정구역"].unique()
selected_region = st.selectbox("지역을 선택하세요", regions)

# 선택 지역 데이터 필터링
region_df = df[df["행정구역"] == selected_region]

# 연령 관련 컬럼만 추출
age_columns = [col for col in df.columns if "2025년05월_계_" in col and ("세" in col or "100세 이상" in col)]
age_labels = [col.replace("2025년05월_계_", "") for col in age_columns]

# 문자열 → 숫자 변환 (쉼표 제거 후)
population_strs = region_df[age_columns].iloc[0]
population_nums = population_strs.str.replace(",", "").astype(int)

# 시각화 (Plotly 인구 피라미드)
fig = go.Figure()

fig.add_trace(go.Bar(
    y=age_labels,
    x=-population_nums.values,
    name='전체 (남녀 합계)',  # 성별 데이터는 없으므로 총계로
    orientation='h',
    marker_color='mediumpurple'
))

fig.update_layout(
    title=f"{selected_region} 연령별 인구 구조",
    barmode='relative',
    xaxis=dict(title='인구 수', tickformat=','),
    yaxis=dict(title='연령'),
    height=700
)

st.plotly_chart(fig, use_container_width=True)
