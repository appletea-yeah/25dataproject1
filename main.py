import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# CSV 파일 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv('202505_202505_연령별인구현황_월간.csv', encoding='cp949')
    return df

df = load_data()
df.columns = df.columns.str.strip()

st.title("📊 지역별 인구 구조 시각화")
st.markdown("대한민국 시군구별 연령별 인구구조 데이터를 기반으로 한 시각화 앱입니다.")

# 지역 선택
region_list = df['행정기관'].unique()
selected_region = st.selectbox("지역을 선택하세요", region_list)

# 선택된 지역의 데이터 필터링
region_df = df[df['행정기관'] == selected_region]

# 연령/성별 열 추출
age_cols = [col for col in df.columns if '세' in col]
male_cols = [col for col in age_cols if '남' in col]
female_cols = [col for col in age_cols if '여' in col]

male = region_df[male_cols].sum().values
female = region_df[female_cols].sum().values
age_labels = [col.split('세')[0] + '세' for col in male_cols]

# Plotly 인구 피라미드
fig = go.Figure()

fig.add_trace(go.Bar(
    y=age_labels,
    x=-male,
    name='남성',
    orientation='h',
    marker_color='skyblue'
))

fig.add_trace(go.Bar(
    y=age_labels,
    x=female,
    name='여성',
    orientation='h',
    marker_color='lightcoral'
))

fig.update_layout(
    title=f"{selected_region} 연령별 인구 피라미드 (2025년 5월)",
    barmode='relative',
    xaxis=dict(title='인구 수', tickformat=','),
    yaxis=dict(title='연령대'),
    bargap=0.05,
    height=600
)

st.plotly_chart(fig, use_container_width=True)
