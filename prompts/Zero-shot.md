# Zero-shot prompt template

You are an analyst. For the following customer review, classify the sentiment as Positive, Neutral, or Negative. 
Tag the review for topics (choose from: food, quality, service, ambiance, price, overall). Assign a priority: High for Positive, Medium for Neutral, Low for Negative. 
Suggest one actionable next step for operations and write a first response message to the customer. 
Output as a single CSV row with columns: customer_id, sentiment, tags, priority, action, first_response.

Review: "<REVIEW_TEXT>"
