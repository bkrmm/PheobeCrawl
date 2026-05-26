# PheobeCrawl: A Personal Insight Agent

A specialized set of Scrapy spiders designed to extract multiple websites from Machine Learning and AI Academic Infrastructure, coupled with a Google Gemini integration to synthesize trends, themes, and community sentiment.

## Work-In-Progress:
- [X] Markdown Sucks
- [ ] More Website like HackerNews and Twitter to be added with their own spiders.
- [ ] A Terminal UI 

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
        └── hackernews.py     # The core hackernews spider: scrapes https://news.ycombinator.com/ and follows every post to its original article.
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

## Output Format

```text
PheobeCrawl main  ? ❯ python gemini_insights.py
✅ API Key Detected.
✅ Loaded data from output/reddit_2026-05-19T17-30-21+00-00.json
✅ Loaded data from output/hackernews_2026-05-25T13-29-08+00-00.json
✅ Loaded data from output/hackernews_2026-05-25T14-21-50+00-00.json
✅ Total entries collected: 3002
🚀 Processing 61 chunks of data using gemini-3.1-flash-lite...
✅ Processed chunk 1/61
✅ Processed chunk 2/61
✅ Processed chunk 3/61
✅ Processed chunk 4/61
✅ Processed chunk 5/61
✅ Processed chunk 6/61
✅ Processed chunk 7/61
✅ Processed chunk 8/61
✅ Processed chunk 9/61
✅ Processed chunk 10/61
✅ Processed chunk 11/61
✅ Processed chunk 12/61
✅ Processed chunk 13/61
✅ Processed chunk 14/61
✅ Processed chunk 15/61
✅ Processed chunk 16/61
✅ Processed chunk 17/61
✅ Processed chunk 18/61
✅ Processed chunk 19/61
✅ Processed chunk 20/61
✅ Processed chunk 21/61
✅ Processed chunk 22/61
✅ Processed chunk 23/61
✅ Processed chunk 24/61
✅ Processed chunk 25/61
✅ Processed chunk 26/61
✅ Processed chunk 27/61
✅ Processed chunk 28/61
✅ Processed chunk 29/61
✅ Processed chunk 30/61
✅ Processed chunk 31/61
✅ Processed chunk 32/61
✅ Processed chunk 33/61
✅ Processed chunk 34/61
✅ Processed chunk 35/61
✅ Processed chunk 36/61
✅ Processed chunk 37/61
✅ Processed chunk 38/61
✅ Processed chunk 39/61
✅ Processed chunk 40/61
✅ Processed chunk 41/61
✅ Processed chunk 42/61
✅ Processed chunk 43/61
✅ Processed chunk 44/61
✅ Processed chunk 45/61
✅ Processed chunk 46/61
✅ Processed chunk 47/61
✅ Processed chunk 48/61
✅ Processed chunk 49/61
✅ Processed chunk 50/61
✅ Processed chunk 51/61
✅ Processed chunk 52/61
✅ Processed chunk 53/61
✅ Processed chunk 54/61
✅ Processed chunk 55/61
✅ Processed chunk 56/61
✅ Processed chunk 57/61
✅ Processed chunk 58/61
✅ Processed chunk 59/61
✅ Processed chunk 60/61
✅ Processed chunk 61/61

🚀 Generating final synthesis...

--- Gemini Final Insights ---

This report synthesizes the provided Reddit and Hacker News data, capturing a technology sector in the midst of a "post-hype" correction. The community is transitioning from a period of unbridled AI enthusiasm to a pragmatic, often cynical, evaluation of the technology's real-world costs, ethical integrity, and operational feasibility.

### 1. Major Trends
*   **From "AI-Hype" to "AI-Realism":** The focus has shifted from the theoretical potential of LLMs to their operational overhead. The community is preoccupied with the "Hidden Costs" of AI, including energy consumption, skyrocketing hardware/memory prices, and the "AI-generated slop" that is polluting academic research and coding repositories.
*   **The "Agentic" Mirage:** A recurring technical trend is the skepticism toward "Agentic AI." Developers increasingly characterize many "agents" as glorified `while-loops` or orchestration wrappers that lack true autonomy, observability, or reliable memory management.
*   **Infrastructure Scrutiny:** There is a surge in "back to basics" engineering. While companies pivot to AI, the community is re-focusing on low-level performance, foundational data structures (e.g., skip-lists, system-level optimizations), and the resilience of physical infrastructure (data centers, grids) that AI ironically relies on.
*   **Regulatory & Ethical Pushback:** We are seeing the rise of "sovereign cloud" initiatives, resistance to corporate tax breaks for data centers, and a growing grassroots effort to protect creative autonomy through local model hosting and self-managed workflows.

### 2. Recurring Themes across Platforms
*   **Academic and Peer Review Crisis:** Both platforms highlight a "broken" scientific ecosystem. The prevalence of LLM-generated papers (hallucinated citations, "slop") has forced institutions like arXiv to implement punitive measures (1-year bans). The community largely views this as a symptom of a "publish or perish" culture incentivizing throughput over rigor.
*   **The "Human-Centric" Defensive Stance:** Across developer forums and social threads, there is a strong defensive posture regarding human expertise. There is widespread pushback against "vibe coding"—the practice of using AI to generate code without understanding it—which is blamed for rising security vulnerabilities and technical debt.
*   **Distrust of Big Tech Leadership:** A shared cynical view persists regarding leadership at firms like OpenAI, Meta, and Google. Users frequently frame corporate moves as "performative" or "AI-washing," where the technology is used as a scapegoat for layoffs or a mechanism for data harvesting rather than genuine product improvement.

### 3. Community Sentiment: Reddit vs. Hacker News
While there is significant overlap in their skepticism, the two platforms exhibit distinct flavors of discourse:

| Platform | Dominant Sentiment | Primary Focus |
| :--- | :--- | :--- |
| **Reddit (r/LocalLLaMA, etc.)** | **Existential & Adversarial** | Focuses on the societal fallout: job displacement, class divides, anti-corporate activism, and the "dystopian" potential of AI surveillance. The tone is often highly polarized and emotional. |
| **Hacker News** | **Technical & Cynical Pragmatism** | Focuses on systemic efficiency, engineering integrity, and legal/economic policy. The tone is professional but deeply suspicious of corporate narratives, focusing on "how it breaks" rather than "how it changes the world." |

*   **Reddit** acts as the emotional and social pulse of the community, where the discourse often devolves into "Us vs. Them" narratives regarding billionaire "broligarchs" and the decline of the middle class.
*   **Hacker News** acts as the technical "check and balance," where the community performs forensic analysis on the mechanics of AI failure, legal precedents for tax breaks, and the stability of the software supply chain.
```

### Conclusion
The prevailing sentiment is one of **"Corrective Maintenance."** The tech community is moving past the phase of uncritical excitement and entering a stage of hardening. Whether through the implementation of stricter academic publishing bans, the development of firewalls for AI agents, or a renewed interest in retro-computing and physical hardware, the sector is currently preoccupied with building **resilience** against the noise, instability, and centralization that have come to define the "AI Era."

----------------------------


⚠️ Disclaimer
This tool is for educational and research purposes. Please respect Reddit's robots.txt and Terms of Service. Excessive scraping may result in IP bans. The project currently sets ROBOTSTXT_OBEY = False in the spider's custom settings for compatibility with old.reddit.com structures; use responsibly.
