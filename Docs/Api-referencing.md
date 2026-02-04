# 🔌 API Reference

This document describes all **available API endpoints**, request/response formats, and error handling for the AI Code Review Agent.

The API is designed to be **simple, predictable, and easy to integrate** with UIs, CLIs, and CI/CD pipelines.

---

## 🌐 Base URL

```text
http://127.0.0.1:5000
```

All endpoints are relative to this base URL.

---

## 📌 Authentication

* ❌ No authentication required (local-first tool)
* 🔒 Can be extended with API keys or OAuth if deployed publicly

---

## 📤 POST /review

Analyze source code and return a structured review.

### Description

This endpoint accepts source code (and optional metadata), performs:

* Language detection
* Static analysis
* LLM-based semantic review

Then returns a **structured JSON report**.

---

### Request Headers

```http
Content-Type: application/json
```

---

### Request Body

```json
{
  "language": "python",
  "code": "def add(a, b): return a + b"
}
```

#### Parameters

| Field    | Type   | Required | Description                                     |
| -------- | ------ | -------- | ----------------------------------------------- |
| language | string | ❌        | Programming language (auto-detected if omitted) |
| code     | string | ✅        | Source code to analyze                          |

---

### Successful Response (200 OK)

```json
{
  "bugs": ["Missing input validation"],
  "security": ["No critical security issues found"],
  "code_quality": ["Add type hints", "Follow PEP8 formatting"],
  "performance": ["No performance bottlenecks detected"],
  "suggested_fix": "def add(a: int, b: int) -> int: return a + b"
}
```

#### Response Fields

| Field         | Type         | Description                         |
| ------------- | ------------ | ----------------------------------- |
| bugs          | list[string] | Logical or runtime issues           |
| security      | list[string] | Security vulnerabilities or notes   |
| code_quality  | list[string] | Style and best-practice suggestions |
| performance   | list[string] | Performance-related feedback        |
| suggested_fix | string       | Optional refactored code            |

---

## 📂 POST /review/file (Planned)

Analyze an uploaded file.

```http
Content-Type: multipart/form-data
```

| Field | Type | Description      |
| ----- | ---- | ---------------- |
| file  | File | Source code file |

---

## 📁 POST /review/folder (Planned)

Analyze an entire project folder.

### Behavior

* Recursively scans source files
* Skips binaries and config files
* Aggregates results per file

---

## ❌ Error Responses

### 400 Bad Request

```json
{
  "error": "Code field is required"
}
```

### 500 Internal Server Error

```json
{
  "error": "LLM service unavailable"
}
```

---

## 🧪 Example cURL Usage

```bash
curl -X POST http://127.0.0.1:5000/review \
  -H "Content-Type: application/json" \
  -d '{"code": "def square(x): return x*x"}'
```

---

## 🔄 Status Codes Summary

| Status Code | Meaning             |
| ----------- | ------------------- |
| 200         | Successful analysis |
| 400         | Invalid request     |
| 500         | Server or LLM error |

---

## 🛣️ API Roadmap

Planned API enhancements:

* Async analysis endpoints
* Batch code review
* GitHub webhook integration
* OpenAPI / Swagger documentation

---

## ⭐ Summary

The API is intentionally minimal yet powerful, enabling easy integration while supporting advanced AI-driven code analysis.

Next:

* See **configuration.md** to customize system behavior.

---

Happy integrating! 🚀
