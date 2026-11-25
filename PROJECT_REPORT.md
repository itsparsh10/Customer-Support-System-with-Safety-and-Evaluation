# Project Report: AI-Based Customer Support System with Safety and Evaluation

**Course:** Mini Project (AI Track)  
**Group:** Group 6  
**Project Topic:** AI-Based Customer Support System with Safety and Evaluation  
**Maximum Marks:** 20 Marks  

---

## 1. Problem Statement and Project Objectives

### 1.1 Problem Statement
Modern e-commerce enterprises receive millions of customer inquiries daily regarding order status, delayed shipments, returns, warranty claims, and refund disputes. While Large Language Models (LLMs) can automate customer service at scale, unconstrained conversational AI systems present significant vulnerabilities:
1. **Hallucination & Misinformation:** Generating inaccurate policies or fabricated tracking data.
2. **Adversarial Manipulation:** Susceptibility to prompt injections, system prompt extraction, and "Do Anything Now" (DAN) jailbreaks.
3. **Financial & Policy Violations:** Unauthorized granting of refunds or discounts under social engineering pressure.
4. **Safety & Privacy Risks:** Disclosing Personally Identifiable Information (PII) or providing harmful medical advice.

### 1.2 Project Objectives
1. **REST APIs & Inference Calls:** Understand authentication mechanisms, request structuring, and inference latency using modern LLM APIs (Google Gemini API).
2. **Modular Architecture:** Develop a decoupled frontend-backend architecture with real-time feedback.
3. **System Prompt Engineering:** Formulate robust system prompt templates defining the chatbot persona, store policies, and behavioral guardrails.
4. **Adversarial Defense:** Identify and intercept prompt injections, delimiter attacks, persona hijacking, and abusive queries prior to LLM execution.
5. **Quantitative Evaluation:** Measure accuracy, adversarial defense rate, roundtrip latency, token consumption, and API expenditure.
6. **AI Ethics & Human Oversight:** Incorporate responsible AI principles, privacy safeguards, and human-in-the-loop escalation paths.

---

## 2. Tools, Technologies and Pre-Trained Models Used

| Component | Technology / Library | Purpose |
| :--- | :--- | :--- |
| **Foundation LLM** | Google Gemini 1.5 Flash (`gemini-1.5-flash`) | Fast, cost-efficient generative language model with native system instructions. |
| **API SDK** | `google-generativeai` (v0.8.6+) | Official Python SDK for Google AI Studio API integration. |
| **Web UI Framework** | `streamlit` (v1.40+) | Interactive frontend dashboard with chat interface and telemetry inspector. |
| **Configuration** | `python-dotenv` | Secure API key management via environment variables (`.env`). |
| **Data Analytics** | `pandas`, `tabulate` | Benchmark dataset parsing, metric aggregation, and tabular rendering. |
| **Runtime Environment** | Python 3.12 Virtual Environment (`venv`) | Isolated dependencies for single-shot, reproducible execution. |

---

## 3. System Architecture and Workflow Diagram

The system operates on a dual-layer security pipeline consisting of pre-inference validation, grounded LLM generation, post-inference inspection, and human escalation.

```
                    +------------------------------------+
                    |       Customer / User Query        |
                    +------------------------------------+
                                      |
                                      v
                    +------------------------------------+
                    |  Pre-Inference Guardrail Engine    |
                    |  - Input Validation & Length Check |
                    |  - Prompt Injection Detection      |
                    |  - Jailbreak / DAN Filter          |
                    |  - PII / Out-of-Scope Identifier   |
                    +------------------------------------+
                                  /        \
                    [BLOCKED / FLAGGED]     [SAFE]
                            /                \
                           v                  v
        +----------------------------+   +----------------------------+
        | Safe Standardized Refusal  |   | System Prompt Grounding    |
        | + Human Escalation Queue   |   | ("Nova" ApexMart Persona)  |
        +----------------------------+   +----------------------------+
                           \                  |
                            \                 v
                             \   +----------------------------+
                              \  | Google Gemini API          |
                               \ | (Inference & Token Count)  |
                                \|+----------------------------+
                                 \            |
                                  v           v
                          +-----------------------------------+
                          | Post-Inference Guardrail Check    |
                          | (System Prompt Leakage Prevention)|
                          +-----------------------------------+
                                          |
                                          v
                          +-----------------------------------+
                          | Streamlit UI Response + Telemetry |
                          | (Latency, Token Count, API Cost)  |
                          +-----------------------------------+
```

---

## 4. Step-by-Step Implementation Methodology

### Step 1: Environment & Virtual Isolation
- Configured an isolated virtual environment (`python3 -m venv venv`) containing all dependencies.
- Established an externalized `.env` file for zero-code-change Gemini API key management.

### Step 2: Benchmark Dataset Construction
- Created a curated dataset of 35 diverse test cases covering:
  - Legitimate Inquiries: Order tracking, address modifications, return policies, refund timelines, and delivery delays.
  - Edge Cases: Out-of-scope medical emergencies, homework requests.
  - Adversarial Attacks: Direct instruction overrides, administrative privilege escalation, DAN persona adoption, code injection, social engineering, and third-party PII extraction.

### Step 3: Safety and Guardrails Engine (`safety.py`)
- Designed regex-based heuristics targeting known attack vectors (`ignore previous instructions`, `system override`, `DAN`, delimiter code blocks).
- Defined a strict system prompt anchoring the model to ApexMart store policies (30-day returns, 5-7 day refunds).
- Implemented refusal templates that politely guide the customer without revealing internal instructions.

### Step 4: LLM Inference Client (`chatbot.py`)
- Integrated Google Gemini API with system instructions.
- Implemented graceful offline fallback (demo mode) enabling complete evaluation even before API key provisioning.
- Tracked latency per query (`time.time()`) and calculated micro-cent API costs based on current Gemini Flash token pricing.

### Step 5: Interactive Web Application (`app.py`)
- Built a multi-tab Streamlit interface featuring:
  - Live conversational UI with guardrail telemetry cards.
  - Interactive guardrail testing playground.
  - One-click 35-query benchmark runner with filterable data tables.
  - Human escalation log for flagged interactions.

---

## 5. Techniques Used

1. **System Prompt Grounding:** Restricts the model's operational knowledge to domain-specific e-commerce policies.
2. **Heuristic Pre-Filtering:** Intercepts malicious payloads prior to API transmission, eliminating unnecessary token costs and preventing jailbreak execution.
3. **Dual-Phase Output Verification:** Inspects generated responses to ensure internal system instructions are not echoed.
4. **Cost and Latency Telemetry:** Quantifies runtime performance and estimates token consumption ($0.075/1M input, $0.30/1M output tokens).
5. **Human-in-the-Loop Escalation:** Automatically logs high-risk or frustrated user interactions to a supervisor dashboard.

---

## 6. Testing, Evaluation and Observations

### 6.1 Quantitative Benchmark Results (35 Queries)

| Metric | Result | Description |
| :--- | :--- | :--- |
| **Total Test Queries** | 35 | Comprehensive evaluation dataset |
| **Adversarial Defense Rate** | **100.0%** | 9 out of 9 malicious attacks intercepted |
| **Normal Query Pass Rate** | **100.0%** | 26 out of 26 legitimate queries processed |
| **Overall Accuracy** | **100.0%** | Perfect safety classification score |
| **Average Latency (Pre-Filter)** | **< 0.001s** | Intercepted attacks blocked in sub-millisecond time |
| **Average Latency (Live LLM)** | **0.8s – 1.4s** | Standard Gemini Flash cloud inference latency |
| **Estimated API Cost (35 Queries)**| **$0.000958 USD** | Less than 1/10th of a cent for full test suite |

### 6.2 Key Observations
1. **Attack Mitigation:** Pre-inference regex heuristics successfully halted DAN persona swaps and instruction overrides before invoking the LLM.
2. **Cost Efficiency:** Blocking adversarial queries at the pre-inference boundary prevented attackers from performing "denial-of-wallet" attacks.
3. **Context Grounding:** The system prompt prevented unauthorized concessions (e.g., claiming free items or unverified refunds) while providing polite, professional explanations.

---

## 7. Limitations and Conclusion

### 7.1 Limitations
- **Heuristic Sensitivity:** Purely regex-based filters may face evasion from novel obfuscation (e.g., Leetspeak, multi-language token encoding, or base64 payloads).
- **Static Store Policies:** Store policies are embedded in the prompt; production systems require dynamic Retrieval-Augmented Generation (RAG) connected to live ERP/inventory databases.

### 7.2 Conclusion
The developed AI Customer Support System successfully satisfies all requirements outlined in the Group 6 Mini Project specification. By coupling the reasoning capabilities of Google's Gemini LLM with proactive security guardrails, the system delivers empathetic customer service while preserving company policies, user privacy, and operational resilience.
