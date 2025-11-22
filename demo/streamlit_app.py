import streamlit as st
import pandas as pd
import os
from scripts.run_classification import mock_classify

# Streamlit Cloud: use writable temp directory
RESULTS_DIR = "/mount/tmp/results"
os.makedirs(RESULTS_DIR, exist_ok=True)

st.title("GenAI Review Classification Demo")

uploaded = st.file_uploader("Upload a CSV with columns: customer_id, review", type=["csv"])

if uploaded:
    df = pd.read_csv(uploaded)
    results = []

    for _, row in df.iterrows():
        results.append(mock_classify(row["customer_id"], row["review"]))

    st.success("Processing complete!")
    st.dataframe(pd.DataFrame(results))

    # Save results to temp folder
    output_path = os.path.join(RESULTS_DIR, "output.csv")
    pd.DataFrame(results).to_csv(output_path, index=False)

    st.write("Download processed results:")
    with open(output_path, "rb") as file:
        st.download_button(
            label="Download CSV",
            data=file,
            file_name="results.csv",
            mime="text/csv"
        )
