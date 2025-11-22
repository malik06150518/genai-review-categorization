import os
import sys
import streamlit as st
import pandas as pd
import tempfile

# Ensure repo root is on the import path (works on Streamlit Cloud)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Use Python's tempfile for Streamlit Cloud compatibility
RESULTS_DIR = tempfile.mkdtemp()

# Try to import the mock classifier from scripts
try:
    from scripts.run_classification import mock_classify, run_mock, run_openai
except Exception as e:
    st.error(
        "Import error: could not import scripts.run_classification.\n\n"
        "Make sure `scripts/run_classification.py` exists and the file and folder names are correct (no .rtf or colon ':' in names)."
    )
    st.write("Detailed error:")
    st.exception(e)
    st.stop()

st.title("GenAI Review Classification Demo")

st.markdown(
    "Upload a CSV with columns: **customer_id, review**. Default mode is **mock** (no API keys required)."
)

mode = st.radio("Mode:", ["mock", "openai"], index=0, help="Choose mock for offline demo, openai to call real API (requires key).")

uploaded = st.file_uploader("Upload CSV", type=["csv"])

if uploaded:
    try:
        df = pd.read_csv(uploaded)
    except Exception as e:
        st.error("Could not read uploaded CSV. Ensure it has columns: customer_id, review.")
        st.exception(e)
        st.stop()

    st.write("Sample input:")
    st.dataframe(df.head())

    if st.button("Run classification"):
        st.info(f"Running in **{mode}** mode. This may take a moment.")
        results = []

        if mode == "mock":
            for _, row in df.iterrows():
                results.append(mock_classify(row.get("customer_id", ""), row.get("review", "")))
        else:
            # OpenAI mode — will attempt to run run_openai on the uploaded file.
            # This expects OPENAI_API_KEY available in environment/st.secrets
            tmp_in = os.path.join(RESULTS_DIR, "tmp_input.csv")
            df.to_csv(tmp_in, index=False)
            tmp_out = os.path.join(RESULTS_DIR, "tmp_output.csv")
            try:
                # run_openai writes output CSV (may raise if key missing)
                run_openai(tmp_in, tmp_out)
                results = pd.read_csv(tmp_out).to_dict(orient="records")
            except Exception as e:
                st.error("OpenAI run failed. Make sure OPENAI_API_KEY is configured in your environment / Streamlit secrets.")
                st.exception(e)
                st.stop()

        results_df = pd.DataFrame(results)
        st.success("Processing complete!")
        st.dataframe(results_df)

        # Provide download directly from dataframe (no need to save to disk first)
        csv = results_df.to_csv(index=False)
        st.download_button(
            "Download results CSV", 
            data=csv, 
            file_name="genai_results.csv", 
            mime="text/csv"
        )
else:
    st.info("Upload a CSV to begin.")