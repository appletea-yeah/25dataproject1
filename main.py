import pandas as pd
import streamlit as st
import plotly.express as px

# 파일 읽기
@st.cache_data
def load_data():
    df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding="euc-kr")
    df = df.copy()
    
    # 쉼표 제거 후 숫자로 변환
    for col in df.columns[1:]:
        df[col] = df[col].astype(str).str.replace(",", "").str.strip()
        df[col] = pd.to_numeric(df[col], errors="coerce")
    
    return df

df = load_data()

# Streamlit UI
st.title("2025년 5월 연령별 인구 시각화")
selected_region = st.selectbox("행정구역 선택", df["행정구역"].unique())

# 선택된 지역 필터링
region_df = df[df["행정구역"] == selected_region]

# 연령별 열만 선택 (0세 ~ 100세 이상)
age_cols = [col for col in df.columns if "계_" in col and "세" in col]
age_data = region_df[age_cols].T
age_data.columns = ["인구수"]
age_data["연령"] = age_data.index.str.extract(r"(\d+세|100세 이상)")
age_data.reset_index(drop=True, inplace=True)

# Plotly 시각화
fig = px.bar(age_data, x="연령", y="인구수", title=f"{selected_region} 연령별 인구 분포", labels={"연령": "연령", "인구수": "인구 수"})
fig.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig)
