from google import genai
from dotenv import load_dotenv
import os
import json
import time


load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Get the fucking API Key, STUPID!")
print("✅ API Key Detected.")

json_file_path = "output/reddit_2026-05-19T17-30-21+00-00.json"

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    filtered_data = [
        {"title": item.get("title"), "subreddit": item.get("subreddit")} 
        for item in data
    ]
    print(f"✅ Loaded and filtered {len(filtered_data)} entries from {json_file_path}")

except FileNotFoundError:
    print(f"❌ Error: File not found at {json_file_path}")
    exit(1)
except json.JSONDecodeError:
    print(f"❌ Error: Failed to decode JSON from {json_file_path}")
    exit(1)

# Gemini Client
client = genai.Client(api_key=api_key)

def generate_with_retry(prompt, model="gemini-3.1-flash-lite", max_retries=3):
    """Helper to handle 429 Rate Limit errors with exponential backoff."""
    for attempt in range(max_retries):
        try:
            return client.models.generate_content(model=model, contents=prompt)
        except Exception as e:
            if "429" in str(e) and attempt < max_retries - 1:
                wait_time = (attempt + 1) * 15
                print(f"⚠️ Rate limit hit. Retrying in {wait_time}s... (Attempt {attempt+1}/{max_retries})")
                time.sleep(wait_time)
            else:
                raise e

# Chunking, FUCK RATE LIMITS
CHUNK_SIZE = 50
chunks = [filtered_data[i:i + CHUNK_SIZE] for i in range(0, len(filtered_data), CHUNK_SIZE)]
chunk_summaries = []

print(f"🚀 Processing {len(chunks)} chunks of data using { 'gemini-3.1-flash-lite' }...")

for i, chunk in enumerate(chunks):
    chunk_str = json.dumps(chunk, indent=2)
    prompt = f"Summarize the key trends and topics in these Reddit posts:\n\n{chunk_str}"
    
    try:
        response = generate_with_retry(prompt)
        chunk_summaries.append(response.text)
        print(f"✅ Processed chunk {i+1}/{len(chunks)}")
        # Small sleep to avoid hitting RPM LIMITS
        time.sleep(2) 
    except Exception as e:
        print(f"❌ Error processing chunk {i+1}: {e}")
        break

if chunk_summaries:
    print("\n🚀 Generating final synthesis...")
    final_prompt = f"""
    The following are summaries of several chunks of Reddit data regarding Machine Learning.
    Please synthesize these into one final, comprehensive report highlighting:
    1. Major Trends
    2. Recurring Themes
    3. Community Sentiment
    
    Summaries:
    {"\n\n".join(chunk_summaries)}
    """
    
    try:
        final_response = generate_with_retry(final_prompt)
        print("\n--- Gemini Final Insights ---\n")
        print(final_response.text)
        print("\n----------------------------")
    except Exception as e:
        print(f"❌ Error generating final synthesis: {e}")
else:
    print("❌ No summaries were generated. Check API quota/errors.")
