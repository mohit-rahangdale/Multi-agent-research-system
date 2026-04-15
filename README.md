# 🔥 Multi-Agent Research Pipeline

An automated, high-performance research assistant powered by **LangChain** and **Mistral AI**. This system orchestrates a team of specialized AI agents to search the web, scrape deep-dive content, draft structured reports, and critically evaluate the final output.

---

## 📉 System Architecture

The following flowchart illustrates the data flow through the multi-agent system. This diagram renders natively in GitHub using Mermaid.

```mermaid
graph TD
    A[User Input: Research Topic] --> B{🔍 Search Agent}
    B -->|Tavily API| C[Top 5 Search Results]
    C --> D{📖 Reader Agent}
    D -->|BeautifulSoup| E[Scraped Content]
    E --> F{✍️ Writer Chain}
    F -->|LCEL| G[Research Report]
    G --> H{🎯 Critic Chain}
    H -->|Evaluation| I[Score & Feedback]
    I --> J[Streamlit UI Display]
    
    style A fill:#FF6B00,stroke:#000,color:#fff
    style G fill:#FF8C00,stroke:#000,color:#fff
    style J fill:#FFA500,stroke:#000,color:#fff
