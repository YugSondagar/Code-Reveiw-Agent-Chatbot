# 🚀 AI Code Review Agent (Flask + Ollama)

> **An advanced, automated code review system that combines static analysis and LLM-based reasoning to deliver fast, accurate, and actionable feedback across multiple programming languages.**

---

## 📌 Overview

Modern software teams need **fast, reliable code reviews**—but manual reviews are slow and inconsistent. This project solves that problem by building an **AI-powered Code Review Agent** that:

- Analyzes code quality, bugs, and security issues
- Supports **multiple programming languages**
- Uses **local LLMs via Ollama** (no API cost)
- Combines **static analysis tools + AI reasoning**
- Provides **structured, professional review output**

This project is designed with **industry-level architecture**, making it ideal for:

- Hackathons 🏆
- Resume & portfolio projects
- Learning AI agents + backend systems

---

## ✨ Key Features

- 🔍 **Automated Code Review** – instant feedback on submitted code
- 🧠 **LLM-Powered Analysis** – deep reasoning using code-specialized models
- 🧪 **Static Analysis Integration** – pylint, bandit, radon, AST parsing
- 🌐 **Multi-Language Support** (extensible)
- 📂 **File / Folder Upload Support**
- 🧩 **Chunked Context Handling** for large files
- 📊 **Structured Output** (bugs, security, quality, performance)
- 💻 **Runs Fully Offline** using Ollama

---

## 🧠 Tech Stack

### Backend

- **Python 3.10.x**
- **Flask** – lightweight backend framework
- **Ollama** – local LLM runtime

### LLM Models

- **DeepSeek-Coder 6.7B** (Primary)
- Qwen2.5-Coder 7B (Optional alternative)

### Code Analysis Tools

- `ast` (Python Abstract Syntax Tree)
- `pylint` – code quality
- `bandit` – security analysis
- `radon` – complexity metrics
- `tree-sitter` (for non-Python languages)

---

## 📁 Project Structure

```text
code-review-agent/
│
├── backend/
│   ├── app.py                  # Flask app entry point
│   │
│   ├── routes/
│   │   └── review.py            # API routes for code review
│   │
│   ├── services/
│   │   ├── ollama_client.py     # Ollama API integration
│   │   ├── code_analyzer.py     # LLM prompt + response logic
│   │   └── static_analysis.py   # pylint, bandit, radon
│   │
│   ├── utils/
│   │   ├── language_detect.py   # Auto-detect programming language
│   │   ├── chunker.py           # Large code chunking
│   │   └── formatter.py         # Structured output formatter
│   │
│   ├── prompts/
│   │   └── review_prompt.txt    # Professional review prompt
│   │
│   ├── requirements.txt
│   └── config.py
│
├── frontend/                    # Optional (HTML / React)
│
├── samples/                     # Sample code for testing
├── README.md
└── .gitignore
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/YugSondagar/Code-Reveiw-Agent-Chatbot.git
cd Code-Reveiw-Agent-Chatbot
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Linux/Mac
```

### 3️⃣ Install Dependencies

```bash
pip install -r backend/requirements.txt
```

---

## 🤖 Ollama Setup

### Install Ollama

👉 [https://ollama.com](https://ollama.com)

### Pull Recommended Model

```bash
ollama pull deepseek-coder:6.7b
```

Ensure Ollama is running:

```bash
ollama serve
```

---

## ▶️ Running the Application

```bash
cd backend
python app.py
```

The server will start at:

```
http://127.0.0.1:5000
```

---

## 🔄 How the System Works

```text
User Code
   ↓
Language Detection
   ↓
Static Analysis (pylint, bandit, radon)
   ↓
Context Chunking
   ↓
LLM (DeepSeek-Coder via Ollama)
   ↓
Structured Review Output
```

---

## 📤 API Example

### Endpoint

```
POST /review
```

### Request (JSON)

```json
{
  "language": "python",
  "code": "def add(a,b): return a+b"
}
```

### Response (Sample)

```json
{
  "bugs": ["No input validation"],
  "security": ["No critical issues found"],
  "code_quality": ["Add type hints"],
  "performance": ["No optimization required"],
  "suggested_fix": "def add(a: int, b: int) -> int: return a + b"
}
```

---

## 🌍 Supported Languages (Current & Planned)

| Language   | Support    |
| ---------- | ---------- |
| Python     | ✅ Full     |
| JavaScript | 🔜 Planned |
| Java       | 🔜 Planned |
| C / C++    | 🔜 Planned |
| Go         | 🔜 Planned |
| TypeScript | 🔜 Planned |

---

## 🏆 Why This Project Stands Out

- ✅ **Hybrid AI + Static Analysis** (industry-grade approach)
- ✅ **Local LLM (No API Cost)**
- ✅ **Scalable Architecture**
- ✅ **Multi-language Ready**
- ✅ **Perfect for Hackathons & Internships**

This project mirrors **real-world internal developer tools** used at tech companies.

---

## 🚧 Future Enhancements

- GitHub PR review bot
- Code quality scoring dashboard
- Diff-based review (before vs after)
- CI/CD integration
- Vector-based long-term code memory

---

## 👨‍💻 Author

**Yug Sondagar**\
B.Tech CSE | AI & Backend Enthusiast

---

## ⭐ Final Note

If you find this project useful, consider giving it a ⭐.\
This project is built with **learning, scalability, and real-world impact** in mind.

Happy coding! 🚀

"# Code-Reveiw-Agent-Chatbot" 
