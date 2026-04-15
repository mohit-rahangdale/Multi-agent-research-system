🔥 Multi-Agent Research Pipeline
An automated, high-performance research assistant powered by LangChain and Mistral AI. This system orchestrates a team of specialized AI agents to search the web, scrape deep-dive content, draft structured reports, and critically evaluate the final output.

🚀 Overview
Traditional LLM queries are limited by their training data. This pipeline overcomes that by:

1. Searching for live, real-time data.

2. Scraping specific, high-value URLs for depth.

3. Synthesizing information into a professional report.

4. Critiquing the work to ensure high quality and factual accuracy.

   🛠️ Tech Stack
Orchestration: LangChain

LLM: Mistral AI (mistral-small-latest)

Interface: Streamlit (Custom Orange & Black Theme)

Search Engine: Tavily AI

Scraping: BeautifulSoup4 & Requests

📉 System Architecture & Flow
The following flowchart illustrates how data moves through the multi-agent system:


graph TD
    A[User Input: Research Topic] --> B{🔍 Search Agent}
    B -->|Queries Tavily API| C[Top 5 Search Results]
    C --> D{📖 Reader Agent}
    D -->|Scrapes Text Content| E[Deep-Dive Research Data]
    E --> F{✍️ Writer Agent}
    F -->|LCEL Chain| G[Structured Research Report]
    G --> H{🎯 Critic Agent}
    H -->|Evaluation| I[Score & Feedback]
    I --> J[Final UI Display]
    
    style A fill:#FF6B00,stroke:#000,color:#fff
    style G fill:#FF8C00,stroke:#000,color:#fff
    style J fill:#FFA500,stroke:#000,color:#fff
