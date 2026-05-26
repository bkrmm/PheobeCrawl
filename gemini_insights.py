from google import genai
from dotenv import load_dotenv
import os
import json
import time
import glob


load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Get the fucking API Key, STUPID!")
print("✅ API Key Detected.")

# Find all JSON files in the output directory
json_files = glob.glob("output/*.json")
if not json_files:
    print("❌ Error: No JSON files found in output directory")
    exit(1)

all_data = []
for file_path in json_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # Identify source based on filename
            source = "reddit" if "reddit" in file_path.lower() else "hackernews" if "hackernews" in file_path.lower() else "unknown"
            
            for item in data:
                # Handle different data structures
                if item.get("type") == "post":
                    all_data.append({
                        "source": source,
                        "type": "post",
                        "title": item.get("title"),
                        "context": item.get("subreddit") or item.get("url")
                    })
                elif "comment_text" in item:
                    all_data.append({
                        "source": source,
                        "type": "comment",
                        "text": item.get("comment_text"),
                        "post_title": item.get("post_title")
                    })
                # Fallback for old reddit format in the original script
                elif "title" in item and "subreddit" in item:
                    all_data.append({
                        "source": source,
                        "type": "post",
                        "title": item.get("title"),
                        "context": item.get("subreddit")
                    })

        print(f"✅ Loaded data from {file_path}")
    except Exception as e:
        print(f"❌ Error loading {file_path}: {e}")

if not all_data:
    print("❌ No valid data extracted from JSON files.")
    exit(1)

print(f"✅ Total entries collected: {len(all_data)}")

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
chunks = [all_data[i:i + CHUNK_SIZE] for i in range(0, len(all_data), CHUNK_SIZE)]
chunk_summaries = []

print(f"🚀 Processing {len(chunks)} chunks of data using { 'gemini-3.1-flash-lite' }...")

for i, chunk in enumerate(chunks):
    chunk_str = json.dumps(chunk, indent=2)
    prompt = f"Summarize the key trends, topics, and discussions in these posts and comments from Reddit and Hacker News:\n\n{chunk_str}"
    
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
    The following are summaries of several chunks of data from Reddit and Hacker News regarding technology and Machine Learning.
    Please synthesize these into one final, comprehensive report highlighting:
    1. Major Trends
    2. Recurring Themes across different platforms
    3. Community Sentiment (comparing Reddit vs Hacker News if applicable)
    
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
