import streamlit as st
import pandas as pd
import plotly.express as px

# 파일 경로 (Streamlit Cloud 배포 시엔 경로만 유지)
FILE_PATH = "202505_202505_연령별인구현황_월간.csv"

@st.cache_data
def load_data():
    # CSV 불러오기
    df = pd.read_csv(FILE_PATH, encoding="euc-kr", skiprows=1)
    df = df.rename(columns={df.columns[0]: "기준일자"})
    df["기준일자"] = pd.to_datetime(df["기준일자"], errors="coerce")
    df = df.dropna(subset=["기준일자"])
    
    # 기준일자 월 단위로 추출
    df["기준월"] = df["기준일자"].dt.to_period("M").astype(str)
    return df

df = load_data()

# Streamlit UI
st.title("📊 연령별 인구현황 시각화")
st.markdown("CSV 데이터를 바탕으로 연령대별 인구 분포를 시각화합니다.")

# 기준월 선택
available_months = sorted(df["기준월"].unique(), reverse=True)
selected_month = st.selectbox("기준월 선택", available_months)

# 선택한 월에 해당하는 데이터 추출
filtered_df = df[df["기준월"] == selected_month]

# 데이터가 존재할 경우만 처리
if filtered_df.empty:
    st.error(f"선택한 {selected_month}에 해당하는 데이터가 존재하지 않습니다.")
else:
    # 인구 수 추출
    age_columns = filtered_df.columns[1:-2]  # 기준일자, 기준월 제외
    population_strs = filtered_df.iloc[0, 1:-2]  # 연령별 인구 문자열
    population_nums = population_strs.str.replace(",", "").astype(int)

    # 시각화용 데이터프레임 생성
    plot_df = pd.DataFrame({
        "연령": age_columns,
        "인구수": population_nums
    })

    # Plotly 그래프
    fig = px.bar(plot_df, x="연령", y="인구수",
                 labels={"연령": "연령", "인구수": "인구 수"},
                 title=f"{selected_month} 기준 연령별 인구 분포")
    st.plotly_chart(fig, use_container_width=True)
