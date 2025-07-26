# 🧠 Lightweight Company Intelligence Agent

This project is an AI-powered research agent that autonomously gathers and summarizes public company intelligence — including summaries, official websites, key people, product lines, locations, and latest news — using local LLMs, public APIs, and a simple command-line or Streamlit interface.

---

## 🚀 Features

- 🔍 Wikipedia and DuckDuckGo integration to find official summaries and websites.
- 📰 Google News RSS scraping for the latest headlines.
- 🧠 Local LLMs via [Ollama](https://ollama.com/) using `gemma:2b` or `phi` to generate compact company summaries and additional key insights.
- 📦 Exports JSON reports for easy sharing.
- 💻 Works in CLI or Streamlit mode.

---

## 🏗️ High-Level Architecture

```text
          ┌────────────────────┐
          │  User Input (CLI)  │
          └────────┬───────────┘
                   │
                   ▼
     ┌─────────────────────────────┐
     │ LightweightCompanyAgent     │
     └────────────┬────────────────┘
                  │
    ┌─────────────┼────────────────────────────────────────────────────────────┐
    ▼             ▼              ▼                    ▼                      ▼
_get_wikipedia  _find_official  _generate_compact  _extract_additional     _get_news_
  _summary()       _website()        _summary()          _info()            _headlines()
    │               │                  │                  │                     │
    ▼               ▼                  ▼                  ▼                     ▼
Wikipedia API   DuckDuckGo API      ollama (LLM)      ollama (LLM x 3)     Google News RSS
   (REST)            (JSON)         → one paragraph   → key people         → headlines only
→ summary text   → website URL      summary           → products/services
                                                     → location/presence
```

# 🛠️ Setup Instructions for Lightweight Company Research Agent

This guide provides the steps to set up and run the project in two modes:
- 🖥️ **CLI Version**
- 🌐 **Streamlit UI Version**

---

## 📦 Step 1: Environment Setup (Common to Both Versions)

1. **Install Python 3.8+**
   > Make sure `python3` and `pip` are available in your terminal.

2. **Install Required Python Libraries**
   ```bash
   pip install ollama requests beautifulsoup4 feedparser
   ```
3. **Install ollama**
   > Visit https://ollama.com and install for your OS (Linux/Windows/Mac)
   > Start ollama Server
   ``` bash
   ollama serve
   ```
   > In other terminal run
   ``` bash
   ollama pull gemma:2b
   ollama pull phi
   ```
## CLI version 
 > run this command
   ``` bash
     python3 company_researcher.py
```
## Streamlit version
 > Install Streamlit
   ``` bash
       pip install streamlit
```
 > run streamlit
   ``` bash
    streamlit run app.py
```

