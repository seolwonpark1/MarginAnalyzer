import streamlit as st
import pandas as pd

st.set_page_config(page_title="Margin Analyzer", layout="wide")

st.title("💰 Margin Analyzer")

uploaded_file = st.file_uploader("엑셀 파일 업로드 (브랜드명, 모델, 제품명, 공급가)", type=["xlsx"])

margin_threshold = st.number_input("마진율 기준 (%)", min_value=0, max_value=100, value=20)

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # '도매가' 또는 '공급가' 자동 인식
    cost_col = None
    for col in df.columns:
        if "공급가" in str(col) or "도매가" in str(col):
            cost_col = col
            break

    model_col = None
    for col in df.columns:
        if "MODEL" in str(col).upper():
            model_col = col
            break

    if cost_col and model_col:
        df[model_col] = df[model_col].astype(str).str.replace(" ", "").str.strip()
        df["비교가(가정)"] = df[cost_col] * 1.3
        df["마진율(%)"] = ((df["비교가(가정)"] - df[cost_col]) / df[cost_col] * 100).round(2)
        filtered_df = df[df["마진율(%)"] >= margin_threshold]
        st.subheader("업로드된 데이터")
        st.dataframe(df)
        st.subheader("💡 기준을 충족한 상품")
        st.dataframe(filtered_df)
    else:
        st.error("'공급가' 또는 '도매가', 'MODEL' 열이 필요합니다.")
