# PheobeCrawl: A Personal Insight Agent

A specialized set of Scrapy spiders designed to extract multiple websites from Machine Learning and AI Academic Infrastructure, coupled with a Google Gemini integration to synthesize trends, themes, and community sentiment.

## Repository Structure

```text
bkrmm-pheobecrawl/
├── README.md                 # Project documentation
├── insights.py               # Script to analyze scraped JSON data using Google Gemini
├── scrapy.cfg                # Scrapy project configuration
└── PheobeCrawl/              # Main Scrapy project package
    ├── __init__.py
    ├── items.py              # Data models (currently using dict yields)
    ├── middlewares.py        # Custom middleware (default scaffolding)
    ├── pipelines.py          # Item processing pipelines (default scaffolding)
    ├── settings.py           # Global Scrapy settings (Feed exports, throttling)
    └── spiders/
        ├── __init__.py
        └── reddit.py         # The core reddit spider: scrapes r/MachineLearning & r/ArtificialInteligence
```

## Features:

    Targeted Scraping: Extracts top weekly posts from r/MachineLearning and r/ArtificialInteligence via old.reddit.com.
    Deep Data Collection: Captures post metadata (title, score, URL) and recursively scrapes top-level comments.
    AI Synthesis: Uses gemini_insights.py to chunk large datasets, summarize trends, and generate a final comprehensive report on community sentiment.
    Rate Limit Protection: Includes exponential backoff retry logic in the Gemini script and respectful download delays in Scrapy settings.

## Prerequisites:

    Python 3.8+
    Scrapy
    Google Generative AI SDK
     (google-genai)
    A valid Google API Key

⚙️ Installation & Setup

    Clone the repository:

```bash
    git clone https://github.com/bkrmm/PheobeCrawl.git
    cd pheobecrawl
```

    Install dependencies:

```bash
    python -m pip install scrapy google-genai python-dotenv
```

    Configure Environment:
    Create a .env file in the root directory and add your API key:

```bash
    GOOGLE_API_KEY = "your_actual_api_key_here"
  ```


## Usage
Step 1: Run the Spider
Execute the Scrapy spider to gather data. Results are automatically saved to the output/ directory as JSON.

```bash
python gemini_insights.py
```

Step 2: Generate Insights
Run the Gemini analysis script on the generated JSON file. 
Note: Ensure the json_file_path in gemini_insights.py matches your latest output file if not using the default timestamp.


```bash
python gemini_insights.py
```

## Configuration Highlights

    Output Format: JSON files are saved in output/reddit_<timestamp>.json.
    Throttling: 
        Scrapy: DOWNLOAD_DELAY = 1s (global), 3s (spider-specific).
        Gemini: Automatic retry with exponential backoff on 429 errors.
    User Agent: Configured to mimic Chrome on Linux to avoid immediate blocking.

⚠️ Disclaimer
This tool is for educational and research purposes. Please respect Reddit's robots.txt and Terms of Service. Excessive scraping may result in IP bans. The project currently sets ROBOTSTXT_OBEY = False in the spider's custom settings for compatibility with old.reddit.com structures; use responsibly.
