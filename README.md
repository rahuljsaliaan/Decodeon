# **DecodEON – LangChain-Powered Code Interpreter**

[![Railway](https://img.shields.io/badge/Hosted%20on-Railway-blue?logo=railway)](https://decodeon-production.up.railway.app/)

Welcome to **DecodEON**, a lightweight and intelligent code interpreter built with the power of LangChain. Decodeon enables developers to interact with and reason over code using AI agents — streamlining debugging, understanding, and automation in a single, intuitive interface.

## Live App

Try out Decodeon in your browser:  
🔗 [**Visit Decodeon App**](https://decodeon-production.up.railway.app/)

## Features

- **LangChain Agent Routing:** Powered by multiple intelligent agents that automatically choose the best strategy to interpret code or files.

- **Dynamic File Understanding:** Upload your `.csv` files and Decodeon will understand, query, and analyze them intelligently.

- **Chat-First Interface:** Ask natural-language questions and get contextual, AI-generated responses based on your uploaded files or project context.

- **Streamlit Frontend:** Clean and responsive interface for ease of interaction and real-time updates.

- **Error Handling & History:** Provides feedback, error tracking, and saves your interactions so you can refer back to past queries.

## How to Use

1. **Open the App:** Head over to [Decodeon](https://decodeon-production.up.railway.app/).
2. **Upload a CSV File (Optional):** Drop in a `.csv` file to let Decodeon reason over it.
3. **Enter a Query:** Ask a question, give a command, or request analysis — Decodeon’s agents will handle the rest.
4. **Interact Intelligently:** Review responses, continue the conversation, or try a new file.

## Technologies Used

- **LangChain** (Core agent routing & LLM integrations)
- **Langsmith & Langchain-Community** (Logging, tooling, and experiments)
- **OpenAI Integration via LangChain-OpenAI**
- **Pydantic & Pydantic-Settings** (For configuration and schema validation)
- **Pandas** (CSV parsing and tabular data manipulation)
- **Streamlit** (Frontend for app interface)
- **QRCode & Tabulate** (Additional output formatting and visual tools)

## Development Setup

> Requires Python `>=3.13,<3.14` and uses [Poetry](https://python-poetry.org/) for dependency management.

```bash
# Install dependencies
poetry install

# Run the application
poetry run start
```

## Continuous Deployment

**Decodeon** is hosted on **Railway**, leveraging continuous deployment so you always get the latest features and improvements instantly.

---

Thank you for checking out **Decodeon**! Whether you're analyzing code, exploring datasets, or experimenting with AI, Decodeon simplifies the process so you can focus on what matters most — building, debugging, and discovering.

Have feedback or feature ideas? Drop them in — we're just getting started!
