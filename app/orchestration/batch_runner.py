import logging
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from app.orchestration.pipeline import ExtractionPipeline

logger = logging.getLogger(__name__)


def run_batch(file_paths: list[str], model: str = "claude-sonnet-4-6", max_workers: int = 4) -> list[dict]:
    pipeline = ExtractionPipeline(model=model)
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_path = {executor.submit(pipeline.run, fp): fp for fp in file_paths}
        for future in as_completed(future_to_path):
            path = future_to_path[future]
            try:
                result = future.result()
                results.append(result)
                logger.info(f"Completed: {path}")
            except Exception as e:
                logger.error(f"Failed: {path} — {e}")
                results.append({"file": path, "error": str(e)})
    return results


def discover_files(directory: str, extensions: tuple = (".pdf", ".docx")) -> list[str]:
    root = Path(directory)
    return [str(p) for ext in extensions for p in root.rglob(f"*{ext}")]
