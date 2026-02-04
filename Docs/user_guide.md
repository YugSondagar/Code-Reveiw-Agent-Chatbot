# User Guide

This guide explains how to use the **AI-Based Code Analysis Platform** from a user’s perspective. It is written for **students, developers, recruiters, and reviewers** who want to analyze code quality, security, and best practices using AI.

---

## 1. Who Is This For?

This platform is useful for:

* **Students** – to improve code quality and learn best practices
* **Developers** – to quickly review unfamiliar or legacy code
* **Hackathon Judges / Recruiters** – to assess code structure and maintainability
* **Teams** – to standardize code review using AI

No prior AI or DevOps knowledge is required.

---

## 2. Accessing the Application

1. Start the Flask server (see `getting-started.md`)
2. Open your browser and navigate to:

   ```
   http://localhost:5000
   ```
3. You will see the **Code Analysis Dashboard**

---

## 3. Analyzing Code

The platform supports **two ways** of submitting code.

### Option A: Paste Code

1. Select the **Programming Language** (Python, Java, C++, JavaScript, etc.)
2. Paste your source code into the editor
3. Click **Analyze Code**

Best for:

* Small files
* Interview questions
* Quick checks

---

### Option B: Upload Code Files (Recommended)

1. Click **Upload File**
2. Select a supported source file (`.py`, `.js`, `.java`, `.cpp`, etc.)
3. Click **Analyze Code**

Best for:

* Real-world projects
* Long files
* Accurate analysis

> ⚠️ Maximum file size is configurable in `configuration.md`

---

## 4. Understanding the Analysis Report

After submission, the system generates a **structured analysis report**.

### 4.1 Code Summary

* What the code does
* High-level purpose
* Main components

---

### 4.2 Code Quality Analysis

* Readability
* Naming conventions
* Code duplication
* Modularity

---

### 4.3 Security Analysis

* Hardcoded secrets
* Unsafe patterns
* Injection risks
* Insecure practices

---

### 4.4 Performance Analysis

* Inefficient loops
* Unnecessary computations
* Scalability concerns

---

### 4.5 Best Practices & Improvements

* Actionable suggestions
* Language-specific standards
* Refactoring recommendations

---

## 5. AI vs Static Analysis (How It Works)

The platform uses a **hybrid approach**:

* **Static Analyzer** → Fast rule-based checks
* **LLM (Ollama)** → Deep contextual understanding

This ensures:

* Lower hallucination risk
* More accurate feedback
* Explainable suggestions

---

## 6. Supported Languages

Currently supported:

* Python
* Java
* JavaScript
* C / C++
* Go (basic)
* Planned: Rust, TypeScript

Language support can be extended easily.

---

## 7. Performance Tips

For best results:

* Upload files instead of pasting large code
* Keep files under configured token limits
* Use appropriate language selection

---

## 8. Privacy & Security

* Code is processed **locally** using Ollama
* No data is sent to external servers
* Uploaded files are deleted after analysis

Ideal for:

* Private projects
* College assignments
* Confidential code

---

## 9. Common User Mistakes

| Issue                   | Solution                                |
| ----------------------- | --------------------------------------- |
| Wrong language selected | Choose correct language before analysis |
| Very large file         | Increase chunk size or split file       |
| Ollama not running      | Start Ollama before Flask server        |

---

## 10. What’s Next?

Planned improvements:

* Project-level analysis (multiple files)
* GitHub repository scanning
* Downloadable PDF reports
* CI/CD integration

---

## 11. Need Help?

If something doesn’t work:

* Check `troubleshooting.md`
* Review logs in the `logs/` folder
* Open an issue on GitHub

---

✅ **You’re now ready to use the AI Code Analysis Platform effectively.**
