import os
import sys
import streamlit as st
import pandas as pd

# Ensure repo root is on the import path (works on Streamlit Cloud)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Writable dir for Streamlit Cloud
RESULTS_DIR = "/mount/tmp/results"
os.makedirs(RESULTS_DIR, exist_ok=True)

# Try to import the mock classifier from scripts
try:
    from scripts.run_classification import mock_classify
except Exception as e:
    st.error(
        "Import error: could not import scripts.run_classification.\n\n"
        "Make sure `scripts/run_classification.py` exists and the file and folder names are correct (no .rtf or colon ':' in names)."
    )
    st.write("Detailed error:")
    st.exception(e)
    # Stop further execution
    st.stop()

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

    with open(output_path, "rb") as file:
        st.download_button(
            label="Download CSV",
            data=file,
            file_name="results.csv",
            mime="text/csv"
        )
