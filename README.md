# 🧠 Company Intelligence Agent

This project is an AI-powered research agent that autonomously gathers and summarizes public company intelligence — including summaries, official websites, key people, product lines, locations, and latest news — using local LLMs, public APIs, and a simple command-line or Streamlit interface.

---

## 🚀 Features and LLM used

- 🔍 Wikipedia and DuckDuckGo integration to find official summaries and websites.
- 📰 Google News RSS scraping for the latest headlines.
- 🧠 Local LLMs via [Ollama](https://ollama.com/) using `gemma:2b` and `phi` to generate compact company summaries and additional key insights.
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
     │ Company Researcher Agent     │
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

# 🛠️ Setup Instructions for Company Research Agent

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
<a href="https://drive.google.com/file/d/1m91GkIz7j47cT_a48n7AJxV3FgwH89AS/view?usp=sharing" target="_blank">
  <button style="padding:10px 20px; background-color:#4CAF50; color:white; border:none; border-radius:5px; cursor:pointer;">
    ▶️ CLI Version Demo Video
  </button>
</a>
> Output Screenshot
<img width="1100" height="843" alt="image" src="https://github.com/user-attachments/assets/9b02a451-8c1e-4962-b31e-cae05b786310" />
> JSON File Output
<img width="1694" height="538" alt="image" src="https://github.com/user-attachments/assets/a8b04b0b-8145-4415-b09c-8e46fd851839" />



## Streamlit version
 > Install Streamlit
   ``` bash
       pip install streamlit
```
 > run streamlit
   ``` bash
    streamlit run app.py
```
<a href="https://drive.google.com/file/d/1oy1NyIS5zRX_dwBxSIpntZWF6jtma4OP/view?usp=sharing" target="_blank">
  <button style="padding:10px 20px; background-color:#4CAF50; color:white; border:none; border-radius:5px; cursor:pointer;">
    ▶️ Streamlit Version Demo Video
  </button>
</a>

> Output Screenshot
<img width="1238" height="569" alt="image" src="https://github.com/user-attachments/assets/cf0abf96-68c3-48f8-824a-e584c8539a44" />
<img width="1222" height="745" alt="image" src="https://github.com/user-attachments/assets/ba9c9350-19c6-4bbd-82ee-6e4d2f67029b" />
<img width="1214" height="597" alt="image" src="https://github.com/user-attachments/assets/3526f0b6-692a-42e1-9d03-ea4bd48eab15" />






