import streamlit as st
import pandas as pd
import os
from scripts.run_classification import mock_classify

st.title("GenAI Review Classification Demo")

uploaded = st.file_uploader("Upload a CSV with columns: customer_id, review", type=["csv"])

if uploaded:
    df = pd.read_csv(uploaded)
    results = []

    for _, row in df.iterrows():
        results.append(mock_classify(row["customer_id"], row["review"]))

    st.success("Processing complete!")
    st.dataframe(pd.DataFrame(results))
