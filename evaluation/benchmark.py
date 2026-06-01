import json
from pathlib import Path
from app.orchestration.pipeline import ExtractionPipeline


def run_benchmark(dataset_dir: str, ground_truth_dir: str, model: str = "claude-sonnet-4-6") -> list[dict]:
    pipeline = ExtractionPipeline(model=model)
    dataset_path = Path(dataset_dir)
    gt_path = Path(ground_truth_dir)
    results = []
    for contract_file in dataset_path.glob("*"):
        if contract_file.suffix not in (".pdf", ".docx"):
            continue
        gt_file = gt_path / (contract_file.stem + ".json")
        if not gt_file.exists():
            continue
        ground_truth = json.loads(gt_file.read_text())
        result = pipeline.run(str(contract_file))
        results.append({
            "file": contract_file.name,
            "extracted": result["extracted"],
            "ground_truth": ground_truth,
            "scores": result["scores"],
            "needs_review": result["needs_review"],
        })
    return results
