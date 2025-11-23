# scripts/run_classification.py
"""Improved script to call an LLM to classify reviews.
Supports mock mode for offline testing and an OpenAI mode that attempts to parse JSON responses robustly.
"""
import os, csv, argparse, json, time, re
from pathlib import Path

PROMPT_TEMPLATE = Path(__file__).parent.parent.joinpath('prompts','Zero-shot.md').read_text(encoding='utf-8')

def mock_process(review_id, review_text):
    lower = review_text.lower()
    if any(w in lower for w in ['amazing', 'great', 'loved', 'enjoyed']):
        sentiment = 'Positive'; priority = 'High'
        tags = ['food'] if any(x in lower for x in ['pasta','dessert','food','pizza','burger']) else ['overall']
        action = 'Acknowledge and promote the praised item.'
        first_response = 'Thank you — we\'re glad you enjoyed your experience!'
    elif any(w in lower for w in ['cold', 'incorrect', 'not', "didn't", 'bad', 'poor','Terrible']):
        sentiment = 'Negative'; priority = 'Low'
        tags = ['food','service']
        action = 'Investigate and correct the issue; follow up with customer.'
        first_response = 'We\'re sorry to hear this. Please contact us so we can make it right.'
    else:
        sentiment = 'Neutral'; priority = 'Medium'
        tags = ['overall']
        action = 'Monitor and gather more data.'
        first_response = 'Thank you for your feedback — we will use it to improve.'
    return {
        'customer_id': review_id,
        'sentiment': sentiment,
        'tags': ';'.join(tags),
        'priority': priority,
        'action': action,
        'first_response': first_response
    }

def parse_json_from_text(text):
    """Attempt to extract a JSON object from model text output."""
    # Try to find first { ... } block
    m = re.search(r'{.*}', text, flags=re.DOTALL)
    if m:
        s = m.group(0)
        try:
            return json.loads(s)
        except Exception:
            # try to fix simple JSON issues: replace single quotes, trailing commas
            s2 = s.replace("'", '"')
            s2 = re.sub(r',\s*}', '}', s2)
            s2 = re.sub(r',\s*\]', ']', s2)
            try:
                return json.loads(s2)
            except Exception:
                return None
    # Try CSV-like row: split by commas into known fields length
    return None

def run_mock(input_csv, output_csv):
    import csv
    with open(input_csv, newline='', encoding='utf-8') as fin, open(output_csv, 'w', newline='', encoding='utf-8') as fout:
        reader = csv.DictReader(fin)
        fieldnames = ['customer_id','sentiment','tags','priority','action','first_response']
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()
        for r in reader:
            out = mock_process(r['customer_id'], r['review'])
            writer.writerow(out)

def run_openai(input_csv, output_csv):
    try:
        import openai
    except Exception as e:
        print('openai package not installed. Install with: pip install openai')
        return
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        print('OPENAI_API_KEY not set. Exiting.')
        return
    openai.api_key = api_key
    with open(input_csv, newline='', encoding='utf-8') as fin, open(output_csv, 'w', newline='', encoding='utf-8') as fout:
        reader = csv.DictReader(fin)
        fieldnames = ['customer_id','sentiment','tags','priority','action','first_response','raw_response']
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()
        for r in reader:
            prompt = PROMPT_TEMPLATE.replace('<REVIEW_TEXT>', r['review']).replace('<CUSTOMER_ID>', r['customer_id'])
            # Use chat completion endpoint; model choice can be adjusted
            try:
                resp = openai.ChatCompletion.create(model='gpt-4o-mini', messages=[{'role':'user','content':prompt}], temperature=0.2)
                text = resp['choices'][0]['message']['content']
            except Exception as e:
                print('OpenAI API call failed:', e)
                text = ''

            parsed = parse_json_from_text(text)
            if parsed:
                # Ensure expected keys exist, fill defaults otherwise
                row = {
                    'customer_id': parsed.get('customer_id', r['customer_id']),
                    'sentiment': parsed.get('sentiment', ''),
                    'tags': ';'.join(parsed.get('tags')) if isinstance(parsed.get('tags'), list) else parsed.get('tags',''),
                    'priority': parsed.get('priority',''),
                    'action': parsed.get('action',''),
                    'first_response': parsed.get('first_response',''),
                    'raw_response': text.replace('\n',' ')[:1000]
                }
            else:
                # Fallback: write raw response into action column for manual review
                row = {
                    'customer_id': r['customer_id'],
                    'sentiment': '',
                    'tags': '',
                    'priority': '',
                    'action': text.replace('\n',' ')[:1000],
                    'first_response': '',
                    'raw_response': text.replace('\n',' ')[:1000]
                }
            writer.writerow(row)
            time.sleep(1)  # safety
    print('OpenAI run complete. Output:', output_csv)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--mode', choices=['mock','openai'], default='mock')
    args = parser.parse_args()
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    if args.mode == 'mock':
        run_mock(args.input, args.output)
        print('Mock run complete. Output:', args.output)
    else:
        run_openai(args.input, args.output)

if __name__ == '__main__':
    main()

