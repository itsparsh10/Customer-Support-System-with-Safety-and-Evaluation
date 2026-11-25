"""
server.py - FastAPI Backend Server for ApexMart AI Customer Support System
Group 6: AI-Based Customer Support System with Safety and Evaluation
"""

import os
import json
import time
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from chatbot import CustomerSupportBot
from safety import SafetyEngine
from evaluate import run_evaluation

# Load environment
load_dotenv()

app = FastAPI(
    title="ApexMart AI Customer Support API",
    description="Backend API for AI-Based Customer Support System with Safety and Evaluation",
    version="2.1.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Shared Bot Instance (Two-model system: Primary + Auto-Fallback)
bot = CustomerSupportBot()

# In-memory escalation storage
escalation_logs: List[Dict[str, Any]] = []

class ChatRequest(BaseModel):
    message: str

class InspectRequest(BaseModel):
    text: str

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_DIR, exist_ok=True)

@app.get("/api/status")
def get_system_status():
    """Returns current active model architecture status."""
    return {
        "status": "online",
        "primary_model": "NVIDIA Nemotron 3 Ultra (Main)",
        "fallback_model": "Grounded Policy Engine (Auto-Fallback)",
        "is_configured": bot.is_api_configured()
    }

@app.post("/api/chat")
def chat_endpoint(req: ChatRequest):
    """
    Core Chat Endpoint:
    Processes queries with sub-second response guarantee and automatic fallback.
    """
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Query message cannot be empty.")

    result = bot.process_query(req.message)

    if result["status"] in ("BLOCKED", "FLAGGED"):
        escalation_entry = {
            "id": len(escalation_logs) + 1,
            "timestamp": time.strftime("%H:%M:%S"),
            "query": req.message,
            "status": result["status"],
            "rule": result["triggered_rule"] or "FLAGGED_POLICY",
            "reason": result["safety_reason"]
        }
        escalation_logs.append(escalation_entry)

    return result

@app.post("/api/inspect")
def inspect_guardrail_endpoint(req: InspectRequest):
    """Direct Guardrail Analyzer for testing prompt injections and jailbreaks."""
    t0 = time.time()
    validation = SafetyEngine.validate_input(req.text)
    latency = round(time.time() - t0, 5)

    refusal_preview = None
    if validation["status"] in ("BLOCKED", "FLAGGED"):
        refusal_preview = SafetyEngine.get_safe_refusal_message(
            validation["triggered_rule"], 
            validation["reason"]
        )

    return {
        "text": req.text,
        "status": validation["status"],
        "is_adversarial": validation["is_adversarial"],
        "triggered_rule": validation["triggered_rule"],
        "reason": validation["reason"],
        "refusal_preview": refusal_preview,
        "latency_sec": latency
    }

@app.get("/api/benchmark")
def get_benchmark_results(refresh: bool = False):
    """Returns the 35-query benchmark evaluation data."""
    results_path = os.path.join(os.path.dirname(__file__), "evaluation_results.json")
    if refresh or not os.path.exists(results_path):
        data = run_evaluation("dataset.json", results_path)
    else:
        with open(results_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    return data

@app.get("/api/escalations")
def get_escalations():
    return {"escalations": escalation_logs, "total": len(escalation_logs)}

@app.get("/")
def serve_index():
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "ApexMart API is running."}

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 ApexMart AI Server running on http://localhost:{port}")
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)
