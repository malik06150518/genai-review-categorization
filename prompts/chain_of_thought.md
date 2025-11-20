# Chain-of-Thought prompt template

Step 1: Read the review and identify phrases indicating sentiment.
Step 2: Determine topics touched (food, service, etc.).
Step 3: Assign sentiment label and priority.
Step 4: Propose an action and draft a first-response.
Output a JSON object with keys: customer_id, sentiment, tags, priority, action, first_response.

Review: "<REVIEW_TEXT>"
