# GenAI Review Categorization — Muhammad Ali Malik

This repository contains a GenAI demonstration that classifies and prioritizes customer reviews and generates first-response drafts and recommended next steps. It was built as the final project for the MIT No-Code AI program.

## What it does
- Classifies review sentiment (Positive / Neutral / Negative)
- Extracts topic tags (food, service, ambiance, price, quality)
- Assigns business priority (High / Medium / Low)
- Generates suggested actions and first-response drafts

# GenAI Review Classification Demo

🚀 [**Live Demo**](https://customerreviewtest.streamlit.app) - Try it now!
 -- **Download the CSV file from the data folder and use it for the live demo!!**


## Getting started
1. Clone the repo
2. Add a `data/reviews_sample.csv` file with columns: customer_id, review
3. Option A (No-code): Use LangChain Studio or Microsoft Copilot with the prompts in `/prompts`
4. Option B (Python): Set `OPENAI_API_KEY` and run `python scripts/run_classification.py --input data/reviews.csv --output results/output.csv`

## Files
- `prompts/` — prompt templates
- `scripts/` — API caller and post-processing scripts
- `demo/` — demo app (Streamlit or Gradio)
- `slides/` — PPT and demo script

## License
MIT

## Contact
Muhammad Ali Malik — ali.malik783@gmail.com|linkedin.com/in/muhammad-ali-malik-2698b859
