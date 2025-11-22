# demo/streamlit_app.py
# Simple Streamlit demo to upload a CSV of reviews and show the mock classification results.
import streamlit as st
import pandas as pd
import subprocess, os, csv, tempfile
import os

st.title('GenAI Review Categorization — Demo (Mock Mode)')

uploaded = st.file_uploader('Upload reviews CSV (columns: customer_id, review)', type=['csv'])
if uploaded is not None:
    df = pd.read_csv(uploaded)
    st.write('Sample reviews:')
    st.dataframe(df.head())

    if st.button('Run mock classification'):
        tmp_in = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
        df.to_csv(tmp_in.name, index=False)
        tmp_out = os.path.join('results', 'streamlit_output.csv')
        RESULTS_DIR = "/mount/tmp/results"
        os.makedirs(RESULTS_DIR, exist_ok=True)
        # Call the script in mock mode
        subprocess.run(['python', 'scripts/run_classification.py', '--input', tmp_in.name, '--output', tmp_out, '--mode', 'mock'])
        out_df = pd.read_csv(tmp_out)
        st.write('Results:')
        st.dataframe(out_df)
        st.success('Done! Download results below.')
        st.download_button('Download results CSV', data=out_df.to_csv(index=False), file_name='genai_results.csv')
else:
    st.info('Upload a sample CSV to begin.')
