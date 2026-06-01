# Runbook

## Running a Single Contract

```bash
python -c "
from app.orchestration.pipeline import ExtractionPipeline
result = ExtractionPipeline().run('path/to/contract.pdf')
print(result)
"
```

## Running a Batch

```bash
python -c "
from app.orchestration.batch_runner import run_batch, discover_files
files = discover_files('data/contracts/')
results = run_batch(files, max_workers=4)
print(f'Processed {len(results)} files')
"
```

## Running Evaluation

```bash
python -m evaluation.benchmark
python -m evaluation.evaluation_report
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | Claude API key |
| `SNOWFLAKE_ACCOUNT` | Snowflake account identifier |
| `SNOWFLAKE_USER` | Snowflake username |
| `SNOWFLAKE_PASSWORD` | Snowflake password |
| `SQS_QUEUE_URL_DEV` | SQS queue URL for dev |
| `SQS_QUEUE_URL_QA` | SQS queue URL for QA |
| `SQS_QUEUE_URL_PROD` | SQS queue URL for prod |
| `AWS_REGION` | AWS region (default: us-east-1) |

## Troubleshooting

**JSON parse failure**: Claude returned non-JSON text. Check `logs/` for the raw response. Usually caused by a context-length overflow — reduce chunk size.

**Low confidence scores**: Review fields with `0.0` scores. Likely missing from the contract or requiring prompt tuning.

**OCR quality issues**: Pre-process scanned PDFs with a higher DPI scan or use `--lang` flag with the appropriate Tesseract language pack.
