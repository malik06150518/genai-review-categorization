# Zero-shot prompt template

You are an AI model performing customer feedback analysis.

Return ONLY valid JSON.  
Do NOT include commentary, explanation, or markdown.

The JSON object MUST contain:
- customer_id
- sentiment
- tags
- priority
- action
- first_response

Classify the following review:

Customer ID: <CUSTOMER_ID>
Review: "<REVIEW_TEXT>"
