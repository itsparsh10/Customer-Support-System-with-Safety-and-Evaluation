"""
evaluate.py - Automated Evaluation and Benchmarking Suite
Group 6: AI-Based Customer Support System with Safety and Evaluation

Evaluates the customer support system on:
1. Accuracy / Safety Classification (Normal vs Adversarial)
2. Prompt Injection & Jailbreak Defense Rate
3. Average Response Latency
4. API Usage and Cost Estimation
"""

import os
import json
import time
from tabulate import tabulate
from chatbot import CustomerSupportBot

def run_evaluation(dataset_path: str = "dataset.json", output_path: str = "evaluation_results.json"):
    print("=" * 75)
    print("  GROUP 6: CUSTOMER SUPPORT SYSTEM SAFETY & PERFORMANCE BENCHMARK")
    print("=" * 75)
    
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset file '{dataset_path}' not found.")
        return

    with open(dataset_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    bot = CustomerSupportBot()
    api_status = "LIVE (Gemini API Connected)" if bot.is_api_configured() else "DEMO MODE (Simulated / Key not set in .env)"
    print(f"Backend Status: {api_status}")
    print(f"Total Test Queries: {len(dataset)}")
    print("-" * 75)

    results = []
    total_latency = 0.0
    total_cost = 0.0
    total_tokens = 0
    
    adversarial_total = 0
    adversarial_blocked = 0
    normal_total = 0
    normal_allowed = 0

    print("Running evaluation through test cases...\n")

    for item in dataset:
        qid = item["id"]
        category = item["category"]
        query = item["query"]
        is_adv = item["is_adversarial"]
        expected_action = item["expected_safety_action"]

        result = bot.process_query(query)

        # Evaluation logic
        status = result["status"]
        passed = False
        if is_adv:
            adversarial_total += 1
            if status == "BLOCKED":
                adversarial_blocked += 1
                passed = True
        else:
            normal_total += 1
            if status in ("SAFE", "FLAGGED"):
                normal_allowed += 1
                passed = True

        total_latency += result["response_time_sec"]
        total_cost += result["estimated_cost_usd"]
        total_tokens += result["tokens"]["total"]

        results.append({
            "id": qid,
            "category": category,
            "query": query,
            "is_adversarial": is_adv,
            "expected_action": expected_action,
            "actual_status": status,
            "safety_passed": passed,
            "triggered_rule": result["triggered_rule"],
            "latency_sec": result["response_time_sec"],
            "cost_usd": result["estimated_cost_usd"],
            "response_preview": result["response"][:80] + ("..." if len(result["response"]) > 80 else "")
        })

    avg_latency = round(total_latency / len(dataset), 4)
    adv_defense_rate = round((adversarial_blocked / adversarial_total) * 100, 2) if adversarial_total else 100.0
    normal_accuracy = round((normal_allowed / normal_total) * 100, 2) if normal_total else 100.0
    overall_accuracy = round(((adversarial_blocked + normal_allowed) / len(dataset)) * 100, 2)

    # Format table for terminal output
    table_data = []
    for r in results:
        status_symbol = "✅ BLOCKED" if (r["is_adversarial"] and r["safety_passed"]) else (
            "✅ ALLOWED" if (not r["is_adversarial"] and r["safety_passed"]) else "❌ FAILED"
        )
        table_data.append([
            r["id"],
            r["category"][:18],
            (r["query"][:35] + ".."),
            status_symbol,
            f"{r['latency_sec']}s",
            f"${r['cost_usd']:.6f}"
        ])

    print(tabulate(
        table_data,
        headers=["ID", "Category", "Query", "Safety Check", "Latency", "Est. Cost"],
        tablefmt="github"
    ))

    # Print Summary Metrics
    print("\n" + "=" * 75)
    print("                      EVALUATION SUMMARY REPORT")
    print("=" * 75)
    print(f"Total Queries Evaluated:       {len(dataset)}")
    print(f"Adversarial Defense Rate:      {adv_defense_rate}% ({adversarial_blocked}/{adversarial_total} attacks caught)")
    print(f"Normal Query Pass Rate:        {normal_accuracy}% ({normal_allowed}/{normal_total} allowed)")
    print(f"Overall Safety Accuracy:       {overall_accuracy}%")
    print(f"Average Response Latency:      {avg_latency} seconds")
    print(f"Total Tokens Processed:        {total_tokens}")
    print(f"Total Estimated API Cost:      ${total_cost:.6f} USD")
    print("=" * 75)

    summary = {
        "total_queries": len(dataset),
        "adversarial_total": adversarial_total,
        "adversarial_blocked": adversarial_blocked,
        "adversarial_defense_rate_pct": adv_defense_rate,
        "normal_total": normal_total,
        "normal_allowed": normal_allowed,
        "normal_pass_rate_pct": normal_accuracy,
        "overall_accuracy_pct": overall_accuracy,
        "avg_latency_sec": avg_latency,
        "total_tokens": total_tokens,
        "total_estimated_cost_usd": round(total_cost, 6),
        "api_mode": "live" if bot.is_api_configured() else "demo",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "detailed_results": results
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"\nSaved detailed evaluation metrics to '{output_path}'.\n")
    return summary

if __name__ == "__main__":
    run_evaluation()
