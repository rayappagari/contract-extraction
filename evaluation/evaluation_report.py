import json
from pathlib import Path
from evaluation.scoring import score_result

EVAL_FIELDS = [
    "contract_type", "effective_date", "expiration_date", "total_value",
    "currency", "payment_terms", "governing_law", "auto_renewal",
    "termination_for_convenience", "liability_cap",
]


def generate_report(benchmark_results: list[dict], output_path: str = "evaluation_report.json") -> dict:
    per_file = []
    for result in benchmark_results:
        scores = score_result(result["extracted"], result["ground_truth"], EVAL_FIELDS)
        per_file.append({"file": result["file"], "scores": scores})
    overall = sum(r["scores"]["overall"] for r in per_file) / len(per_file) if per_file else 0.0
    field_averages = {
        field: sum(r["scores"]["field_scores"].get(field, 0.0) for r in per_file) / len(per_file)
        for field in EVAL_FIELDS
    } if per_file else {}
    report = {"overall_accuracy": round(overall, 4), "field_averages": field_averages, "per_file": per_file}
    Path(output_path).write_text(json.dumps(report, indent=2))
    return report
