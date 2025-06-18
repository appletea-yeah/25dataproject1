import streamlit as st
import pandas as pd
import plotly.express as px

# 파일 업로드 or 로컬 실행 시 경로
FILE_PATH = "202505_202505_연령별인구현황_월간.csv"

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv(FILE_PATH, encoding="euc-kr", skiprows=1)
    df = df.rename(columns={df.columns[0]: "기준일자"})
    df["기준일자"] = pd.to_datetime(df["기준일자"], errors="coerce")
    df = df.dropna(subset=["기준일자"])
    return df

df = load_data()

# Streamlit UI
st.title("📊 연령별 인구현황 시각화")
st.markdown("업로드된 데이터를 바탕으로 연령대별 인구 변화를 시각화합니다.")

# 기준일자 선택
dates = df["기준일자"].dt.strftime("%Y-%m").unique()
selected_date = st.selectbox("기준월 선택", options=sorted(dates, reverse=True))

# 선택된 날짜의 데이터 필터링
filtered_df = df[df["기준일자"].dt.strftime("%Y-%m") == selected_date]

# 연령별 인구 컬럼 추출 (일반적으로 0~100세, 1살 단위)
age_columns = filtered_df.columns[1:]  # 첫 번째는 기준일자
population_strs = filtered_df.iloc[0, 1:]  # 해당 행에서 인구 수만 추출
population_nums = population_strs.str.replace(",", "").astype(int)

# 시각화를 위한 데이터프레임 생성
plot_df = pd.DataFrame({
    "연령": age_columns,
    "인구수": population_nums
})

# Plotly Bar Chart
fig = px.bar(plot_df, x="연령", y="인구수",
             labels={"연령": "연령", "인구수": "인구 수"},
             title=f"{selected_date} 기준 연령별 인구 분포")

st.plotly_chart(fig, use_container_width=True)
