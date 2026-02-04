# 🚀 Getting Started

This guide helps you **set up, run, and verify** the AI Code Review Agent on your local machine.

Whether you are a first-time user, contributor, or evaluator, follow these steps to get the system running smoothly.

---

## 📋 Prerequisites

Before starting, ensure you have the following installed:

- **Python 3.10.x** (recommended)
- **Git**
- **Ollama** (for running local LLMs)
- Minimum **8 GB RAM** (16 GB recommended)

Check versions:
```bash
python --version
git --version
```

---

## 📥 Clone the Repository

```bash
git clone https://github.com/YugSondagar/Code-Reveiw-Agent-Chatbot.git
cd Code-Reveiw-Agent-Chatbot
```

---

## 🧪 Create a Virtual Environment

### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 📦 Install Dependencies

```bash
pip install --upgrade pip
pip install -r backend/requirements.txt
```

If installation fails, refer to **troubleshooting.md**.

---

## 🤖 Install & Configure Ollama

### 1️⃣ Install Ollama
Download from:
👉 https://ollama.com

Verify installation:
```bash
ollama --version
```

---

### 2️⃣ Pull Recommended Model

```bash
ollama pull deepseek-coder:6.7b
```

This model is optimized for **code understanding and review**.

---

### 3️⃣ Start Ollama Server

```bash
ollama serve
```

By default, Ollama runs on:
```
http://localhost:11434
```

---

## ▶️ Run the Application

```bash
cd backend
python app.py
```

You should see output similar to:
```text
Running on http://127.0.0.1:5000
```

---

## ✅ Verify Installation

Test the API using `curl`, Postman, or any REST client.

### Sample Request
```bash
curl -X POST http://127.0.0.1:5000/review \
  -H "Content-Type: application/json" \
  -d '{"language":"python","code":"def add(a,b): return a+b"}'
```

### Expected Response
```json
{
  "bugs": [],
  "security": [],
  "code_quality": ["Add type hints"],
  "performance": [],
  "suggested_fix": "def add(a: int, b: int) -> int: return a + b"
}
```

If you receive a response, your setup is successful 🎉

---

## 🧭 What’s Next?

- Explore **features.md** to understand capabilities
- Read **user-guide.md** to learn how to use the system
- See **architecture.md** for internal design
- Refer to **api-reference.md** for endpoint details

---

## 🆘 Need Help?

If you face issues:
- Check **troubleshooting.md**
- Ensure Ollama is running
- Verify Python version

---

Happy building! 🚀

