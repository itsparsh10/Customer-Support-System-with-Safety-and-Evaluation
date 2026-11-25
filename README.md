# AI-Based Customer Support System with Safety and Evaluation
**Mini Project — Group 6 (20 Marks)**

An end-to-end, production-ready AI customer support application powered by a **FastAPI REST Backend** and a **Modern Custom HTML/Tailwind CSS/JavaScript Frontend**, integrated with **NVIDIA NIM** (`nvidia/nemotron-3.5-super-vl-120b-a12b`) and **Google Gemini API**.

---

## 🚀 Quick Start (One Shot Setup)

The virtual environment and all dependencies are **already created and installed** in `./venv`.

### Step 1: Check Your API Keys in `.env`
Open [`.env`](file:///Users/sparshsharma/Downloads/AI-Mini-Project/.env). Your NVIDIA API key is already configured:
```bash
NVIDIA_API_KEY=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
GEMINI_API_KEY=
```

---

### Step 2: Run the Web App
Run the startup script:
```bash
./run.sh
```
*(Or manually: `source venv/bin/activate && python server.py`)*

Open your browser at:  
👉 **`http://localhost:8000`**

---

### Step 3: Run the Terminal Evaluation Benchmark (Optional)
To run the automated benchmark across all 35 customer queries directly in your terminal:
```bash
source venv/bin/activate
python evaluate.py
```

---

## 🎨 Frontend & Backend Architecture

Unlike generic Streamlit UIs, this project features a **custom, modern, glassmorphic web interface**:
* **Backend:** FastAPI asynchronous REST server (`server.py`) serving:
  * `POST /api/chat`: Runs queries through guardrails + LLM inference + cost telemetry.
  * `POST /api/inspect`: Real-time pre-inference guardrail testing without invoking the LLM.
  * `GET /api/benchmark`: 35-query performance evaluation dataset.
  * `GET /api/status`: Active model and provider configuration.
* **Frontend:** Clean, responsive Single Page Application (`static/index.html`):
  * **💬 Live Chat Experience:** Real-time conversation, prompt suggestions, expandable telemetry badges (Latency, Tokens, Cost, Safety Status).
  * **🛡️ Guardrail Tester:** Interactive playground for testing prompt injections, DAN jailbreaks, and PII leaks, with live human escalation logs.
  * **📊 35-Query Benchmark Dashboard:** 5 KPI metric cards, category filters, live search, and filterable results table.
  * **📑 Presentation Deck:** Interactive 4-slide presentation viewer matching the syllabus requirements.
  * **📖 Architecture & Ethics:** Full technical workflow and responsible AI ethics documentation.

---

## 📊 Evaluation Benchmark Summary

| Metric | Result | Description |
| :--- | :--- | :--- |
| **Total Test Queries** | **35** | Curated across 7 real-world e-commerce domains |
| **Adversarial Defense Rate** | **100.0%** | **9 out of 9** prompt injections & DAN jailbreaks blocked |
| **Normal Query Pass Rate** | **100.0%** | **26 out of 26** legitimate customer queries allowed |
| **Overall Safety Accuracy** | **100.0%** | Zero false positives / false negatives |
| **Average Defense Latency** | **< 0.001s** | Malicious attacks intercepted in sub-milliseconds ($0 token cost) |
| **Average LLM Latency** | **1.29s** | NVIDIA Nemotron 3.5 Super VL 120B cloud inference |
| **Total Test Suite Cost** | **$0.000958 USD** | Less than 1/10th of a cent for 35 queries |

---

## 📁 Clean Project Structure

```
AI-Mini-Project/
├── .env                  # Active NVIDIA & Gemini API keys
├── .env.example          # Environment template
├── requirements.txt      # FastAPI, Uvicorn, OpenAI, Google SDKs, Pandas
├── venv/                 # Pre-configured Python 3.12 virtual environment
├── server.py             # FastAPI REST API backend
├── chatbot.py            # Dual-provider LLM client (NVIDIA NIM + Gemini)
├── safety.py             # Heuristic guardrail engine & regex patterns
├── dataset.json          # 35 test queries (normal + adversarial)
├── evaluate.py           # Standalone terminal evaluation script
├── run.sh                # 1-click startup script (FastAPI server on :8000)
├── PROJECT_REPORT.md     # Full 20-mark workflow report (Deliverable 1)
├── PRESENTATION_SLIDES.md# 4-slide presentation markdown (Deliverable 2)
├── slides.html           # Standalone 4-slide HTML presentation
└── static/
    ├── index.html        # Custom Tailwind CSS/JS web application
    └── slides.html       # Static presentation deck
```
