# 🔥 Multi-Agent Research System

An AI-powered **multi-agent research pipeline** that autonomously searches, analyzes, writes, and critiques research reports using LLMs and tools.

Built with **LangChain, Streamlit, Tavily API, and Mistral AI**.

---

## 🚀 Features

- 🔍 **Search Agent** → Finds relevant and recent information from the web  
- 📖 **Reader Agent** → Extracts detailed content from selected URLs  
- ✍️ **Writer Agent** → Generates structured research reports  
- 🎯 **Critic Agent** → Evaluates and improves the report quality  
- 🖥️ **Interactive UI (Streamlit)** with history & download option  

---

## 🧠 System Architecture

The system follows a **multi-agent pipeline**, where each agent performs a specialized task.

### 🔄 Flowchart

```mermaid
flowchart TD

A[User Input Topic] --> B[Search Agent 🔍]
B --> C[Web Search Tool (Tavily API)]

C --> D[Reader Agent 📖]
D --> E[Scrape URL Tool]

E --> F[Writer Agent ✍️]
F --> G[Generate Research Report]

G --> H[Critic Agent 🎯]
H --> I[Feedback & Score]

I --> J[Final Output in UI]

